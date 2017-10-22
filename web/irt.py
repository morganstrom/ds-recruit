import numpy as np
from scipy.stats import norm

# Function to estimate skill level theta
# Using Expected A Posteriori method
# http://onlinelibrary.wiley.com/doi/10.1002/ets2.12057/full

def set_norm_prior(mean=0, sd=1):
    """
    Normal prior distribution of theta with 33 quadrature points
    """
    theta = np.arange(-4, 4.25, 0.25)
    return norm.pdf(theta, mean, sd)

def prob_correct_response(theta, a, b, D=1.702):
    """
    Calculates probability of correct response given skill level theta
    and item difficulty (b) and discrimination (a).
    D is a scaling parameter, defaulting to 1.702
    """
    # Length of array theta
    n = len(theta)
    # Likelihood at each theta
    L = np.repeat(D, n) * np.repeat(a, n) * (theta - np.repeat(b, n))
    # Probability at each theta
    p = np.ones(n) / (np.ones(n) + np.exp(-L))
    return p

def joint_probability(p_correct, score):
    """
    Calculates joint probability from expected probability of answering
    correctly and observed score
    :param p_correct: probability of correct response
    :param score: 1 if correct response, 0 if incorrect
    :return: array of joint probabilities
    """
    pass


def update_theta_eap():
    pass

