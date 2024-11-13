"""Functions related to the put-call relationship."""

import numpy as np

def putCallParity(opPr, S, K, r, T, q, priceCall=False):
    """Use put-call parity to compute the value of a (European) option.

    Parameters
    ----------
    opPr     : float    : Price of contract.
    S        : float    : Current price of stock.
    K        : float    : Strike price of the option.
    r        : float    : Annualized risk-free interest rate, continuously compounded.
    T        : float    : Time, in years, until maturity.
    q        : Dividend : Continuous or discrete dividend.
    priceCall: bool     : If pricing call.
    
    Returns
    -------
    value : float : Price of option under put-call parity assumptions.

    Notes
    -----
    If dividend is discrete, it is assumed the first payout is not this instant.
    
    Example(s)
    ----------
    >>> putCallParity(0.5287, 100, 110, .08, .5, .01)
    >>> 6.714290387487309
    
    >>> putCallParity(6.714290387487309, 100, 110, .08, .5, .01, priceCall=True)
    >>> 0.5286999999999997

    >>> putCallParity(2, 100, 110, .05, 2.25,
                      q=[.73, .82, .76, .8], qTimes=[.5, 1, 1.5, 2])
    >>> 3.216647529846469
    
    """
    adjK = np.exp(-r*T) * K
    adjS = S - q.discount(r, T) if q.discrete else S*q.discount(T=T)
    callMinusPut = adjS - adjK

    value = opPr + callMinusPut if priceCall else opPr - callMinusPut
    return value

def putCallBound(opPr, S, K, r, T, boundCall=False):
    """Use put-call inequalties to bound the value of a (American) option.
    
    Parameters
    ----------
    opPr     : float    : Price of contract.
    S        : float    : Current price of stock.
    K        : float    : Strike price of the option.
    r        : float    : Annualized risk-free interest rate, continuously compounded.
    T        : float    : Time, in years, until maturity.
    boundCall: bool     : If bounding a call.

    Returns
    -------
    bounds : tuple : Upper and lower bounds on a fair price for the option.
    
    Example(s)
    ----------
    >>> putCallBound(2.03, 36, 37, .055, .5)
    >>> (2.026363254477799, 3.03)
    
    >>> putCallBound(2.03, 37, 35, .055, .5, boundCall=True)
    >>> (4.029999999999999, 4.979386110629113)
    
    """
    adjK = np.exp(-r*T) * K
    mxDiff = S - adjK
    mnDiff = S - K

    lower = mnDiff + opPr if boundCall else opPr - mxDiff
    upper = mxDiff + opPr if boundCall else opPr - mnDiff
    
    bounds = (max(lower, 0), upper)
    return bounds

def lowerBoundRate(callPr, putPr, S, K, T):
    """Use put-call inequalties to bound risk-free interest rate from below.

    Derivation of bound:
        By the put-call inequalities:
            C-P <= S-K*exp(-rT)
        Isolating r:
            [ln(K) - ln(S-C+P)] / T <= r
            
    *Well-definedness of ln(S-C+P):
        Quantity is well-defined iff S-C+P > 0:
           [C-P <= S-K*exp(-rT)] ==> [S-C+P >= K*exp(-rT) > 0].

    When r > 0 and K >= 1 this bound is non-trivial:
        By the put-call inequalities:
            [S-K <= C-P] ==> [-K <= C-P-S] ==> [(S-C+P)/K <= 1]
    Note: ln is negative only on (0, 1). So ln(K) > 0 and ln(S-C+P) > 0.
        That is:
            0 < [ln(K) - ln(S-C+P)] / T <= r

    Parameters
    ----------
    callPr : float : Price of contract.
    putPr  : float : Price of contract.
    S      : float : Current price of stock.
    K      : float : Strike price of the option.
    T      : float : Time, in years, until maturity.
    
    Returns
    -------
    lower : float : Lower bound for the implied risk free interest rate.
    
    Example(s)
    ----------
    >>> lowerBoundRate(0.5287, 6.714290387487309, 100, 110, .5)
    >>> 0.07058389984817895

    """
    lower = -np.log((S - callPr + putPr)/K) / T
    return lower
