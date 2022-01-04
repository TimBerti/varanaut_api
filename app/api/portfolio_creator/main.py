import pandas as pd


def split_equal(z: int, n: int):
    '''Split z in n as equal as possible parts'''
    return [int(x + 1) if i < z % n else int(x) for i, x in enumerate([(z-z % n)/n]*n)]


def portfolio_creator(db, request):
    '''Return portfolio with n_positions, with risk under or equal to risk_coefficient'''

    sql = f'''
        SELECT ticker, cluster, combined_score
        FROM companies_display 
        WHERE ticker IN (
                SELECT UNNEST(holdings) FROM etf 
                WHERE ticker = 'VTI'
            )
        AND cluster IS NOT NULL
        AND combined_score IS NOT NULL
        AND implied_volatility > 0
        AND implied_volatility_ranker <= {request["risk_coefficient"]}
        AND sector != 'Financial Services'
    '''

    if request.get('esg'):
        sql += '''
            AND esg
        '''

    if request.get('dividend'):
        sql += '''
            AND dividend_yield > 1.5
        '''

    if request.get('value'):
        sql += '''
            AND price_earnings_ranker + price_book_ranker > 1
        '''

    if request.get('growth'):
        sql += '''
            AND revenue_growth_3y_ranker > 0.6
        '''

    sql += '''
        ORDER BY combined_score DESC
    '''

    df = pd.read_sql(sql, con=db.bind)

    clusters = df['cluster'].unique()

    n_per_cluster = split_equal(request["n_positions"], len(clusters))

    positions = []

    for cluster, n in zip(clusters, n_per_cluster):
        positions += df[df['cluster']
                        == cluster]['ticker'].head(n).tolist()

    return positions
