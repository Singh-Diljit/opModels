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
