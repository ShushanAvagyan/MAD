"""
    Implementation of logistic regression
"""
import numpy as np

def sigmoid(s):
    """
        sigmoid(s) = 1 / (1 + e^(-s))
    """
    return 1 / (1 + np.exp(-s))

def normalize(X):
    """
        This function normalizes X by dividing each column by its mean
    """
    norm_X = np.ones(X.shape[0])
    feature_means = [np.mean(norm_X)]
    for elem in X.T[1:]:
        feature_means.append(np.mean(elem))
        elem = elem / np.mean(elem)
        norm_X = np.column_stack((norm_X, elem))
    return norm_X, feature_means

def gradient_descent(X, Y, epsilon=1e-8, l=1, step_size=1e-4, max_steps=1000):
    """
    Implement gradient descent using full value of the gradient.
    :param X: data matrix (2 dimensional np.array)
    :param Y: response variables (1 dimensional np.array)
    :param l: regularization parameter lambda
    :param epsilon: approximation strength
    :param max_steps: maximum number of iterations before algorithm will
        terminate.
    :return: value of beta (1 dimensional np.array)
    """
    beta = np.zeros(X.shape[1])
    X, feature_means = normalize(X)
    for _ in range(max_steps):
        res = []
        for j in range(1, X.shape[1]):
            S = 0
            for i in range(X.shape[0]):
                temp = sigmoid(X[i].dot(beta)) - Y[i]
                S = S + temp*X[i, j]
            res.append((S[0] + (l / feature_means[j]**2)*beta[j])/(X.shape[0]))
        res = np.array(res)
        res0 = 0
        S = 0
        for i in range(X.shape[0]):
            temp = sigmoid(X[i].dot(beta)) - Y[i]
            S = S + temp*X[i, 0]
        res0 = S[0] /(X.shape[0])
        new_beta_zero = beta[0] - step_size * res0
        new_beta = np.array([new_beta_zero, *(beta[1:] - step_size * res)])
        if sum((beta - new_beta)**2) < (sum(beta**2) * epsilon):
            return new_beta, np.array(feature_means)
        beta = new_beta
    return beta, np.array(feature_means)
