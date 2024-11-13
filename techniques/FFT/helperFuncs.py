"""Supporting functions for inverse FFT related computations."""

import numpy as np
#from helperFunctions import isATM, discountFunc

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

def dampConst(lnK, alpha, atmFlag):
    """Evaluate a dampening function driven constant used in integration.

    Parameters
    ----------
    lnK     : func  : Characteristic function (fixed stock-related paramaters).
    alpha   : float : Dampening paramater.
    atmFlag : bool  : If option is 'at the money' or not.

    Returns
    -------
    res : float : Constant = 1/(pi * F(alpha*lnK)) for F = exp() or sinh().

    """
    if atmFlag:
        const = np.pi * np.exp(alpha*lnK)
    else:
        const = np.pi * np.sinh(alpha*lnK)

    res = 1/const
    return res

def phi_FT(phi, alpha, disc, atmFlag):
    """Transform the characteristic function by a FT-driven proccess.

    Result is equal to: FT(C_T)(ln(v)).

    Parameters
    ----------
    phi     : func  : Characteristic function (fixed stock-related paramaters).
    alpha   : float : Dampening paramater.
    disc    : float : Discount rate.
    atmFlag : bool  : If option is 'at the money' or not.

    Returns
    -------
    twiPhi : func : Transformed phi by FT-driven proccess.

    Notes
    -----
    Function is NOT the same as 'twiPhi' in 'genFuncs'. Both this and the
    'genFuncs' outputs are taylored to their uses and include simplifications
    based on the context of the equations they are used in.

    """
    if atmFlag:
        denom = lambda u: alpha**2 + alpha - u**2 + 1j*u*(2*alpha + 1)
        twiPhi = lambda u: disc * phi(u-1j*(1+alpha)) / denom(u)
    else:
        ft = lambda u: 1/(1j*u + 1) - 1/(disc * 1j*u) - phi(u-1j)/(u**2-1j*u)
        twiPhi = lambda u: disc * (ft(u - 1j*alpha) - ft(u + 1j*alpha)) / 2
        
    return twiPhi  

def genFuncs(phi, S, K, alpha, disc, eps=.01):
    """Generate functions required in executing option pricing via FFT.

    Parameters
    ----------
    phi   : func  : Characteristic function (fixed stock-related paramaters).
    S     : float : Current price of stock.
    K     : float : Strike price of the option.
    alpha : float : Dampening paramater.
    disc  : float : Discount rate.
    eps   : float : Cutoff for option being 'at the money' or not.

    Returns
    -------
    dampener : func : Dampening function for square integrability over R
    twiPhi   : func : Transformed phi by FT-driven proccess.

    Notes
    -----
    Function is NOT the same as 'twiPhi' in 'transformedChar'. Both this and
    the 'transformedChar' outputs are taylored to their uses and include
    simplifications based on the context of the equations they are used in.

    """
    atmFlag = isATM(S, K, eps)
    if atmFlag:
        dampener = lambda x: np.exp(alpha * x)
        denom_ = lambda u: alpha**2 + alpha -u**2 + 1j*u*(2*alpha + 1)
        twiPhi = lambda u: phi(u-1j*(1+alpha)) / denom_(u)
        
    else:
        dampener = lambda x: np.sinh(alpha * x)
        ft = lambda u: 1/(1j*u + 1) - 1/(disc * 1j*u) - phi(u-1j)/(u**2-1j*u)
        twiPhi = lambda u: (ft(u - 1j*alpha) - ft(u + 1j*alpha)) / 2
        
    return dampener, twiPhi

def phiVol_FT(phiVol, alpha, disc, atmFlag):
    """Transform the multi-input characteristic function by a FT-driven proccess.

    Result is equal to: FT(C_T)(ln(v)) varying in v and one of S, r, T, vol, q.

    Parameters
    ----------
    phiVol : func  : Characteristic function (wiht only 'vol' not fixed).
    alpha : float : Dampening paramater.
    disc  : float : Discount rate.
    atmFlag : bool  : If option is 'at the money' or not.

    Returns
    -------
    twiPhi : func : Transformed phiVol by FT-driven proccess.

    """
    if atmFlag:
        denom = lambda u: alpha**2 + alpha - u**2 + 1j*u*(2*alpha + 1)
        twiPhi = lambda x, u: disc * phiVol(x)(u-1j*(1+alpha)) / denom(u)

    else:
        phiTerm = lambda x, u: phiVol(x)(u-1j) / (u**2-1j*u)
        ft = lambda x, u: 1/(1j*u + 1) - 1/(disc * 1j*u) - phiTerm(x, u)
        twiPhi = lambda x, u: disc/2 * (ft(x, u - 1j*alpha) - ft(x, u + 1j*alpha))
        
    return twiPhi

"""
def genPhi_FT(genPhi, r, T, alpha, atmFlag, greek='delta'):
    #
    Transform the multi-input characteristic function by a FT-driven proccess.

    Result is equal to: FT(C_T)(ln(v)) varying in v and one of S, r, T, vol, q.

    Parameters
    ----------
    genPhi  : func  : Characteristic function (fixed stock-related paramaters).
    r       : float : Annualized risk-free interest rate, continuously compounded.
    T       : float : Time, in years, until maturity.
    alpha   : float : Dampening paramater.
    atmFlag : bool  : If option is 'at the money' or not.
    greek   : str   : Information on variable input.

    Returns
    -------
    twiPhi : func : Transformed multi-input phi by FT-driven proccess.

    #
    phi_ = genPhi(greek)
    disc = discountFunc(r, T, greek)   
    if atmFlag:
        denom = lambda u: alpha**2 + alpha - u**2 + 1j*u*(2*alpha + 1)
        twiPhi = lambda x, u: disc(x) * phi_(x)(u-1j*(1+alpha)) / denom(u)

    else:
        phiTerm = lambda x, u: phi_(x)(u-1j) / (u**2-1j*u)
        ft = lambda x, u: (1/(1j*u + 1) - 1/(disc(x) * 1j*u) - phiTerm(x, u)
        twiPhi = lambda x, u: disc(x)/2 * (ft(x, u - 1j*alpha) - ft(x, u + 1j*alpha))
        
    return twiPhi
"""


