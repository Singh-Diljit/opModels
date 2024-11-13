"""Test Models"""

def phiBSM(S, r, T, vol, q):
    halfVar = vol**2 / 2
    drft = np.log(S) + (r - q - halfVar)*T
    phi = lambda u: np.exp(1j*u*drft - halfVar*T*u**2)

    return phi

def phiBSM_v(S, r, T, q):
    return lambda vol: phiBSM(S, r, T, vol, q)

"""Price an option by solving for the delta and probability of ending ITM."""

import numpy as np
import scipy.integrate

def integratePhi(phi, S, K, r, T, q, call=True):
    """Price an option by calculating the delta and Pr(S_T > K).

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
    tuple : Price of option, Delta of option

    Example(s)
    ---------
    >>> def phiBSM(S, r, T, vol, q):
            halfVar = vol**2 / 2
            drft = np.log(S) + (r - q - halfVar)*T
            phi = lambda u: np.exp(1j*u*drft - halfVar*T*u**2)

            return phi
    
    >>> phi_1 = phiBSM(S=110, r=.1, T=.5, vol=.25, q=.004)
    >>> integratePhi(phi_1, S=110, K=107, r=.1, T=.5, q=.004, call=False)
    >>> (4.120882545489373, -0.30280916820133263)

    >>> phi_2 = phiBSM(S=100, r=.08, T=.5, vol=.2, q=.004)
    >>> integratePhi(phi_2, S=100, K=110, r=.08, T=.5, q=.004)
    >>> (3.3167691850158647, 0.3689885120328471)

    >>> integratePhi(phi_2, S=100, K=110, r=.08, T=.5, q=.004, call=False)
    >>> (9.203407625038103, -0.6310114879671529)

    >>> integratePhi(phi_2, S=100, K=90, r=.08, T=.5, q=.004, call=False)
    >>> (1.064584293450137, -0.13908873256331966)
    
    """
    twPhi = lambda u: phi(u-1j) / phi(-1j)

    k = np.log(K)
    trfPhi = lambda u: np.imag(np.exp(-1j*u*k) * phi(u)) / u
    trfTwi = lambda u: np.imag(np.exp(-1j*u*k) * twPhi(u)) / u
    
    A = scipy.integrate.quad(trfPhi, 0, np.inf)[0]
    B = scipy.integrate.quad(trfTwi, 0, np.inf)[0]

    pITMCall = .5 + A/np.pi
    deltaCall = .5 + B/np.pi

    adjS, adjK = S*np.exp(-q*T), K*np.exp(-r*T)
    if call:
        pr = adjS*deltaCall - adjK*pITMCall
        delta = deltaCall

    else: #pricing a put
        pr = adjK*(1 - pITMCall) - adjS*(1-deltaCall)
        delta = deltaCall - 1

    return pr, delta
