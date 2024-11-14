"""BSM< greeks"""

from scipy.stats import norm
import numpy as np

def delta(S, K, r, T, vol, q, call=True):
    """Return the delta of an option.

    Parameters
    ----------
    S   : float : Current price of stock. (float)
    K   : float : Strike price of the option. (float)
    r   : float : Annualized risk-free interest rate, continuously compounded.
    T   : float : Time, in years, until maturity.
    vol : float : Volatility of the stock.
    q   : float : Continous dividend rate.
    call: bool  : If calculating delta of a call.

    Returns
    -------
    delta_ : float : The delta of the option.
    
    Example(s)
    ----------
    >>> delta(95, 99, .08, 1, .2, .005)
    >>> 0.6029303105314465
    
    >>> delta(100, 80, .08, 1, .2, .005, call=False)
    >>> -0.05555806850625897
    
    """
    rateTime, divTime = r * T, q * T
    divDisc = np.exp(-divTime)
    stdDev = vol * np.sqrt(T)
    logChange = np.log(S/K) + (rateTime - divTime)
    d1 = (logChange)/stdDev + stdDev/2
    
    cdf_d1 = norm().cdf(d1)
    if call:
        delta_ = divDisc * cdf_d1

    else: #delta of a put
        delta_ = divDisc * (cdf_d1-1)
        
    return delta_

def gamma(S, K, r, T, vol, q):
    """Return the gamma of an option.

    Parameters
    ----------
    S   : float : Current price of stock. (float)
    K   : float : Strike price of the option. (float)
    r   : float : Annualized risk-free interest rate, continuously compounded.
    T   : float : Time, in years, until maturity.
    vol : float : Volatility of the stock.
    q   : float : Continous dividend rate.

    Returns
    -------
    gamma() : float : The gamma of the option.
    
    Example(s)
    ----------
    >>> gamma(95, 99, .08, 1, .2, .005)
    >>> 0.020151022323663708

    """
    rateTime, divTime = r * T, q * T
    divDisc = np.exp(-divTime)
    stdDev = vol * np.sqrt(T)
    logChange = np.log(S/K) + (rateTime - divTime)
    d1 = (logChange)/stdDev + stdDev/2

    return np.exp(-divTime) * norm().pdf(d1) / (S*stdDev)

def theta(S, K, r, T, vol, q, call=True, startDate=(), normalize=True):
    """Return the theta of an option.

    For exact BSM theta, initialize startDate, calander.py will then
    calculate the total number of trading days from startDate to T years
    in the future, and from that divide the total number of days by T,
    to accurately equidistrube theta each day in the options interval.

    Parameters
    ----------
    S   : float : Current price of stock. (float)
    K   : float : Strike price of the option. (float)
    r   : float : Annualized risk-free interest rate, continuously compounded.
    T   : float : Time, in years, until maturity.
    vol : float : Volatility of the stock.
    q   : float : Continous dividend rate.
    call: bool  : If calculating delta of a call.
    
    startDate : str, tuple : Start date of option.
        See calander.parseDate for acceptable date inputs
        EX: 'Dec. 21 2025', '12/21/25', '21 Dec 25', (21, 12, 2025)     
    normalize : bool : If theta will be normalized by days in the year.
        
    Returns
    -------
    theta_ : float : The theta.
    
    Example(s)
    ----------
    >>> theta(95, 99, .08, 1, .2, .005)
    >>> -0.028598714481995045

    >>> theta(95, 110, .08, 1, .2, .005, call=False)
    >>> 0.006205233615442862

    """
    rateTime, divTime = r * T, q * T
    rateDisc, divDisc = np.exp(-rateTime), np.exp(-divTime)
    adjS, adjK = S * divDisc, K * rateDisc
    
    sqrtT = np.sqrt(T)
    stdDev = vol * sqrtT
    
    logChange = np.log(S/K) + (rateTime - divTime)
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev
    
    pdf_d1 = norm().pdf(d1)
    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        theta_ = (- adjS * pdf_d1 * vol/(2 * sqrtT)
                  + q * adjS * cdf_d1
                  - r * adjK * cdf_d2)
        
    else: #theta of a put
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        theta_ = (- adjS * pdf_d1 * vol/(2 * sqrtT)
                  - q * adjS * cdf_neg_d1
                  + r * adjK * cdf_neg_d2)
        
    if normalize:
        days = calander.trDays(startDate, T) if startDate else 252
        T_ = T if startDate else 1
        theta_ = theta_ * T_ / days  #normalize to calculate theta per day

    return theta_

def vega(S, K, r, T, vol, q):
    """Return the vega of an option.

    Parameters
    ----------
    S   : float : Current price of stock. (float)
    K   : float : Strike price of the option. (float)
    r   : float : Annualized risk-free interest rate, continuously compounded.
    T   : float : Time, in years, until maturity.
    vol : float : Volatility of the stock.
    q   : float : Continous dividend rate.

    Returns
    -------
    vega() : float : The vega.
    
    Example(s)
    ----------
    >>> vega(100, 90, .08, .5, .2, 0)
    >>> 15.428798828843359
    
    """
    rateTime, divTime = r * T, q * T
    divDisc = np.exp(-divTime)
    adjS, sqrtT = S * divDisc, np.sqrt(T)
    
    stdDev = vol * sqrtT
    logChange = np.log(S/K) + (rateTime - divTime)
    d1 = (logChange)/stdDev + stdDev/2

    return adjS * norm().pdf(d1) * sqrtT

def rho(S, K, r, T, vol, q, call=True):
    """Return the rho of an option.

    Parameters
    ----------
    S   : float : Current price of stock. (float)
    K   : float : Strike price of the option. (float)
    r   : float : Annualized risk-free interest rate, continuously compounded.
    T   : float : Time, in years, until maturity.
    vol : float : Volatility of the stock.
    q   : float : Continous dividend rate.
    call: bool  : If calculating rho of a call.

    Returns
    -------
    rho_ : float : The rho.
    
    Example(s)
    ----------
    >>> rho(100, 90, .08, .5, .3, 0)
    >>> 31.076085664197922
    
    >>> rho(100, 110, .08, .5, .3, 0, call=False)
    >>> -33.984456766195976
    
    """
    rateTime, divTime = r * T, q * T
    stdDev = vol * np.sqrt(T)
    logChange = np.log(S/K) + (rateTime - divTime)
    d2 = (logChange)/stdDev - stdDev/2

    adjK = K * np.exp(-rateTime)
    if call:
        rho_ = adjK * T * norm().cdf(d2)

    else: #rho of a put
        rho_ = -adjK * T * norm().cdf(-d2)

    return rho_
