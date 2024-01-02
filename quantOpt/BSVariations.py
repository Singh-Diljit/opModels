"""Price a perpetual put and American options with constant dividend."""

from blackScholesMerton import BSM
from helperFunctions import *

def blacksApprox(spotPrice, strikePrice, intRate, T, vol, dividend, divTimes):
    """Return an approximination of a American option with constant dividend.

    Parameters
    ----------
    spotPrice : float
        Current price of stock.
    strikePrice : float
        Strike price of the option.
    intRate : float
        Annualized risk-free interest rate, continuously compounded.
    T : float
        Time, in years, until maturity.
    vol : float
        Volatility of the stock.
    dividend : float, list
        Constant dividend.
    divTimes : list
        Time, in years, of dividend payouts.

    Returns
    -------
    pseudoAm : float
        Estimate of option price.

    Example(s)
    ---------
    >>> blacksApprox(50, 55, .1, .5, .3, .7, [3/12, 5/12])
    >>> 2.6756877949596003
    
    """
    if type(dividend) != list:
        dividend = [dividend] * len(divTimes)

    #Calculate price of European option with same expiry, no dividend
    divPV = discountedDiscrete(dividend, divTimes, intRate)
    adjustedSpot = spotPrice - divPV
    euroSameT = BSM(adjustedSpot, strikePrice, intRate, T, vol, 0)

    #Calculate price of European option with expiry before final dividend
    finalDivTime = divTimes[-1]
    divPV_ = discountedDiscrete(dividend[:-1], divTimes[:-1], intRate)
    adjustedSpot_ = spotPrice - divPV_
    euroEarly = BSM(adjustedSpot_, strikePrice, intRate, finalDivTime, vol, 0)

    pseudoAm = max(euroSameT, euroEarly)

    return pseudoAm

def perpetualPut(spotPrice, strikePrice, intRate, vol, dividend):
    """Price an American put that never expires.

    Parameters
    ----------
    spotPrice : float
        Current price of stock.
    strikePrice : float
        Strike price of the option.
    intRate : float
        Annualized risk-free interest rate, continuously compounded.
    vol : float
        Volatility of the stock.
    dividend : float
        Continous dividend rate.

    Returns
    -------
    value : float
        Estimate of option price.

    Example(s)
    ---------
    >>> perpetualPut(150, 100, .08, .2, .005)
    >>> 1.8344292693352149
    
    """
    volSq = vol ** 2
    #Solve the associated quadratic
    constantTerm = intRate - dividend - volSq/2
    discriminant = constantTerm**2 + 2*volSq*intRate
    root = (-constantTerm - discriminant**.5) / volSq

    #Compute solution to ODE
    factor = strikePrice / (1 - root)
    expTerm = (root*spotPrice - spotPrice) / (root*strikePrice)
    value = factor * (expTerm ** root)
    
    return value
