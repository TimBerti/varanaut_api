import pandas as pd
import numpy as np


def get_portfolio_df(db, tickers):

    sql = f'''
        SELECT ticker, cluster, implied_volatility_ranker
        FROM companies_display 
        WHERE ticker IN ('{"', '".join(tickers)}')
        AND cluster IS NOT NULL
        AND combined_score IS NOT NULL
        AND implied_volatility > 0
        ORDER BY combined_score DESC
    '''

    return pd.read_sql(sql, con=db.bind).set_index('ticker')


def get_data(db, excluded_tickers, max_iv):

    sql = f'''
        SELECT ticker, cluster, combined_score 
        FROM companies_display 
        WHERE ticker IN (
                SELECT UNNEST(components) FROM indices 
                WHERE ticker = 'RUA'
            )
        AND ticker NOT IN ('{"', '".join(excluded_tickers)}')
        AND cluster IS NOT NULL
        AND combined_score IS NOT NULL
        AND implied_volatility > 0
        AND implied_volatility_ranker < {max_iv}
        ORDER BY combined_score DESC
    '''

    return pd.read_sql(sql, con=db.bind)


def recommendation(db, portfolio):

    tickers = [x['ticker'] for x in portfolio]

    portfolio_df = pd.DataFrame(portfolio).join(
        get_portfolio_df(db, tickers), on='ticker', how='inner')

    df = get_data(db, tickers, portfolio_df['implied_volatility_ranker'].max())

    corr_matrix = pd.read_sql('cluster_correlation', con=db.bind).to_numpy()

    cluster_df = pd.DataFrame({'cluster': df['cluster'].unique()}).join(
        portfolio_df.groupby('cluster').sum(), on='cluster')

    cluster_df.fillna(0, inplace=True)

    cluster_weight = cluster_df.sort_values('cluster')['weight'].to_numpy()

    clusters = np.argsort(corr_matrix @ cluster_weight)[:3]

    cluster_groups = df[df['cluster'].isin(clusters)].groupby('cluster')

    return df.iloc[cluster_groups['combined_score'].idxmax()]['ticker'].to_list()
