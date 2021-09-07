import numpy as np
from statsmodels.stats.correlation_tools import corr_nearest


def lambda_plus(n, m):
    '''
    Upper eigenvalue limit of the Marchenko Pastur density.
    '''

    q = float(n)/float(m)
    return (1+1/q+2*np.sqrt(1/q))


def denoise_correlation_matrix(corr):
    '''
    corr: normalized correlation matrix.

    Returns denoised correlation matrix using the Marchenko Pastur Theorem.
    '''

    evals, evecs = np.linalg.eig(corr)  # eigenvalue decomposition

    n, m = corr.shape

    # set eigenvalues smaller then lambda plus to constant, while retaining trace
    np.put(evals, np.argwhere(evals < lambda_plus(n, m)),
           evals[evals < lambda_plus(n, m)].mean())

    # calculate denoised correlation matrix
    corr_denoised = np.dot(np.dot(evecs, np.diag(evals)), np.linalg.inv(evecs))

    corr_denoised = (corr_denoised + corr_denoised.T)/2  # symmetrize matrix

    # find nearest correlation matrix
    corr_denoised = corr_nearest(corr_denoised)

    return corr_denoised
