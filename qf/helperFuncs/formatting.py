"""Format and type coercion related functions."""

import numpy as np

def makeArray(X):
    """Convert input into an array.

    Parameters
    ----------
    X : * : Data to convert into an array.

    Returns
    -------
    res : array : Array with data from input.

    Notes
    -----
    * Input should be either an iterable or an instance of a supported
    datatype. See numpy documentation for supported datatypes for an
    array.

    """
    if type(X) == np.array:
        res = X
    elif hasattr(X, '__iter__'):
        res = np.array(X)
    else:
        res = np.array([X])
        
    return res

def makeCallable(arr):
    """Make each entry in a rectangular array callable.

    Parameters
    ----------
    arr : array_like : Rectangular collection of functions or constants.

    Returns
    -------
    res: ndarray : Array of callable functions.
    
    Example(s)
    ---------
    >>> f = makeCallable([np.exp, 3])
    >>> f[0](2)
    >>> 7.38905609893065

    >>> f = makeCallable([[np.exp, 3], [5, 7]])
    >>> f[1][1](2)
    >>> 7

    """
    arr = np.array(arr)
    if arr.ndim == 1:
        res = [x if callable(x) else (lambda u: x) for x in arr]
    else:
        res = [[x if callable(x) else (lambda u: x) for x in row]
               for row in arr]
    
    return np.array(res)

def callMulti(f):
    """Make an array callable.

    Parameters
    ----------
    arr : array : Rectangular collection of functions.

    Returns
    -------
    res: func : A single callable function.
    
    Example(s)
    ---------
    >>> f = callMulti(makeCallable([[np.exp, 3], [5, 7]]))
    >>> f(2)
    >>> [[7.3890561 3.       ]
         [7.        7.       ]]

    """
    if f.ndim == 1:
        res = lambda X: np.array([f_i(X) for f_i in f])
    else:
        res = lambda X: np.array([[ff(X) for ff in f_i] for f_i in f])
    return res

def paddedVec(X, desiredLen):
    X = makeArray(X)
    padding = np.zeros(desiredLen - len(X))
    return np.append(X, padding)

def reduceTrailingZeros(X, desiredLen):
    """Make input into a np.array of desired length, padding with zeros."""
    X = list(makeArray(X))
    while X[-1] == 0:
        X.pop()
    return np.array(X)

def wrapList(X, desiredLen=2):
    if not isinstance(X, list):
        X = [X]
    if len(X) < desiredLen:
        X = X + [0]*(desiredLen - len(X))
    return X

def reduceZero(nums, objs):
    """nums: array of floats, objs: array of objs (or objs==0), same len."""
    resNums, resObjs = [], []
    for i, x in enumerate(nums):
        if x != 0 and objs[i] != 0:
            resNums.append(x)
            resObjs.append(objs[i])
    return np.array(resNums), resObjs
            
def makeRectangle(arr):
    """Return the minimal rectangular array made by padding rows with 0.

    Parameters
    ----------
    arr : array_like : List of lists to be made into a rectangular array.

    Returns
    -------
    res: array : Minimal rectangular array.
    
    Example(s)
    ---------
    >>> arr = [[1,2,3],
                [1,2]]
    >>> makeRectangle(arr)
    >>> [[1. 2. 3.]
         [1. 2. 0.]]
    
    """
    if isinstance(arr, np.ndarray):
        return arr
    lens = [len(row) for row in arr]
    maxLen = max(lens)
    res = np.zeros(shape=(len(arr), maxLen))
    for i, row in enumerate(arr):
        res[i][:lens[i]] = row
            
    return res
