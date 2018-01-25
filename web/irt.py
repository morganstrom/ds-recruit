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
    :param theta: Array of k quadrature points
    :param mean: Mean of prior distribution (center)
    :param sd: Standard deviation of prior distribution (scale)
    :return: Numpy array of k quadrature weights for each quadrature point in theta
    """
    return norm.pdf(theta, mean, sd)


def normalize_pmf(pmf):
    """
    Normalizes a probability mass function, so that the values sum to 1
    :param pmf: Array of k unnormalized densities
    :return: Array of k normalized densities
    """
    return pmf / np.sum(pmf)


def p_correct(theta, a, b):
    """
    Probability of answering a question of a certain difficulty and discrimination
    correctly, given an array of k theta quadrature points.
    :param theta: Array of k quadrature points along ability scale
    :param a: Array of n item discrimination parameters
    :param b: Array of n item difficulty parameters
    :return: Array of length k, probabilities for answering correctly for each quadrature point
    """
    theta = np.array(theta)
    a = np.array(a)
    b = np.array(b)

    k = theta.size
    n = a.size

    theta_mat = np.tile(theta, (n, 1)).T
    a_mat = np.tile(a, (k, 1))
    b_mat = np.tile(b, (k, 1))

    z_mat = a_mat * (theta_mat - b_mat)
    return np.ones_like(z_mat) / (np.ones_like(z_mat) + np.exp(-z_mat))


def likelihood(theta, a, b, x):
    """
    Likelihood of an observed set of n responses, given an array of k quadrature points.
    :param theta: Array of k quadrature points along ability scale
    :param a: Array of n question discrimination parameters
    :param b: Array of n question difficulty parameters
    :param x: Array of n question scores (1 or 0)
    :return: Array of k likelihood values for each quadrature point in theta
    """
    p_ = p_correct(theta, a, b)
    p = np.power(p_, x) * np.power(1 - p_, 1 - x)
    return np.prod(p, axis = 1)


def eap(theta, like, prior):
    """
    Expected A Posteriori estimate of individual ability.
    :param theta: Array of k quadrature points along ability scale
    :param like: Array of k likelihood values for each quadrature point
    :param prior: Array of k prior quadrature weights for each quadrature point
    :return: Double representing the mean of the posterior distribution
    """
    return np.sum(theta * like * prior) / np.sum(like * prior)


def eap_psd(theta_hat, theta, like, prior):
    """
    Posterior Standard Deviation of EAP estimate of individual ability.
    :param theta_hat: Double representing EAP estimate of individual ability.
    :param theta: Array of k quadrature points along ability scale
    :param like: Array of k likelihood values for each quadrature point
    :param prior: Array of k prior quadrature weights for each quadrature point
    :return: Double representing the estimated posterior standard deviation
    """
    return np.sqrt(np.sum(np.power(theta - theta_hat, 2) * like * prior) / np.sum(like * prior))
