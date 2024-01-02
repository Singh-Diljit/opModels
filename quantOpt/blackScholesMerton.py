"""Implement the Black-Scholes model, functions for Greeks, implied vol."""

from numpy import log as ln, exp
from statistics import NormalDist as normal
from helperFunctions import *

"""
The following parameters are used in nearly every function in
this file. For sake of brevity they are listed below, and referred
back to as required.

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
    dividend : float
        Continous dividend rate.
    priceCall : bool, optional
        If pricing a call contract.
    call : bool, optional
        If calculating Greek for a call.
        
"""
###BSM model
def BSM(spotPrice, strikePrice, intRate, T, vol, dividend, priceCall=True):
    """Return the BSM price of an option.

    Parameters
    ----------
    See document header.

    Returns
    -------
    value : float
        The BSM value of the option.
    
    Example(s)
    ----------
    >>> BSM(100, 110, .08, .5, .2, .004)
    >>> 3.3167691850161702
    
    >>> BSM(100, 90, .08, .5, .2, .004, priceCall=False)
    >>> 1.0645842934501353
    
    """
    stdDev = vol * (T**.5)
    logChange = ln(spotPrice/strikePrice) + (intRate-dividend)*T
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    costStrike = discounted(strikePrice, intRate, T)
    divDiscSpot = discounted(spotPrice, dividend, T)
    
    if priceCall:
        prITM, prOTM = normal().cdf(d1), normal().cdf(d2)
        value = expVal(prITM, divDiscSpot) - expVal(prOTM, costStrike)

    else: #pricing a put
        prITM, prOTM = normal().cdf(-d2), normal().cdf(-d1)
        value = expVal(prITM, costStrike) - expVal(prOTM, divDiscSpot)

    return value

###Greeks
def delta(spotPrice, strikePrice, intRate, T, vol, dividend, call=True):
    """Return the delta of a option.

    Parameters
    ----------
    See document header.

    Returns
    -------
    delta_ : float
        The delta.
    
    Example(s)
    ----------
    >>> delta(95, 99, .08, 1, .2, .005)
    >>> 0.6029303105314465
    
    >>> delta(100, 80, .08, 1, .2, .005, call=False)
    >>> -0.05555806850625897
    
    """
    stdDev = vol * (T**.5)
    logChange = ln(spotPrice/strikePrice) + (intRate-dividend)*T
    d1 = (logChange)/stdDev + stdDev/2
    
    prITM = normal().cdf(d1)
    if call:
        delta_ = exp(-dividend*T) * prITM

    else: #delta of a put
        delta_ = exp(-dividend*T) * (prITM-1)
        
    return delta_

def gamma(spotPrice, strikePrice, intRate, T, vol, dividend):
    """Return the gamma of an option.

    Parameters
    ----------
    See document header.

    Returns
    -------
    gamma_ : float
        The gamma.
    
    Example(s)
    ----------
    >>> gamma(95, 99, .08, 1, .2, .005)
    >>> 0.020151022323663708

    """
    stdDev = vol * (T**.5)
    logChange = ln(spotPrice/strikePrice) + (intRate-dividend)*T
    d1 = (logChange)/stdDev + stdDev/2
    gamma_ = exp(-dividend*T) * normal().pdf(d1) / (spotPrice*stdDev)

    return gamma_

def theta(spotPrice, strikePrice, intRate, T, vol, dividend, call=True,
          startDate=(), normalize=True):
    """Return the theta of an option.

    For exact BSM theta, initialize startDate, calander.py will then
    calculate the total number of trading days from startDate to T years
    in the future, and from that divide the total number of days by T,
    to accurately equidistrube theta each day in the options interval.

    Parameters
    ----------
    [See document header]
    startDate : str, tuple (dd, mm, yyyy), optional
                See calander.parseDate lists all acceptable inputs
                EX: 'Dec. 21 2025', '12/21/25', '21 Dec 25', (21, 12, 2025)
        Start date of option.
    normalize : bool, optional
        If theta will be normalized by days in the year.
        
    Returns
    -------
    theta_ : float
        The theta.
    
    Example(s)
    ----------
    >>> theta(95, 99, .08, 1, .2, .005)
    >>> -0.028598714481995045

    >>> theta(95, 110, .08, 1, .2, .005, call=False)
    >>> 0.006205233615442862

    """
    stdDev = vol * (T**.5)
    logChange = ln(spotPrice/strikePrice) + (intRate-dividend)*T
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    costStrike = discounted(strikePrice, intRate, T)
    divDiscSpot = discounted(spotPrice, dividend, T)
    pdfd1 = normal().pdf(d1)

    if call:
        prITM, prOTM = normal().cdf(d1), normal().cdf(d2)
        theta_ = (-divDiscSpot * normal().pdf(d1) * vol / (2 * T**.5)
                  + dividend * divDiscSpot * prITM
                  - intRate * costStrike * prOTM)
        
    else: #theta of a put
        prOTM, prITM = normal().cdf(-d1), normal().cdf(-d2)
        theta_ = (-divDiscSpot * normal().pdf(d1) * vol / (2 * T**.5)
                  - dividend * divDiscSpot * prOTM
                  + intRate * costStrike * prITM)
    if normalize:
        days = calander.trDays(startDate, T) if startDate else 252
        T_ = T if startDate else 1
        theta_ = theta_ * T_ / days  #normalize to calculate theta per day

    return theta_

def vega(spotPrice, strikePrice, intRate, T, vol, dividend):
    """Return the vega of an option.

    Parameters
    ----------
    See document header.

    Returns
    -------
    vega_ : float
        The vega.
    
    Example(s)
    ----------
    >>> vega(100, 90, .08, .5, .2, 0)
    >>> 15.428798828843359
    
    """
    stdDev = vol * (T**.5)
    logChange = ln(spotPrice/strikePrice) + (intRate-dividend)*T
    d1 = (logChange)/stdDev + stdDev/2

    divDiscSpot = discounted(spotPrice, dividend, T)
    vega_ = divDiscSpot * normal().pdf(d1) * T**.5

    return vega_

def rho(spotPrice, strikePrice, intRate, T, vol, dividend, call=True):
    """Return the rho of an option.

    Parameters
    ----------
    See document header.

    Returns
    -------
    rho_ : float
        The rho.
    
    Example(s)
    ----------
    >>> rho(100, 90, .08, .5, .3, 0)
    >>> 31.076085664197915
    
    >>> rho(100, 110, .08, .5, .3, 0, call=False)
    >>> -33.98445676619597
    
    """
    stdDev = vol * (T**.5)
    logChange = ln(spotPrice/strikePrice) + (intRate-dividend)*T
    d2 = (logChange)/stdDev - stdDev/2

    costStrike = discounted(strikePrice, intRate, T)
    if call:
        rho_ = costStrike * T * normal().cdf(d2)

    else: #vega of a put
        rho_ = -costStrike * T * normal().cdf(-d2)

    return rho_

###Solve for volatility
def vol(spotPrice, strikePrice, intRate, T, dividend, optionPrice,
        call=True, seedVol=.1, eps=10**(-5), maxIterations=200):
    """Return the BSM implied volatility of an option.
    
    This functions uses the Newton-Raphson method to iteratively find
    an approximation of volatility assuming a BSM pricing model.

    Parameters
    ----------
    [See document header]
    optionPrice : float
        Price of option.
    call : bool, optional
        If the option used for IV is a call.
    seedVol : float, optional
        Initial guess at volatility.
    eps : float, optional
        Accepted error in optionPrice error. Not the same as error in IV.
    maxIterations : float, optional
        Maximum number of iterations function will perfrom.

    Returns
    -------
    seedVol : float
        The BSM implied volatility.
    
    Example(s)
    ----------
    >>> vol(172.37, 175, .0463, 1, .0055, 19.55)
    >>> 0.256812757150514
    
    """
    for _ in range(maxIterations):
        BSMpr = BSM(spotPrice, strikePrice, intRate, T, seedVol, dividend, call)
        error = optionPrice - BSMpr
        if abs(error) < eps:
            break
        vega_ = vega(spotPrice, strikePrice, intRate, T, seedVol, dividend)
        seedVol += error / vega_
    
    return seedVol
