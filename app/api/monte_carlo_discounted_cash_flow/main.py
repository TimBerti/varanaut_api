import numpy as np
from fastapi.responses import JSONResponse


def monte_carlo_discounted_cash_flow(n_trials=100000, n_periods=10, p_0=100, r_0=1.3, dr_0=.3, r_n=1.04, dr_n=.16, S_0=10, m=0.3, dm=0.1, terminal_multiple=15, discount_rate=.1):
    '''
    n_trials: number of trials
    n_periods: number of periods

    r_0: initial growth
    dr_0: uncertainty of initial growth

    r_n: terminal growth
    dr_n: uncertainty of terminal growth

    S_0: initial revenue per share

    m: expected margin
    dm: range of margin

    discount_rate: discount rate per period

    terminal_multiple: terminal multiple applied to last cash flow
    '''

    # calculate return and return uncertainty for each period

    r_arr = np.linspace(r_0, r_n, n_periods)
    dr_arr = np.linspace(dr_0, dr_n, n_periods)

    # calculate cash flows

    m_arr = np.random.triangular(m - dm, m, m + dm, size=(n_trials, n_periods))

    r_matrix = np.random.normal(size=(n_trials, n_periods)) * dr_arr + r_arr
    cash_flow_matrix = S_0 * r_matrix.cumprod(axis=1) * m_arr

    # discount cash flows

    discount_rate_arr = (np.ones(n_periods) / (1 + discount_rate)).cumprod()

    discounted_cash_flow_matrix = cash_flow_matrix * discount_rate_arr

    # calculate terimnal values

    terminal_value_arr = discounted_cash_flow_matrix[:, -1] * terminal_multiple

    # calculate fair values

    fair_values_arr = discounted_cash_flow_matrix.sum(
        axis=1) + terminal_value_arr

    # calculate probabilites of beeing undervalued

    hist, bin_edges = np.histogram(fair_values_arr, bins=1000, range=(
        0, np.percentile(fair_values_arr, 99)))

    cumulative_probability = hist.cumsum() / hist.sum()

    p_undervalued_arr = 1 - cumulative_probability

    return_object = JSONResponse(content={'fair_value': np.median(fair_values_arr),
                                          'p_undervalued': p_undervalued_arr[np.argmin(np.abs(bin_edges - p_0))],
                                          'cash_flow_matrix': cash_flow_matrix[:100].tolist(),
                                          'mean_cash_flow': cash_flow_matrix.mean(axis=0).tolist(),
                                          'discounted_cash_flow_matrix': discounted_cash_flow_matrix[:100].tolist(),
                                          'mean_discounted_cash_flow': discounted_cash_flow_matrix.mean(axis=0).tolist(),
                                          'hist': hist.tolist(),
                                          'bin_edges': bin_edges[:-1].tolist(),
                                          'p_undervalued_arr': p_undervalued_arr.tolist()
                                          }
                                 )

    return return_object
