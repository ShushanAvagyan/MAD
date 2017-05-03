"""
    Implementation of DecisionTree class, that represents one Decision Tree

"""

from decision_tree_build import build_tree
import numpy as np

class DecisionTree(object):
    """
    :param max_tree_depth: maximum depth for this tree.
    """
    def __init__(self, max_tree_depth):
        self.max_depth = max_tree_depth
        self.tree = None

    def fit(self, X, Y):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :param Y: 1 dimensional python list or numpy 1 dimensional array
        """
        X = np.array(X)
        Y = np.array(Y)
        X = np.column_stack((X, Y))
        self.tree = build_tree(X, 0, self.max_depth)

    def predict(self, X):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :return: Y - 1 dimension python list with labels
        """
        Y = []
        for elem in X:
            tree = self.tree
            while not tree.is_leaf:
                if elem[tree.column] >= tree.value:
                    tree = tree.true_branch

                else:
                    tree = tree.false_branch
            for k, _ in tree.current_results.items():
                Y.append(k)
                break

        return Y
