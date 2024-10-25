"""Implement VG model."""

import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now you can import from stochProc and other modules
from stochProc.VarianceGamma import VarianceGamma
from stochProc.Geometric import Geometric
from models.Model.Model import qq

def phiVG(S, r, T, v, q, theta, gammaVar, gammaMean):
    """Compute the characteristic function for the VG model.

    Parameters
    ----------
    S    : float : Current price of stock.
    r    : float : Annualized risk-free interest rate, continuously compounded.
    T    : float : Time, in years, until maturity.
    v    : float : Current volatility.
    theta:
    gammaVar:
    gammaMean:

    Returns
    -------
    res: function : Characteristic function.
    
    Example(s)
    ---------
    >>> 
    >>> 
    
    """
    varTerm = gammaVar * v**2 / 2
    omega = np.log(1 - theta*gammaVar - varTerm) / gammaVar
    tExp = -T/gammaVar
    
    phi_vg = lambda u: (1 - 1j*theta*gammaVar*u + varTerm*u**2) ** (tExp)

    phi = lambda u: S * np.exp((r-q-omega)*T*1j*u) * phi_vg(u)

    return phi

def stochProcVG(S, r, T, v, q, theta, gammaVar, gammaMean):
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
    omega = 5
    drift_ = lambda t, S: (omega + r - q) * t
    sp_ = VarianceGamma(drift_, gammaVar, ...)

    sp = Geometric(sp_, mag=S)
    return sp

VG = Model(phi=phiVG, stochProc=stochProcVG)
