import numpy as np
from scipy.stats import norm

# Function to estimate skill level theta
# Using Expected A Posteriori method
# http://onlinelibrary.wiley.com/doi/10.1002/ets2.12057/full

def quadrature_points(k=33):
    """
    Returns a numpy array of quadrature points along the
    ability scale, going from -4 to 4 with k quadrature points
    :param k: Number of quadrature points
    :return: Numpy array of quadrature points
    """
    return np.linspace(-4, 4, k)


def quadrature_weights(theta, mean=0, sd=1):
    """
    Prior with normal distribution, returning probability mass function
    at each quadrature point in theta.
    :param theta: Array of quadrature points
    :param mean: Mean of prior distribution (center)
    :param sd: Standard deviation of prior distribution (scale)
    :return: Numpy array representing quadrature
    weights for each element in theta
    """
    return norm.pdf(theta, mean, sd)


def p_correct(theta, a, b):
    """
    Probability of answering a question of a certain difficulty and discrimination
    correctly, given an array of possible theta quadrature points.
    :param theta: Array of quadrature points along ability scale
    :param a: double representing item discrimination
    :param b: double representing item difficulty
    :return: Array of probabilities for answering correctly for each quadrature point
    """
    z = a * (theta - b)
    return 1.0 / (1 + np.exp(-z))


def likelihood(theta, a, b, x):
    """
    Likelihood of an observed set of k responses.
    :param theta: Array of quadrature points along ability scale
    :param a: Array of k question discrimination parameters
    :param b: Array of k question difficulty parameters
    :param x: Array of k question scores (1 or 0)
    :return: Array of likelihood values for each quadrature point in theta
    """
    # Todo: Check that a, b and x have all the same length
    # Todo: Get rid of for-loop, extend p_correct to handle arrays of a and b
    if (type(x).__name__ == 'int'):
        p_ = p_correct(theta, a, b)
        return np.power(p_, x) * np.power(1 - p_, 1 - x)
    else:
        p = np.zeros((len(theta), len(x)))
        for i in np.arange(len(x)):
            p_ = p_correct(theta, a[i], b[i])
            p[:, i] = np.power(p_, x[i]) * np.power(1 - p_, 1 - x[i])
        return np.prod(p, axis = 1)


def eap(theta, L, theta_w):
    """
    Expected A Posteriori estimate of individual ability.
    :param theta: Array of quadrature points along ability scale
    :param L: Array of likelihood values for each quadrature point
    :param theta_w: Prior quadrature weights for each quadrature point
    :return: Double representing the mean of the posterior distribution
    """
    return np.sum(theta * L * theta_w) / np.sum(L * theta_w)

def eap_psd(theta_hat, theta, L, theta_w):
    """
    Posterior Standard Deviation of EAP estimate of individual ability.
    :param theta_hat: Double representing EAP estimate of individual ability.
    :param theta: Array of quadrature points along ability scale
    :param L: Array of likelihood values for each quadrature point
    :param theta_w: Prior quadrature weights for each quadrature point
    :return: Double representing the estimated posterior standard deviation
    """
    return np.sqrt(np.sum(np.power(theta - theta_hat, 2) * L * theta_w) / np.sum(L * theta_w))
