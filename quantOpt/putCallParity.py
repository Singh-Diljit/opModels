"""Implied interest rate, bounds on interest rate, and put-call relationships."""

from numpy import log as ln
from helperFunctions import *

def putCallParity(contractPrice, spotPrice, strikePrice,
                  intRate, T, dividend, divPayout=float('inf'),
                  priceCall=False):
    """Use put-call parity to compute the value of a (European) option.
    
    Parameters
    ----------
    contractPrice : float
        Price of contract (call or put).
    spotPrice : float
        Current price of stock.
    strikePrice : float
        Strike price of the option.
    intRate : float
        Annualized risk-free interest rate, continuously compounded.
    T : float
        Time, in years, until maturity. Function assumes T != 0.
    dividend : float, list
        Either continous dividend rate, or list of payouts.
    divPayout : float, list, optional
        Time, in years, dividends are paid out until maturity. By defualt
        set to continous payouts, represented by float('inf') payouts.
        Function assumes first divPayout is not today.
    priceCall : bool, optional
        If pricing a put contract (information for call was given).

    Returns
    -------
    value : float
        The value of option under put call parity assumptions.
    
    Example(s)
    ----------
    >>> putCallParity(0.5287, 100, 110, .08, .5, .01)
    >>> 6.714290387487309
    
    >>> putCallParity(6.714290387487309, 100, 110, .08, .5, .01, priceCall=True)
    >>> 5.814409612512691

    >>> putCallParity(2, 100, 110, .05, 2.25, [.73, .82, .76, .8],
                      divPayout=[.5, 1, 1.5, 2])
    >>> 3.216647529846469
    
    """
    costStrike = discounted(strikePrice, intRate, T)

    if divPayout != float('inf') and sum(dividend) == 0:
        divPayout = float('inf')
        dividend = 0

    if divPayout == float('inf'):
        divDiscSpot = discounted(spotPrice, dividend, T)
        callMinusPut = divDiscSpot - costStrike
        
    else:
        discDiv = discountedDiscrete(dividend, divPayout, intRate)
        callMinusPut = spotPrice - discDiv - costStrike

    pricePut = (not priceCall)

    if pricePut:
        value = contractPrice - callMinusPut

    if priceCall:
        value = contractPrice + callMinusPut
        
    return value

def impliedRate(callPrice, putPrice, spotPrice, strikePrice,
                T, dividend, divPayout=float('inf'), effort=100, error=-1):
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
    callPrice, putPrice : float
        Price of contract.
    spotPrice : float
        Current price of stock.
    strikePrice : float
        Strike price of the option.
    T : float
        Time, in years, until maturity.
    dividend : float, list
        Either continous dividend rate, or list of payouts.
    divPayout : float, list, optional
        Time, in years, dividends are paid out until maturity. By defualt
        set to continous payouts, represented by float('inf') payouts.
    effort : float, optional
        Number of iterations used in the approximation of interest rate.
        Only relevant if calculation is based of discrete dividend model.
    error : float, optional
        Accepted error in the approximation of in approximation algorithm.
        This is NOT the error in the interest rate, but the putCall disrepency.
        Only relevant if calculation is based of discrete dividend model.
    
    Returns
    -------
    rate : float
        The implied risk free interest rate.
    
    Example(s)
    ----------
    >>> impliedRate(0.5287, 6.714290387487309, 100, 110, .5, .01)
    >>> 0.08000000000000007
    
    >>> impliedRate(60, 67.19085, 100, 120, 3, [2,2,2], [1,2,3])
    >>> 0.05480000110893794
    
    """
    if (divPayout != float('inf') and sum(dividend) == 0) or (not divPayout):
        divPayout = float('inf')
        dividend = 0

    if divPayout == float('inf'):
        divDiscSpot = discounted(spotPrice, dividend, T)
        costStrike = divDiscSpot - callPrice + putPrice
        zeroCouponBond = costStrike / strikePrice # = e^(-intRate * T)
        rate = -ln(zeroCouponBond) / T
        
    else:
        divPlusStrike = spotPrice + putPrice - callPrice
        
        N, divMax = len(dividend), max(dividend)
        maxSum = N*divMax + strikePrice

        #Find if rate is negative
        valZero = (discountedDiscrete(dividend, divPayout, 0)
                    + discounted(strikePrice, 0, T))
        
        if valZero == divPlusStrike:
            rate = 0
            return rate
            
        ratePos = (valZero > divPlusStrike)

        upper_denom = divPayout[0] if ratePos else T
        upper = -ln(divPlusStrike/maxSum) / upper_denom
        lower = -ln(divPlusStrike/strikePrice) / T #Realized if dividends = 0

        if ratePos: lower = max(lower, 0)
        else: upper = min(upper, 0)
            
        for _ in range(effort):
            rate = (upper + lower) / 2
            val = (discountedDiscrete(dividend, divPayout, rate)
                   + discounted(strikePrice, rate, T))
            if val > divPlusStrike: lower = rate
            else: upper = rate

            if error > 0 and abs(val - divPlusStrike) < error: break

    return rate

def putCallBound(contractPrice, spotPrice, strikePrice,
                  intRate, T, boundCall=False):
    """Use put-call inequalties to bound the value of a (American) option.
    
    Parameters
    ----------
    contractPrice : float
        Price of contract (call or put).
    spotPrice : float
        Current price of stock.
    strikePrice : float
        Strike price of the option.
    intRate : float
        Annualized risk-free interest rate, continuously compounded.
    T : float
        Time, in years, until maturity. Function assumes T != 0.
    boundCall : bool, optional
        If bounding a put contract (information for call was given).

    Returns
    -------
    bounds : tupple
        Upper and lower bounds on a fair price for the option.
    
    Example(s)
    ----------
    >>> putCallBound(2.03, 36, 37, .055, .5)
    >>> (2.026363254477799, 3.03)
    
    >>> putCallBound(2.03, 37, 35, .055, .5, boundCall=True)
    >>> (4.029999999999999, 4.979386110629113)
    
    """
    mxDiff = spotPrice - discounted(strikePrice, intRate, T)
    mnDiff = spotPrice - strikePrice

    if boundCall:
        lower = mnDiff + contractPrice
        upper = mxDiff + contractPrice
    else: #bound put
        lower = contractPrice - mxDiff
        upper = contractPrice - mnDiff

    bounds = (max(lower, 0), upper)
    
    return bounds

def lowerBoundRate(callPrice, putPrice, spotPrice, strikePrice, T):
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
    callPrice, putPrice : float
        Price of contract.
    spotPrice : float
        Current price of stock.
    strikePrice : float
        Strike price of the option.
    T : float
        Time, in years, until maturity.
    
    Returns
    -------
    lower : float
        Lower bound for the implied risk free interest rate.
    
    Example(s)
    ----------
    >>> lowerBoundRate()
    >>> 

    """
    lnNum = spotPrice - callPrice + putPrice
    lnDen = strikePrice
    lower = -ln(lnNum/lnDen) / T

    return lower
