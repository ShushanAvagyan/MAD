import numpy as np
from collections import defaultdict

class DecisionNode(object):
    """
    DecisionNode is a building block for Decision Trees.
    DecisionNode is a python class representing a  node in our decision tree
    """
    def __init__(self,
                 column=None,
                 value=None,
                 false_branch=None,
                 true_branch=None,
                 current_results=None,
                 is_leaf=False,
                 results=None):
        self.column = column
        self.value = value
        self.false_branch = false_branch
        self.true_branch = true_branch
        self.current_results = current_results
        self.is_leaf = is_leaf
        self.results = results


def dict_of_values(data):
    """
    param data: a 2D Python list representing the data. Last column of data is Y.
    return: returns a python dictionary showing how many times each value appears in Y
    """
    results = defaultdict(int)
    for row in data:
        r = row[len(row) - 1]
        results[r] += 1
    return dict(results)


def divide_data(data, feature_column, feature_val):
    """
    this function takes the data and divides it in two parts by a line. A line
    is defined by the feature we are considering (feature_column) and the target 
    value. The function returns a tuple (data1, data2) which are the desired parts of the data.
    For int or float types of the value, data1 have all the data with values >= feature_val
    in the corresponding column and data2 should have rest.
    For string types, data1 should have all data with values == feature val and data2 should 
    have the rest.

    param data: a 2D Python list representing the data. Last column of data is Y.
    param feature_column: an integer index of the feature/column.
    param feature_val: can be int, float, or string
    return: a tuple of two 2D python lists
    """
    data1 = []
    data2 = []

    for i in range(len(data)):
        if data[i][feature_column] >= feature_val:
            data1.append(data[i])
        else:
            data2.append(data[i])

    return data1, data2


def gini_impurity(data1, data2):

    """
    param data1: A 2D python list
    param data2: A 2D python list
    return: a number - gini_impurity 
    """
    p1 = 0
    p2 = 0
    n1 = len(data1)
    n2 = len(data2)
    for row in data1:
        if row[len(row) - 1] == 1:
           p1 += 1
    for row in data2:
        if row[len(row) - 1] == 1:
           p2 += 1
    if n1 != 0:
        p1 /= n1
    if n2 != 0:
        p2 /= n2
    
    return n1*2*p1*(1-p1) + n2*2*p2*(1-p2)


def build_tree(data, current_depth=0, max_depth=1e10):
    """
    build_tree is a recursive function.
    What it does in the general case is:
    1: find the best feature and value of the feature to divide the data into
    two parts
    2: divide data into two parts with best feature, say data1 and data2
        recursively call build_tree on data1 and data2. this should give as two 
        trees say t1 and t2. Then the resulting tree should be 
        DecisionNode(...... true_branch=t1, false_branch=t2) 


    In case all the points in the data have same Y we should not split any more, and return that node
    For this function we will give you some of the code so its not too hard for you ;)
    
    param data: A 2D python list
    param current_depth: an integer. This is used if we want to limit the number of layers in the
        tree
    param max_depth: an integer - the maximal depth of the representing
    return: an object of class DecisionNode

    """
    if len(data) == 0:
        return DecisionNode(is_leaf=True)
    if current_depth == max_depth:
        return DecisionNode(current_results=dict_of_values(data))

    if len(dict_of_values(data)) == 1:
        l = list(dict_of_values(data).keys())
        results = l[0]
        return DecisionNode(current_results=dict_of_values(data), is_leaf=True, results=results)

    self_gini = gini_impurity(data, [])
    best_gini = 1e10
    best_column = None
    best_value = None
    best_split = None

    for i in range(len(data[1])-1):
        for row in data:
            r = row[i]
            d1,d2 = divide_data(data, i, r)
            gini = gini_impurity(d1, d2)
            if gini < best_gini:
                best_gini = gini
                best_column = i
                best_value = r
    
    best_split = divide_data(data,best_column,best_value)
    
    data1, data2 = best_split

    if abs(self_gini - best_gini) < 1e-10:
        l = list(dict_of_values(data).keys())
        results = l[0]
        return DecisionNode(current_results=dict_of_values(data), is_leaf=True, results=results)

    else:
        
            current_depth += 1
            t1 = build_tree(data1, current_depth)
            t2 = build_tree(data2, current_depth)
            return DecisionNode(column=best_column, value=best_value, true_branch=t1, false_branch=t2, current_results=dict_of_values(data))
