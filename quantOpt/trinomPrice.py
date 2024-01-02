"""Implement trinomial pricing model, functions for Greeks, implied vol."""

import numpy as np
from helperFunctions import *
import calander
import blackScholesMerton as bsm

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
    optionType : str
        Type of option being priced. Choices are: 
            "American Call", "American Put", "European Call"
            "European Put", "Bermuda Call", "Bermuda Put"
    exerciseTimes : list, optional
        Increasing list of times (in years) the option can be exercised.
    height : int
        The height of the binomial tree.
    eps : float, optional
        Accepted error in determining close ex.
    startDate : str, tuple (dd, mm, yyyy), optional
                See calander.parseDate lists all acceptable inputs
                EX: 'Dec. 21 2025', '12/21/25', '21 Dec 25', (21, 12, 2025)
        Start date of option - for exact exercise dates.
    greeks : bool, optional
        If using TOPM to calculate delta, gamma, or theta.
        
"""
###TOPM model
def TOPM(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=250,
         eps=10**-4, startDate=(), greeks=False):
    """Price American, European, and Bermuda options via TOPM.

    This function uses the height paramater to determine the discrete
    moments from now to expiry the option is priced. For Bermuda options,
    this can mean missing potential exerciseDates if the height is less
    than the number of trading days until expiry.
    
    Parameters
    ----------
    See document header.

    Returns
    -------
    price[0] : float
        The BOPM price of the option.
        
    Example(s)
    ----------
    >>> TOPM(100, 120, .05, .5, .2, 0, 'american call', height=500)
    >>> 1.0227329188091918

    >>> exDates = [.25, .5, .75, 1]
    >>> TOPM(120, 110, .05, 1.2, .2, .05, 'bermuda put',
             exDates, 1000, startDate='Jan 1 2024')
    >>> 5.51068389326396

    """
    #Check well-definedness of probability
    heightUpperBound = np.ceil(T/2 * (intRate - dividend)**2 / vol**2)
    if height < heightUpperBound:
        errorMessage = f'TOPM requires: height >= {heightUpperBound}.'
        raise ValueError(errorMessage)
    
    #Frequently used values
    delT = T / height
    priceUp = np.exp(vol * np.sqrt(2*delT))
    priceDown = 1/priceUp
    stable = 1
    expFactor = vol * np.sqrt(delT/2)
    normFactor = (np.exp(expFactor) - np.exp(-expFactor)) ** 2
    probUp = (np.exp((intRate-dividend)*delT/2) - np.exp(-expFactor)) ** 2 / normFactor
    probDown = (np.exp(expFactor) - np.exp((intRate-dividend)*delT/2)) ** 2 / normFactor
    probStable = 1 - (probUp + probDown)
    discFactor = np.exp(-intRate * delT)
    
    #Option Type
    call = isCall(optionType)
    put = (not call)
    american, european, bermuda = exerciseType(optionType)

    if bermuda:
        if not exerciseTimes:
            bermuda, european = False
        else:
            if startDate:
                dayT = calander.oneDay(startDate, T)
            else:
                dayT = 1/252
            exSteps = overlapRange(exerciseTimes, delT, height, dayT, eps)
    
    #Value at expiry
    price = [0] * (2*height+1)
    prFactor = priceDown ** (height+1)
    
    for i in range(2*height+1):
        prFactor *= priceUp
        if call:
            price[i] = max(spotPrice*prFactor - strikePrice, 0)
        else: #option is a put
            price[i] = max(strikePrice - spotPrice*prFactor, 0)
   
    #Value at earlier times
    for i in range(height-1, -1, -1):
        currentTime = delT * i
        exBerm = (bermuda and i in exSteps)
        for j in range(2*i + 1):
            trinomPr = (probUp*price[j+2]
                        + probStable*price[j+1]
                        + probDown*price[j])
            trinomVal = discFactor * trinomPr
            if american or exBerm:
                if call:
                    exVal = max(0, spotPrice * priceUp**(j-i) - strikePrice)
                else: #option is a put
                    exVal = max(0, strikePrice - spotPrice * priceUp**(j-i))
                price[j] = max(trinomVal, exVal)

            else: #option is European or Bermuda with exercise not allowed
                price[j] = trinomVal
        if i == 2 and greeks:
            thetaCalc = price[2]
    if greeks:
        res = [price[0], thetaCalc]
    return price[0] if not greeks else res

###Greeks minus gamma
def delta(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=400,
         eps=10**-4, startDate=(), deltaSpot=10**-5):
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
    >>> delta(95, 99, .08, 1, .2, .005, 'european call')
    >>> 0.6142208556880746

    >>> delta(100, 80, .08, 1, .2, .005, 'european put')
    >>> -0.05778247273990899
    
    """
    diff = deltaSpot / 2
    spA, spB = spotPrice - diff, spotPrice + diff
    
    prA = TOPM(spA, strikePrice, intRate, T, vol, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    prB = TOPM(spB, strikePrice, intRate, T, vol, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    
    delta_ = (prB - prA) / deltaSpot
  
    return delta_

def theta(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=400,
         eps=10**-4, startDate=(), deltaT=10**-3, normalize=True):
    """Return the theta of an option.

    For exact theta, initialize startDate, calander.py will then
    calculate the total number of trading days from startDate to T years
    in the future, and from that divide the total number of days by T,
    to accurately equidistrube theta each day in the options interval.

    Parameters
    ----------
    [See document header]
    normalize : bool, optional
        If theta will be normalized by days in the year.
        
    Returns
    -------
    theta_ : float
        The theta.
    
    Example(s)
    ----------
    >>> theta(95, 99, .08, 1, .2, .005, 'american call')
    >>> -0.028619027867760577

    >>> theta(95, 110, .08, 1, .2, .005, 'european put')
    >>> 0.006211160561653978

    """
    op = TOPM(spotPrice, strikePrice, intRate, T, vol, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    theta_ = (op[1]-op[0]) / (2*T/height)

    if normalize:
        days = calander.trDays(startDate, T) if startDate else 252
        T_ = T if startDate else 1
        theta_ = theta_ * T_ / days  #normalize to calculate theta per day

    return theta_

def vega(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=500, eps=10**-4,
         startDate=(), deltaVol=10**-4):
    """Return the vega of an option.

    Parameters
    ----------
    See document header.
    deltaVol : float, optional
        The change in vol used to approximate vega.

    Returns
    -------
    vega_ : float
        The vega.
    
    Example(s)
    ----------
    >>> vega(100, 90, .08, .5, .2, 0, 'european call')
    >>> 15.634841935607824
    
    """
    diff = deltaVol / 2
    volA, volB = vol - diff, vol + diff
    
    prA = TOPM(spotPrice, strikePrice, intRate, T, volA, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    prB = TOPM(spotPrice, strikePrice, intRate, T, volB, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    
    vega_ = (prB - prA) / deltaVol

    return vega_

def rho(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=500, eps=10**-4,
         startDate=(), deltaR=10**-4):
    """Return the rho of an option.

    Parameters
    ----------
    See document header.
    deltaR : float, optional
        The change in intRate used to approximate vega.
        
    Returns
    -------
    rho_ : float
        The rho.
    
    Example(s)
    ----------
    >>> rho(100, 90, .08, .5, .3, 0, 'american call')
    >>> 31.076106565244288
    
    >>> rho(100, 110, .08, .5, .3, 0, 'bermuda put', [.15, .3, .45])
    >>> -22.497356868189655
    
    """
    diff = deltaR / 2
    rA, rB = intRate - diff, intRate + diff
    
    prA = TOPM(spotPrice, strikePrice, rA, T, vol, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    prB = TOPM(spotPrice, strikePrice, rB, T, vol, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    
    rho_ = (prB - prA) / deltaR
    
    return rho_
