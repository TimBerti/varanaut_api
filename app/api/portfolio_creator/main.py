import pandas as pd


def split_equal(z: int, n: int):
    '''Split z in n as equal as possible parts'''
    return [int(x + 1) if i < z % n else int(x) for i, x in enumerate([(z-z % n)/n]*n)]


def portfolio_creator(db, risk_coefficient, n_positions):
    '''Return portfolio with n_positions, with risk under or equal to risk_coefficient'''

    sql = '''
        SELECT ticker, cluster, implied_volatility_ranker, combined_score 
        FROM companies_display 
        WHERE ticker IN (
                SELECT UNNEST(components) FROM indices 
                WHERE ticker = 'RUA'
            )
        AND cluster IS NOT NULL
        AND combined_score IS NOT NULL
        AND implied_volatility > 0
        AND sector != 'Financial Services'
        ORDER BY combined_score DESC
    '''

    df = pd.read_sql(sql, con=db.bind)

    filtered_df = df[df['implied_volatility_ranker'] <= risk_coefficient]

    clusters = filtered_df['cluster'].unique()

    n_per_cluster = split_equal(n_positions, len(clusters))

    positions = []

    for cluster, n in zip(clusters, n_per_cluster):
        positions += filtered_df[filtered_df['cluster']
                                 == cluster]['ticker'].head(n).tolist()

    return positions
