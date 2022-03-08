import pandas as pd
import numpy as np
from random import sample
from fastapi.responses import JSONResponse


def get_portfolio_df(db, tickers):

    sql = f'''
        SELECT ticker, smb_factor, hml_factor, cma_factor, rmw_factor, implied_volatility
        FROM companies_display 
        WHERE ticker IN ('{"', '".join(tickers)}')
    '''

    return pd.read_sql(sql, con=db.bind).set_index('ticker')


def get_data(db, excluded_tickers, max_iv):

    sql = f'''
        SELECT DISTINCT ON (name) name, ticker, combined_score, smb_factor, hml_factor, cma_factor, rmw_factor
        FROM companies_display 
        WHERE ticker NOT IN ('{"', '".join(excluded_tickers)}')
        AND combined_score IS NOT NULL
        AND implied_volatility BETWEEN 1 AND {max_iv}
        AND sector != 'Financial Services'
    '''

    return pd.read_sql(sql, con=db.bind)


def calculate_recommendation(db, portfolio):

    # get data

    if len(portfolio) > 100:
        return JSONResponse(content='Portfolio must be smaller then 100', status_code=400)

    if not {type(x.get('ticker')) == str and type(x.get('weight')) in [float, int] for x in portfolio} == {True}:
        return JSONResponse(content='Wrong portfolio format.', status_code=400)

    tickers = [x['ticker'] for x in portfolio]

    portfolio_df = pd.DataFrame(portfolio).join(
        get_portfolio_df(db, tickers), on='ticker', how='inner')

    max_portfolio_iv = portfolio_df['implied_volatility'].max()

    max_iv = 1.1 * max_portfolio_iv if max_portfolio_iv > 0 else 100

    df = get_data(db, tickers, max_iv)

    # calculate portfolio vector

    portfolio_vector = np.array([[(portfolio_df['weight'] * portfolio_df['smb_factor']).sum(),
                                 (portfolio_df['weight'] *
                                  portfolio_df['hml_factor']).sum(),
                                 (portfolio_df['weight'] *
                                  portfolio_df['cma_factor']).sum(),
                                 (portfolio_df['weight'] * portfolio_df['rmw_factor']).sum()]]).T

    # calculate angle between stocks and portfolio vector

    M = df[['smb_factor', 'hml_factor', 'cma_factor', 'rmw_factor']].to_numpy()

    df['angle'] = np.abs(np.arccos((M@portfolio_vector).T[0] / np.sqrt(
        (M@M.T).diagonal() * (portfolio_vector.T@portfolio_vector)[0][0])))

    # choose 3 tickers randomly out of the 10 tickers, with the best combined score,
    # out of the 150 tickers closest (farthest) to (from) the portfolio
    # for the similar (diversification) recommendation

    tmp_similar_recommendation = df.sort_values('angle')[:150].sort_values(
        'combined_score', ascending=False)['ticker'][:10].to_list()

    tmp_diversification_recommendation = df.sort_values('angle', ascending=False)[
        :150].sort_values('combined_score', ascending=False)['ticker'][:10].to_list()

    similar_recommendation = sample(tmp_similar_recommendation, k=3)
    diversification_recommendation = sample(
        tmp_diversification_recommendation, k=3)

    return JSONResponse(content={'similar': similar_recommendation, 'diversification': diversification_recommendation})
