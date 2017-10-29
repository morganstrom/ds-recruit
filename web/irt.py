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


def prior(theta, mean=0, sd=1):
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
    correctly, given the individual's ability theta.
    :param theta: Array of quadrature points along ability scale
    :param a: double representing item discrimination
    :param b: double representing item difficulty
    :return: Array of probabilities for answering correctly for each theta
    """
    z = a * (theta - b)
    return 1.0 / (1 + np.exp(-z))


def likelihood(theta, a, b, x):
    #a = np.repeat(1.0, 5)
    #b = np.array([-2.155, -0.245, 0.206, 0.984, 1.211])
    #x = np.array([1, 1, 0, 0, 0])
    p = np.zeros((len(theta), len(x)))
    for i in np.arange(len(x)):
        p_ = p_correct(theta, a[i], b[i])
        p[:, i] = np.power(p_, x[i]) * np.power(1 - p_, 1 - x[i])
    return np.prod(p, axis = 1)


def eap(theta, L, A):
    return np.sum(theta * L * A) / np.sum(L * A)

def eapSD(theta_hat, theta, L, A):
    return np.sqrt(np.sum(np.power(theta - theta_hat, 2) * L * A) / np.sum(L * A))
