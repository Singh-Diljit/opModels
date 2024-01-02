"""Implement binomial pricing model, functions for Greeks, implied vol."""

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
        If using BOPM to calculate delta, gamma, or theta.
        
"""
###BOPM model
def BOPM(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=500,
         eps=10**-4, startDate=(), greeks=False):
    """Price American, European, and Bermuda options via BOPM.

    This function uses the height paramater to determine the discrete
    moments from now to expiry the option is priced. For Bermuda options,
    this can mean missing potential exerciseDates if the height is less
    than the number of trading days until expiry.
    
    Parameters
    ----------
    See document header.

    Returns
    -------
    res : float, list
        If 'greeks==False': res is the BOPM price of the option
        Else: res is a list of levels 0-3 of the option tree
        
    Example(s)
    ----------
    >>> BOPM(100, 120, .05, .5, .2, 0, 'american call', height=1000)
    >>> 1.0227329188100436

    >>> exDates = [.25, .5, .75, 1]
    >>> BOPM(120, 110, .05, 1.2, .2, .05, 'bermuda put',
             exDates, 1000, startDate='Jan 1 2024')
    >>> 5.512121137906666

    """
    #Check well-definedness of probability
    heightUpperBound = np.ceil(T * (intRate - dividend)**2 / vol**2)
    if height < heightUpperBound:
        errorMessage = f'BOPM requires: height >= {heightUpperBound}.'
        raise ValueError(errorMessage)
    
    #Frequently used values
    delT = T / height
    priceUp = np.exp(vol * np.sqrt(delT))
    priceDown = 1 / priceUp
    probUp = (np.exp((intRate-dividend)*delT) - priceDown) / (priceUp-priceDown)
    probDown = 1 - probUp
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
    price = [0] * (height+1)
    priceUpSq = priceUp ** 2
    prFactor = priceDown ** (height+2)
    for i in range(height+1):
        prFactor *= priceUpSq
        if call:
            price[i] = max(spotPrice*prFactor - strikePrice, 0)
        else: #option is a put
            price[i] = max(strikePrice - spotPrice*prFactor, 0)
   
    #Value at earlier times
    res = [0, 0, 0]
    for i in range(height-1, -1, -1):
        currentTime = delT * i
        exBerm = (bermuda and i in exSteps)
        for j in range(i+1):
            binomVal = discFactor * (probUp*price[j+1] + probDown*price[j])
            if american or exBerm:

                if call:
                    exVal = max(0, spotPrice * priceUp**(2*j-i) - strikePrice)
                else: #option is a put
                    exVal = max(0, strikePrice - spotPrice * priceUp**(2*j-i))
                price[j] = max(binomVal, exVal)

            else: #option is European or Bermuda with exercise not allowed
                price[j] = binomVal

        if greeks and i < 3: res[i] = [x for x in price[:i+1]]
            
    if not greeks:
        res = price[0]

    return res

###Greeks

def delta(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=500,
         eps=10**-4, startDate=()):
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
    >>> 0.6027636563788857

    >>> delta(100, 80, .08, 1, .2, .005, 'european put')
    >>> -0.0556145244008193
    
    """
    delT = T / height
    prUp = np.exp(vol * np.sqrt(delT))
    
    tree = BOPM(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes, height, eps, startDate, greeks=True)

    opD, opU = tree[1]
    delta_ = (opU*prUp - opD*prUp) / (spotPrice * prUp**2 - spotPrice)
    
    return delta_

def gamma(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=500, eps=10**-4,
         startDate=()):
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
    >>> gamma(95, 99, .08, 1, .2, .005, 'american call')
    >>> 0.020171905018027125

    """
    delT = T / height
    prUpSq = np.exp(2 * vol * np.sqrt(delT))
    
    tree = BOPM(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes, height, eps, startDate, greeks=True)

    opDD, opDU, opUU = tree[2]
    opUD = opDU
    spUU, spDD = spotPrice*prUpSq, spotPrice/prUpSq
    sp = spotPrice
    
    A = opUU-opUD
    B = opUD-opDD
    X = spUU - sp
    Y = sp - spDD
    Z = spUU - spDD

    gamma_ = 2 * (A*Y - B*X) / (X*Y*Z)
    
    return gamma_

def theta(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes=[], height=500, eps=10**-4,
         startDate=(), normalize=True):
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
    >>> -0.028607269234589366

    >>> theta(95, 110, .08, 1, .2, .005, 'european put')
    >>> 0.006207352950055122

    """
    tree = BOPM(spotPrice, strikePrice, intRate, T, vol, dividend,
         optionType, exerciseTimes, height, eps, startDate, greeks=True)

    opUD, op = tree[2][1], tree[0][0]
    delT = T / height
    theta_ = (opUD - op) / (2*delT)
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
    >>> 15.260267051928622
    
    """
    diff = deltaVol / 2
    volA, volB = vol - diff, vol + diff
    
    prA = BOPM(spotPrice, strikePrice, intRate, T, volA, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    prB = BOPM(spotPrice, strikePrice, intRate, T, volB, dividend,
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
    >>> 31.070465134561687
    
    >>> rho(100, 110, .08, .5, .3, 0, 'bermuda put', [.15, .3, .45])
    >>> -22.15481826988608
    
    """
    diff = deltaR / 2
    rA, rB = intRate - diff, intRate + diff
    
    prA = BOPM(spotPrice, strikePrice, rA, T, vol, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    prB = BOPM(spotPrice, strikePrice, rB, T, vol, dividend,
                optionType, exerciseTimes, height, eps, startDate)
    
    rho_ = (prB - prA) / deltaR
    
    return rho_

###Solve for volatility
def vol(spotPrice, strikePrice, intRate, T, dividend, optionType, opPr,
        prEr=10**(-4)):
    """Use BSM implied volatiltiy to find the BOPM implied vol.

    Parameters
    ----------
    See document header.
    opPr : float
        Price of option.
    prEr : float, optional
        Accepted error in optionPrice error. Not the same as error in IV.
        
    Returns
    -------
    seedVol : float
        The BOPM/BSM implied volatiltiy.
    
    Example(s)
    ----------
    >>> vol()
    >>>
    
    """
    call = isCall(optionType)
    seedVol = bsm.vol(spotPrice, strikePrice, intRate, T, dividend, opPr, call,
                   eps=prEr)
    seedPr = BOPM(spotPrice, strikePrice, intRate, T, seedVol, dividend,
                  optionType)

    error = abs(opPr - seedPr)
    if error > prEr:
        dVol = seedVol * prEr
        vega_ = vega(spotPrice, strikePrice, intRate, T, seedVol, dividend,
                     optionType)
        
    totEffort = 0
    while error > prEr and totEffort < 100:
        flag = -1 if vega_ < 0 else 1
        if opPr < seedPr:
            while opPr < seedPr:
                totEffort += 1
                seedVol -= flag * dVol
                seedPr = BOPM(spotPrice, strikePrice, intRate, T,
                              seedVol, dividend, optionType)
                error = abs(opPr - seedPr)

        else:
            while opPr > seedPr:
                totEffort += 1
                seedVol += flag*dVol
                seedPr = BOPM(spotPrice, strikePrice, intRate, T,
                              seedVol, dividend, optionType)
                error = abs(opPr - seedPr)
                
        dVol /= 10

    return seedVol
