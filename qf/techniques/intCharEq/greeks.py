"""CharEq greeks"""

import numpy as np
import scipy.integrate

def delta(phi, S, K, r, T, q, call=True):
    """Calculate delta via direct integration of phi.

    Parameters
    ----------
    phi  : func  : Characteristic function (fixed stock-related paramaters).
    S    : float : Current price of stock.
    K    : float : Strike price of the option.
    r    : float : Annualized risk-free interest rate, continuously compounded.
    T    : float : Time, in years, until maturity.
    q    : float : Continuous dividend rate.
    call : bool  : If pricing call.

    Returns
    -------
    delta_ : Delta of option

    Example(s)
    ---------
    >>>
    >>>
    >>>
    
    """
    twPhi = lambda u: phi(u-1j) / phi(-1j)

    k = np.log(K)
    trfPhi = lambda u: np.imag(np.exp(-1j*u*k) * phi(u)) / u
    trfTwi = lambda u: np.imag(np.exp(-1j*u*k) * twPhi(u)) / u
    
    B = scipy.integrate.quad(trfTwi, 0, np.inf)[0]
    delta_ = .5 + B/np.pi

    return delta_

def firstOrder(h, genPhi, S, K, r, T, q, call=True, greek='delta'):
    """Calculate first order greeks via direct integration of phi.

    Parameters
    ----------
    h    : float : Change in input.
    genPhi : func  : Characteristic function (fixed stock-related paramaters).
    S    : float : Current price of stock.
    K    : float : Strike price of the option.
    r    : float : Annualized risk-free interest rate, continuously compounded.
    T    : float : Time, in years, until maturity.
    q    : float : Continuous dividend rate.
    call : bool  : If pricing call.
    greek: str   : Greek to be calculated.

    Returns
    -------
    grk : First order greek.

    Example(s)
    ---------
    >>>
    >>>
    >>>
    
    """

    if greek == 'delta':
        return delta(phi, S, K, r, T, q, call)
    
    phi_ = genPhi(greek)
    twPhi = lambda u: phi_(u-1j) / phi_(-1j)

    k = np.log(K)
    trfPhi = lambda u: np.imag(np.exp(-1j*u*k) * phi_(u)) / u
    trfTwi = lambda u: np.imag(np.exp(-1j*u*k) * twPhi(u)) / u

    facS, facK = 1, 1
    if greek == 'theta':
        tmp = np.exp(-h*T) - np.exp(h*T)
        facS, facK = tmp, tmp
        F = np.exp(-h*T) * trfTwi_Pos - np.exp(h*T) * trfTwi_Neg
        G = np.exp(-h*T) * phi_Pos - np.exp(h*T) * phi_Neg
    elif greek == 'rho':
        facK = np.exp(-h*r) - np.exp(h*r)
        F = trfTwi
        G = np.exp(-h*r) * phi_Pos - np.exp(h*r) * phi_Neg
    elif greek == 'div':
        facS = np.exp(-h*q) - np.exp(h*q)
        F = np.exp(-h*q) * trfTwi_Pos - np.exp(h*q) * trfTwi_Neg
        G = trfPhi
    
    A = scipy.integrate.quad(G, 0, np.inf)[0]
    B = scipy.integrate.quad(F, 0, np.inf)[0]

    intK = A/np.pi
    intS = B/np.pi

    adjS, adjK = S*np.exp(-q*T), K*np.exp(-r*T)
    if call:            
        prDiff = facS*adjS/2 + adjS*intS - adjK*intK - facK*adjK/2

    else: #pricing a put #NEEDS TO GET DONE
        pITM, delta = 1 - delta, 1 - pITM
        prDiff = adjK*delta - adjS*pITM                    

    grk = prDiff / (2*h)
    return grk
