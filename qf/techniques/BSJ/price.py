"""Jump Diffusion"""

from scipy.stats import norm
from scipy.special import factorial
import numpy as np
#from bsm import BSM
from testModels import BSM

def bsj(S, K, r, T, vol, q, lam, stdJ, scaleJ, sumMx, call=True):
    """

    exp(-y*m*T) * sum_{n=0}^inf (y*m*T)**n * BSM(S, K, r_n, T, v_n, q=0, call)


    Paramaters
    ----------
    S      : float    
    K      : float    
    r      : float    
    T      : float
    vol    : float    
    q      : float
    lam    : float : intensity of process
    stdJ   : float : std of lognormal jump
    scaleJ : float : scale factor for jump intensity
    sumMx  : int   : Truncation of Sum
    call   : bool

    Returns
    -------
    res : float : Price of option.

    Examples
    --------
    >>> BSJump(S=95, K=100, r=.07, T=1, vol=.25, q=0,
                lam=1, stdJ=.2, scaleJ=.4, sumMx=50, call=False)
    >>> 28.537701262519796
    
    """
    yMul = lam * scaleJ * T
    factor = np.exp(-yMul)
    interval = np.arange(sumMx)

    r_n = r - lam*(scaleJ-1) + np.log(scaleJ)/T * interval
    v_n = np.sqrt(vol**2 + interval * stdJ**2/T)
    weights = (yMul ** interval) / factorial(interval)

    BSMValues = BSM(S, K, r_n, T, v_n, q, call)

    return factor * np.sum(weights * BSMValues)

