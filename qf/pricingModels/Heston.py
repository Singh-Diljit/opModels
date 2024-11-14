"""Implement Heston model."""

import numpy as np

def phi(S, r, T, v, q, kappa, theta, xi, rho):
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

    Returns
    -------
    res: function : Characteristic function.
    
    Example(s)
    ---------
    >>> 
    >>> 
    
    """
    xiSq = xi**2
    varSq = v**4
    lnS = np.log(S)
    
    A = lambda u: kappa - 1j*u*rho*xi
    d = lambda u: np.sqrt(A(u)**2 + (u**2 + 1j*u)*xiSq)
    g = lambda u: (A(u)-d(u)) / (A(u)+d(u))

    twiD = lambda u: np.exp(-T * d(u))
    lnRat = lambda u: np.log(1 - g(u)*twiD(u)) - np.log(1 - g(u))
    ratio = lambda u: (A(u)-d(u)) / xiSq

    lnPhi = lambda u: (1j*u*lnS + 1j*u*(r-q)*T + ratio(u)*theta*kappa*T
                       - 2*theta*kappa * lnRat(u)/xiSq
                       + varSq*ratio(u) * (1-twiD(u)) / (1-g(u)*twiD(u)))

    phi = lambda u: np.exp(lnPhi(u))

    return phi

def stochDE(S, r, T, v, q, kappa, theta, xi, rho):
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

    Returns
    -------
    res: function : Characteristic function.
    
    Example(s)
    ---------
    >>> 
    >>> 
    
    """
    drift_S = lambda t, X: (r-q)*X[0]
    drift_v = lambda t, X: kappa * (theta-X[1])
    driftVec = [drift_S, drift_v]

    drift_S = lambda t, X: X[0] * np.sqrt(X[1])
    drift_v = lambda t, X: xi * np.sqrt(X[1])
    diffMat = [[diff_S],[diff_v]]
    
    res = sSDE(drift=driftVec, diff=diffMat, P=standardBM, rho=rho, T=T)
    return res
    
Heston = Model(phi=phiHes, stochDiffEq=stochDE)
