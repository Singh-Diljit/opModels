"""Implement Heston model, functions for Greeks"""

import numpy as np

"""
The following parameters are used in nearly every function in
this file. For sake of brevity they are listed below, and referred
back to as required.

    Parameters
    ----------
    spotPrice : float
        Current price of stock.
    spotVol : float
        Current volatility of stock.
    intRate : float
        Annualized risk-free interest rate, continuously compounded.
    T : float
        Time, in years, until maturity.
    longVol : int, float
        Volatility of stock.
    rateVol : int, float
         Dividend yield, continuously compounded.
    correlation : int, float
        The correlation between Wiener processes used to model vol and price.
    steps : int, optional
        Number of discretization made.
    sims : int, optional
        
"""
###Heston model
def hestonDisc(spotPrice, spotVol, intRate, T,
    longVol, volOfVol, rateVol, correlation, steps=500):
    """Return volatility and price approximations from a simulation of Heston.

    Parameters
    ----------
    See document header.

    Returns
    -------
    price : float
        Price after one simulation of Heston.
    vol : float
        Volatility after one simulation of Heston.
    
    Notes
    -----
    This function uses O(1) memory - useful for fine approximations,
    but slightly slower than if we sample outside the for loop.
    
    Example(s)
    ----------
    >>> hestonDisc(spotPrice=100, spotVol=.2, intRate=.04, T=2,
        longVol=.15, volOfVol=.3, rateVol=.4, correlation=.6)
    >>> (96.7112883007313, 0.16729993691416314)

    """
    dt = T / steps
    pr, vo = spotPrice, spotVol    
    for i in range(1, steps+1):
        Z_v, x_ = np.random.normal(size=2)
        Z_s = correlation*x_ + np.sqrt(1-correlation)*x_

        vo += (rateVol * (longVol-vo) * dt + volOfVol * np.sqrt(vo*dt) * Z_v)
        pr += (intRate * pr * dt + np.sqrt(vo*dt) * pr * Z_s)
            
        vo = max(0, vo)
    
    return pr, vo

def hestonMonteCarlo(spotPrice, strikePrice, spotVol, intRate, T,
    rateVol, longVol, volOfVol, correlation, steps=750, sims=500, call=True):
    """Return volatility and price approximations from a simulation of Heston.
    
    Parameters
    ----------
    See document header.

    Returns
    -------
    price : float
        Price of option.
    vol : float
        Volatility of option.
    
    Example(s)
    ----------
    >>> hestonMonteCarlo(105, 100, .01, 0, 1, 2, .01, .1, 0)
    >>> 7.492916765096218

    """
    price = 0
    for _ in range(sims):
        pr_, vo_ = hestonDisc(spotPrice, spotVol, intRate, T,
                    longVol, volOfVol, rateVol, correlation, steps)

        diff = pr_ - strikePrice if call else -pr_ + strikePrice
        price += max(diff, 0)

    value = np.exp(-intRate * T) * price
    
    return value / sims
