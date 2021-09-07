import pandas as pd


def load_returns(db):
    '''
    Returns dataframe with 1 year of daily returns
    and dataframe with fama and french expectations for Russell 3000 companies
    with a relative score over or equal to 4.
    '''

    sql = '''
        SELECT ticker, fama_french_expectation FROM companies_display WHERE 
        ticker IN (
            SELECT UNNEST(components) FROM indices 
            WHERE ticker = 'RUA'
        )
        AND fama_french_expectation IS NOT NULL
        AND relative_score >= 4
        ORDER BY ticker
        ;
    '''

    fundamentals_df = pd.read_sql(sql, con=db.bind)

    tickers = fundamentals_df['ticker'].unique()

    sql = f'''
        SELECT time, ticker, adjusted_close / LAG(adjusted_close) OVER (
            PARTITION BY ticker
            ORDER BY time
        ) AS daily_return
        FROM eod WHERE ticker IN 
            ('{"', '".join(tickers)}')
        AND time > CURRENT_DATE - INTERVAL '1 year'
    '''

    daily_returns_df = pd.read_sql(sql, con=db.bind)

    daily_returns_df = daily_returns_df.pivot(
        index='time', columns='ticker', values='daily_return')

    return daily_returns_df, fundamentals_df
