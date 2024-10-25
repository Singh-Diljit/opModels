"""Implement Heston model."""

import numpy as np

def phiSVJ(S, r, T, v, q, kappa, theta, xi, rho, jumpInt, jumpMean, jumpVar):
    """Compute the characteristic function for the Heston model.

    Parameters
    ----------
    S    : float : Current price of stock.
    r    : float : Annualized risk-free interest rate, continuously compounded.
    T    : float : Time, in years, until maturity.
    v    : float : Current volatility.
    q    : float : Continous dividend rate.
    kappa: float : Rate variance reverts to long variance.
    theta: float : Long variance.
    xi   : float : Vol of vol.
    rho  : float : Correlation coefficient.
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

    varComp = lambda u: np.exp(jVarHalf*u**2
                               + 1j*u*jTerm
                               - 1j*u*jVarHalf)
    
    lnPhiJump = lambda u: T*jumpInt * (-1 + varComp(u))
    phiHes = phiHeston(S, r-jumpInt*jBar, T, v, q, kappa, theta, xi, rho)
    phi = lambda u: np.exp(lnPhiJump(u)) * phiHes(u)

    return phi
    
SVJ = Model(phi=phiSVJ)
