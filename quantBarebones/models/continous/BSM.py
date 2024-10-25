"""Implement BSM model."""

import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now you can import from stochProc and other modules
from stochProc.BrownianMotion import BMQ
from stochProc.Geometric import GeoQ
from models.Model.Model import qq

def phi(S, r, T, v, q):
    """Return the characteristic function for the BSM model.

    Parameters
    ----------
    S   : float : Current price of stock.
    r   : float : Annualized risk-free interest rate, continuously compounded.
    T   : float : Time, in years, until maturity.
    v   : float : Volatility of the stock.
    q   : float : Continous dividend rate.

    Returns
    -------
    res : function : Characteristic function.
    
    Example(s)
    ---------
    >>> 
    >>> 
    
    """
    lnS = np.log(S)
    lnPhi = lambda u: 1j*u*lnS + 1j*u*(r-q)*T - T*v**2*(u**2 + 1j*u)/2
    phi = lambda u: np.exp(lnPhi(u))
    
    return phi

def stochProc(S, r, T, v, q):
    """Return the stochastic process for the BSM model.

    Parameters
    ----------
    S   : float : Current price of stock.
    r   : float : Annualized risk-free interest rate, continuously compounded.
    T   : float : Time, in years, until maturity.
    v   : float : Volatility of the stock.
    q   : float : Continous dividend rate.

    Returns
    -------
    res : StochasticProcess : The SP for BSM.
    
    Example(s)
    ---------
    >>> 
    >>> 
    
    """
    halfVar = v**2 / 2
    BM_drift = (r - q - halfVar)*T
    BM = BrownianMotion(BM_drift, v, T)

    sp = Geometric(BM, mag=S)
    return sp
    
BSM = Model(phi, stochProc)
