import cvxpy as cp
import numpy as np


def optimal_asset_allocation(expected_returns, corr, gamma=1):
    '''
    expected_returns: array with expected returns
    corr: correlation matrix
    gamma: risk aversion coefficient from 1 to 5

    Returns optimal asset allocation for a long only portfolio.
    '''

    w = cp.Variable(corr.shape[0])

    expected_returns = np.array([expected_returns]).T

    objective = cp.Maximize(expected_returns.T@w -
                            gamma * cp.quad_form(w, corr))

    constraints = [cp.sum(w) == 1, w >= 0]

    prob = cp.Problem(objective, constraints)

    prob.solve(solver=cp.ECOS)

    return w.value
