"""Solve for risk-free interest rate."""

import numpy as np

def impliedRate(callPr, putPr, S, K, T, q, eps=.000001, maxIts=100):
    """Solve for the risk-free interest rate using put-call parity.

    When dealing with discrete dividend payout model an approximation
    is computed via a optimized binary search. The upper bound for interest
    rate is found easily after noticing the discounted div payments + discounted
    strike is decreasing with respect to interest rate.

    The lower bound is tricker but relies on noticing for positive rate,
    if t_i is non-decreasing positive then and the following values are defined:
        A = N*d_{max}*exp(-r*t_0) + K*exp(-r*t_0)
        B = N*d_{max}*exp(-r*t_0) + K*exp(-r*T)
        C = sum^N_i(d_i*exp(-r*t_i)) + K*exp(-r*T)
    then A >= B >= C where C = (discounted div payments + discounted strike).

    The case for negative rate is similar, but uses T instead of t_0 for
    the inequalities.

    Parameters
    ----------
    callPr : float : Price of contract.
    putPr  : float : Price of contract.
    S      : float : Current price of stock.
    K      : float : Strike price of the option.
    T      : float : Time, in years, until maturity.
    q      : Dividend : Continuous or discrete dividend.
    eps    : float : Margin for error of option priced with IV vs true vol.
    maxIts : int : Maximum number of iterations function will perfrom.
    
    Returns
    -------
    impliedR : float : The implied risk-free interest rate.
    
    Example(s)
    ----------
    >>> impliedRate(0.5287, 6.714290387487309, 100, 110, .5, .01)
    >>> 0.08000000000000007
    
    >>> impliedRate(60, 67.19085, 100, 120, 3, [2,2,2], [1,2,3])
    >>> 0.05480000110893794

    Notes
    -----
    'eps' and 'maxIts' are only relevant for discrete dividends.
    
    """
    if q.continous:
        adjS = S*q.discount(T=T)
        adjK = adjS - callPr + putPr
        zeroCouponBond = adjK / K #= e^(-r*T)
        impliedR = -np.log(zeroCouponBond) / T
        
    else: #non-trivial discrete dividends
        rateTerm = S + putPr - callPr
        mxSum = q.numberPayments * q.maxDiv + K

        valZero = q.total() + K
        #Early return for rate == 0.
        if valZero == rateTerm:
            impliedR = 0
            return impliedR

        #Find if rate is positive
        ratePos = (valZero > rateTerm)

        upper_denom = q.times[0] if ratePos else T
        upper = -np.log(rateTerm / mxSum) / upper_denom
        lower = -np.log(rateTerm / K) / T #Realized if q.total == 0

        if ratePos:
            lower = max(lower, 0)
            
        else:
            upper = min(upper, 0)

        for _ in range(maxIts):
            impliedR = (upper + lower) / 2
            pcParityError = (
                K * np.exp(-impliedR*T)
                + np.sum(q.div * np.exp(-impliedR*q.times)))

            if pcParityError > rateTerm:
                lower = impliedR
                
            else:
                upper = impliedR

            if eps > 0 and (abs(pcParityError - rateTerm) < eps):
                break

    return impliedR
