import pandas as pd
import numpy as np


def get_portfolio_df(db, tickers):

    sql = f'''
        SELECT ticker, smb_factor, hml_factor, cma_factor, rmw_factor, implied_volatility_ranker
        FROM companies_display 
        WHERE ticker IN ('{"', '".join(tickers)}')
        AND implied_volatility > 0
        ORDER BY combined_score DESC
    '''

    return pd.read_sql(sql, con=db.bind).set_index('ticker')


def get_data(db, excluded_tickers, max_iv):

    sql = f'''
        SELECT ticker, combined_score, smb_factor, hml_factor, cma_factor, rmw_factor
        FROM companies_display 
        WHERE ticker IN (
                SELECT UNNEST(components) FROM indices 
                WHERE ticker = 'RUA'
            )
        AND ticker NOT IN ('{"', '".join(excluded_tickers)}')
        AND combined_score IS NOT NULL
        AND implied_volatility > 0
        AND implied_volatility_ranker < {max_iv}
        ORDER BY combined_score DESC
    '''

    return pd.read_sql(sql, con=db.bind)


def similar_recommendation(db, portfolio):

    # get data

    portfolio = [{'ticker': 'VRTX', 'weight': 0.2}, {'ticker': 'MSFT', 'weight': 0.2}, {
        'ticker': 'META', 'weight': 0.2}, {'ticker': 'GE', 'weight': 0.2}, {'ticker': 'NFLX', 'weight': 0.2}]

    tickers = [x['ticker'] for x in portfolio]

    portfolio_df = pd.DataFrame(portfolio).join(
        get_portfolio_df(db, tickers), on='ticker', how='inner')

    df = get_data(db, tickers, portfolio_df['implied_volatility_ranker'].max())

    # calculate portfolio vector

    portfolio_vector = np.array([[(portfolio_df['weight'] * portfolio_df['smb_factor']).sum(),
                                 (portfolio_df['weight'] *
                                  portfolio_df['hml_factor']).sum(),
                                 (portfolio_df['weight'] *
                                  portfolio_df['cma_factor']).sum(),
                                 (portfolio_df['weight'] * portfolio_df['rmw_factor']).sum()]]).T

    # calculate between stocks and portfolio vector

    M = df[['smb_factor', 'hml_factor', 'cma_factor', 'rmw_factor']].to_numpy()

    df['angle'] = np.arccos((M@portfolio_vector).T[0] / np.sqrt(
        (M@M.T).diagonal() * (portfolio_vector.T@portfolio_vector)[0][0]))

    # choose best stocks in the closest 50

    return df.sort_values('angle')[:50].sort_values('combined_score', ascending=False)['ticker'][:3].to_list()
