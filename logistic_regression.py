import numpy as np


def mean_f(X):
    X = np.array(X)
    mean_ = np.array([1])
    for i in range(1, X.shape[1]):
        mean_ = np.append(mean_, np.mean(X[:,i]))
    return mean_


def f(X):
    X_ = np.array(X, dtype=np.float64)
    for i in range(len(X)):
        X_[i] /= mean_f(X)
    return X_


def sigmoid(s):
    return 1 / (1 + np.exp(-s))


def normalized_gradient(X, Xnorms, Y, beta, l):
    """
    :param X: data matrix (2 dimensional np.array)
    :param Y: response variables (1 dimensional np.array)
    :param beta: value of beta (1 dimensional np.array)
    :param l: regularization parameter lambda
    :return: normalized gradient, i.e. gradient normalized according to data
    """
    grad = np.zeros(X.size)
    for i in range(X.size):
        grad[i] = Y*X[i] * (1-sigmoid(Y*(beta.T.dot(X))))/Xnorms[i]
    return grad


def gradient_descent(X, Y, epsilon=1e-6, l=1, step_size=1e-4, max_steps=10):
    X = np.column_stack((np.ones(len(X)), X))
    Xnorms = mean_f(X)
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
    X = f(X)
    for s in range(max_steps):
        for i in range(len(X)):
            grad = normalized_gradient(X[i],Xnorms, Y[i], beta, l)
            beta[0] = beta[0] + grad[0]
            for i in range(1, X.shape[1]-1):
                beta[i] = beta[i] + (step_size) * grad[i] / X.shape[0]
    return beta
 
