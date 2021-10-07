from .data import load_returns
from .marchenko_pastur import denoise_correlation_matrix
from .asset_allocation import optimal_asset_allocation
import numpy as np


def sigmoid_scaler(x):
    x = (x - np.mean(x)) / np.std(x)
    return 2 / (1 + np.exp(-1.66 * x)) - 1


def optimal_portfolio(gamma, db):
    '''
    Returns the optimal portfolio regarding the risk aversion coefficient gamma
    using the fama and french five factor model and marchenko pastur denoising
    '''

    daily_returns_df, fundamentals_df = load_returns(db)

    daily_returns_df = (daily_returns_df - daily_returns_df.mean()
                        ) / daily_returns_df.std()    # normalize

    corr = daily_returns_df.corr()

    fundamentals_df = fundamentals_df[fundamentals_df['ticker'].isin(
        corr.index)]    # filter NAs

    expected_return = sigmoid_scaler(
        np.log(fundamentals_df['fama_french_expectation'] / 100 + 1))

    corr_denoised = denoise_correlation_matrix(
        corr)

    # calculate allocations

    weights = optimal_asset_allocation(
        expected_return, corr_denoised, gamma)

    fundamentals_df['weight'] = weights

    fundamentals_df = fundamentals_df[fundamentals_df['weight'] >= 1e-5]

    fundamentals_df.reset_index(drop=True, inplace=True)

    fundamentals_df.index += 1

    return fundamentals_df[['ticker', 'weight']].to_dict(orient='records')
