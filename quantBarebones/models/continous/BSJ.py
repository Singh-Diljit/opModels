"""Implement BSJ model."""

import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now you can import from stochProc and other modules
from models.Model.Model import qq
def phiBSJ(S, r, T, v, q, jumpInt, jumpMean, jumpVar):
    """Compute the characteristic function for the Heston model.

    Parameters
    ----------
    S    : float : Current price of stock.
    r    : float : Annualized risk-free interest rate, continuously compounded.
    T    : float : Time, in years, until maturity.
    v    : float : Current volatility.
    q    : float : Continous dividend rate.
    jumpInt : float : Intesity of jump process. (lambda)
    ln(1+J) = N(jumpMean, jumpVar)
    jumpMean: float : Mean of each jump
    jumpVar : float : Variance of 

    Returns
    -------
    res: function : Characteristic function.
    
    Example(s)
    ---------
    >>> 
    >>> 
    
    """
    jVarHalf = jumpVar/2
    jTerm = jumpMean + jVarHalf
    jBar = np.exp(jTerm) - 1
    
    driftComp = lambda u: r - q - v**2 - jumpInt*jBar
    expTerm = lambda u: np.exp(-jVarHalf*u**2 + 1j*jumpMean*u - 1)
    lnPhi = lambda u: -.5*T*(u*v)**2 + 1j*u*driftComp(u) + jumpInt*expTerm(u)

    phi = lambda u: np.exp(lnPhi)

    return phi

BSJ = Model(phi=phiBSJ)
