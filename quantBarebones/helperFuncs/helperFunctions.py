"""General supporting functions."""

import numpy as np

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

    Given a list points, [p_1, ..., p_M], and a list of
    multiples of x: [0, x, ...,(N-1)x], find all i s.t. there
    exists p_j in P and  p_j <= x*i < p_j + fwd, with eps accepted
    error in comparing floats.
    
    Parameters
    ----------
    points : list
        Non-decreasing list of floats.
    x : float
        Base value.
    N : int
        Total number of steps.
    fwd : float
        Defines range of each point.
    eps : float, optional
        Accepted error in comparing floats.
        
    Returns
    -------
    res : set
        Set of integers satisfying condition

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
    """Number of nodes on a given level.

    Assumes no collision (no two nodes are the same or will be the same.)
    By stars and bars the number of nodes is given by:
        (lvl + gRate - 1) CHOOSE (lvl - 1)

    Parameters
    ----------
    lvl  : int : Level of tree
    gRate: int : NUmber of nodes spawned by each node.

    Returns
    -------    
    res : int : number of nodes on a level.
    
    Example(s)
    ---------
    >>> 

    """
    return math.comb(lvl + gRate - 1, lvl - 1)
