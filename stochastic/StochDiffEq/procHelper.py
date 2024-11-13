"""Helper functions used in the implemention of the sSDE class."""

import numpy as np

"""
Need to do sSDE_str.
Diffuculty in printing string of functions.
"""

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

def identity3D(M, N):
    """Generate a 3-D matrix with each entry a 2-D identity matrix.

    Parameters
    ----------
    N : int : Number of (M, M) - identity matrices.
    M : int : Provides dimension of identity matrix.

    Returns
    -------
    res: ndarray : 3-D array of shape=(M, N, N) with res[i] = np.identity(N).
    
    Example(s)
    ---------
    >>> identity3D(2, 3)
    >>> [[[1. 0.]
          [0. 1.]]

         [[1. 0.]
          [0. 1.]]

         [[1. 0.]
          [0. 1.]]]
    
    """    
    return np.array([np.identity(M)]*N)

def idRho(shape_tuple):
    """Generate a 4-D matrix with each entry a 2-D identity matrix.

    n = numSDE
    p = numProc
    d = dimProc

    each process has a 3D matrix, namely a 2D matrix (n by n) for each of its
    dimension of the process. Result is n of identity3D(d, p)

    Assumes P^1, ..., P^M are ind. AND if dim(P^i) > 1 each comp is ind.
        
    """
    numSDE, numProc, dimProc = shape_tuple
    return np.array([[np.identity(dimProc)]*numProc]*numSDE)

def sSDE_str(data):
    """Return a string representing a single SDE or system of SDEs.

            f_1(t, X_t)dt + g^1_1(t, X_t)dP^1_t + ... + g^1_M(t, X_t)dP^M_t
                                        .
    dX_t =                                  .
                                        .
            f_d(t, X_t)dt + g^d_1(t, X_t)dP^1_t + ... + g^d_M(t, X_t)dP^M_t

    Indexing set: [start, end]

    """
    return 'cats'
