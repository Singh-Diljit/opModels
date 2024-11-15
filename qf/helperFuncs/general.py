"""General (math-focused) supporting functions."""

import numpy as np
import math
from formatting import makeArray

def isATM(S, K, eps=.01):
    """Return if abs(S-K) <= eps."""
    return abs(S-K) <= eps

def discountFunc(r=1, T=1, greek='delta'):
    """Generate a callable discount-rate function.

    Parameters
    ----------
    r     : float : Annualized risk-free interest rate, continuously compounded.
    T     : float : Time, in years, until maturity.
    greek : str   : Information on variable input.

    Returns
    -------
    disc : func : Vectorized discount-rate function of one variable.

    """
    if greek == 'rho':
        disc = lambda x: np.exp(-x*T) 
    elif greek == 'theta':
        disc = lambda x: np.exp(-r*x)
    else:
        disc = lambda x: np.exp(-r*T)
        
    return disc

def overlapRange(points, x, N, fwd, eps=10**-4):
    """Return the intersection of a list of ranges and a list of multiples.

    Parameters
    ----------
    points : list  : Non-decreasing list of floats.
    x      : float : Base value.
    N      : int   : Total number of steps.
    fwd    : float : Defines range of each point.
    eps    : float : Accepted error in comparing floats.
        
    Returns
    -------
    res : set : Set of integers satisfying overlap condition.

    Notes
    -----
    Given P = [p_1, ..., p_m] and a fixed number, 'fwd' this function
    finds all non-negative integers, i, such that there exists:
        p_j with p_j <= x*i < p_j + fwd.
    When comparing floats an error of 'eps' is accepted.

    Example(s)
    ----------
    >>> overlapRange([1/10, 1/6, 1/5, 1/2], 1/36, 72, .005, eps=10**-4)
    >>> {18, 6}
    
    """
    res, P = set(), len(points)
    i, j = 0, 0
    pos = 0
    while i < N and j < P:
        if pos <= points[j] - eps:
            i += 1
            pos += x
        elif pos > points[j] + fwd + eps:
            j += 1
        else: #pos is within range
            res.add(i)
            i += 1
            pos += x

    return res

def numNodes(lvl, gRate):
    """Use stars-and-bars to compute the number of nodes on a given level.

    Parameters
    ----------
    lvl  : int : Level of tree
    gRate: int : Number of nodes spawned by each node.

    Returns
    -------    
    res : int : Number of nodes on a level.

    Notes
    -----
    This function assumes no two nodes are the same value on any given
    level. The result is given by stars and bars which says the answer is
    res = (lvl + gRate - 1) CHOOSE (lvl - 1).
    
    Example(s)
    ---------
    >>> numNodes(5, 3)
    >>> 35

    """
    return math.comb(lvl + gRate - 1, lvl - 1)

def forward(S, r, T, q, c):
    """Return the forward value.

    Parameters
    ----------
    S : float : Current price of asset.
    r : float : Annualized risk-free interest rate, continuously compounded.
    T : float : Time, in years, until maturity.
    q : float : Continuous dividend rate.
    c : float : Convenience yield.

    Returns
    -------
    - : float : The forward value of S.

    """
    return S * np.exp((r_c - q)*T)

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

def equalStepSize(inc, eps=10**(-6)):
    """Return if an array has more than one value, upto eps."""
    arr = makeArray(inc)
    return (np.max(arr) - np.min(arr)) < eps
