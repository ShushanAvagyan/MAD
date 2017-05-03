"""
    Implementation of Random Forest class
"""

from collections import defaultdict
import numpy as np
from decision_tree_build import build_tree

class RandomForest(object):
    """
    RandomForest a class, that represents Random Forests.

    :param num_trees: Number of trees in the random forest
    :param max_tree_depth: maximum depth for each of the trees in the forest.
    :param ratio_per_tree: ratio of points to use to train each of
        the trees.
    """
    def __init__(self, num_trees, max_tree_depth, ratio_per_tree=0.5):
        self.num_trees = num_trees
        self.max_tree_depth = max_tree_depth
        self.ratio_per_tree = ratio_per_tree
        self.trees = None

    def fit(self, X, Y):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :param Y: 1 dimensional python list or numpy 1 dimensional array
        """
        self.trees = []
        X = np.array(X)
        Y = np.array(Y)
        X = np.column_stack((X, Y))
        for _ in range(self.num_trees):
            np.random.shuffle(X)
            self.trees.append(build_tree(X[0:int(self.ratio_per_tree * X.shape[0])],
                                         0, self.max_tree_depth))
    def aux_predict(self, X):
        """
        Auxiliary function for prediction
        """
        Y = []
        for tree in self.trees:
            Y_temp = []
            for elem in X:
                while not tree.is_leaf:
                    if elem[tree.column] >= tree.value:
                        tree = tree.true_branch

                    else:
                        tree = tree.false_branch
                for k in tree.current_results.keys():
                    Y_temp.append(k)
                    break
            Y.append(Y_temp)
        Y = np.array(Y)
        return Y


    def predict(self, X):
        """
        :param X: 2 dimensional python list or numpy 2 dimensional array
        :return: 1 dimension python list with labels
        """
        Y = self.aux_predict(X)
        ans = []
        for row in Y.T:
            results = defaultdict(int)
            for elem in row:
                results[elem] += 1
            d = dict(results)
            max_qty = 0
            best_value = 0
            for value, qty in d.items():
                if qty > max_qty:
                    max_qty = qty
                    best_value = value
            ans.append(best_value)
        return ans
