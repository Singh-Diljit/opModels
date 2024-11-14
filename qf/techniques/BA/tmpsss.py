"""Graph IV in Black's approximation."""

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def freqVol(vol, rootTime, logChange, adjS, adjK, call=True):
    """Return Black's Approximation when volatility is the only variable."""
    stdDev = vol * rootTime
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        prITM, prOTM = norm().cdf(d1), norm().cdf(d2)
        value = prITM*adjS - prOTM*adjK

    else: #pricing a put
        prITM, prOTM = norm().cdf(-d2), norm().cdf(-d1)
        value = prITM*adjK - prOTM*adjS

    return max(value), stdDev

def freqVega(h, prA, stdDev, rootTime, logChange, adjS, adjK, call=True):
    """Return vega when volatility is the only variable."""
    stdDev += h * rootTime
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        prITM, prOTM = norm().cdf(d1), norm().cdf(d2)
        value = prITM*adjS - prOTM*adjK

    else: #pricing a put
        prITM, prOTM = norm().cdf(-d2), norm().cdf(-d1)
        value = prITM*adjK - prOTM*adjS

    prB = max(value)
    diffQ = (prB - prA) / h
    
    return diffQ

def vol(opPr, S, K, r, T, div, dYr, call=True, volEst=.1, eps=10**(-5), its=200):
    """Compute the implied volatility of an option via Black's Approximation.
    
    This functions uses the Newton-Raphson method to iteratively find
    an approximation of volatility..

    Parameters
    ----------
    opPr   : Price of contract.
    S      : Current price of stock.
    K      : Strike price of the option.
    r      : Annualized risk-free interest rate, continuously compounded.
    T      : Time, in years, until maturity.
    vol    : Volatility of the stock.
    div    : List of dividend payment(s).
    dYr    : Time, in years, of dividend payout(s).
    call   : If pricing call.
    volEst : Initial guess at volatility.
    eps    : Accepted error in optionPrice error.
        (Not the same as error in IV.)
    its    : Maximum number of iterations function will perfrom.

    Returns
    -------
    The implied volatility.
    
    Example(s)
    ----------
    >>> vol(opPr=2.675, S=50, K=55, r=.1, T=.5, div=[.7]*2,
            dYr=[3/12, 5/12], call=True, v_0=.1, eps=10**(-5), its=200)
    >>> 0.29994845231460604
    
    """
    dYr, div = np.append(dYr, T), np.append(div, 0)
    rateTime = r * dYr
    disc = np.exp(-rateTime)
    adjS = S - np.cumsum(disc * div)
    adjK = K * disc
    rootTime = np.sqrt(dYr)
    logChange = np.log(adjS / K) + rateTime

    h = .05
    for _ in range(its):
        prEst, stdDev = freqVol(volEst, rootTime, logChange, adjS, adjK, call)
        error = opPr - prEst
        if abs(error) < eps:
            break
        vega = freqVega(h, prEst, stdDev, rootTime, logChange, adjS, adjK, call)
        h = error / vega
        volEst += h
    
    return volEst

def bashIt(opPr, X, K, r, t, div, dYr,
               call=True, volEst=.1, eps=10**(-5), its=200):
    return np.array([[vol(opPr, spot, K, r, time, div, dYr, call, volEst, eps, its)
                      for spot in X] for time in t])

def IVsurface(opPr, S, K, r, T, div, dYr,
          call=True, volEst=.1, eps=10**(-5), its=50):
    """Compute the implied volatility of an option via Black's Approximation.
    
    This functions uses the Newton-Raphson method to iteratively find
    an approximation of volatility.

    Parameters
    ----------
    opPr   : Price of contract.
    S      : Array of possible stock prices.
    K      : Strike price of the option.
    r      : Annualized risk-free interest rate, continuously compounded.
    T      : Array of time, in years, of possible until maturity.
    vol    : Volatility of the stock.
    div    : List of dividend payment(s).
    dYr    : Time, in years, of dividend payout(s).
    call   : If pricing call.
    volEst : Initial guess at volatility.
    eps    : Accepted error in optionPrice error.
        (Not the same as error in IV.)
    its    : Maximum number of iterations function will perfrom.

    Returns
    -------
    Plot the IV surface.
    
    Example(s)
    ----------
    >>>
    >>>
    
    """ 
    t = np.linspace(.01, T, num=5) #make 100
    A, B = min(S, K), max(S, K)
    X = np.linspace(.25*A, 1.75*B, num=5) #make 100
    m = np.log(X/K) / np.sqrt(T) 

#    z = vol_VectTS(opPr, X, K, r, t, div, dYr,
#               call=True, volEst=.1, eps=10**(-5), its=200)
    z = bashIt(opPr, X, K, r, t, div, dYr,
               call=True, volEst=.1, eps=10**(-5), its=200)

        
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    t, X = np.meshgrid(t, X)
    surf = ax.plot_surface(t, X, z)

    ax.set_xlabel('time')
    ax.set_ylabel('moneyness')
    ax.set_zlabel('IV')
    plt.title('IV (Black\'s Approximation')
    
    plt.show()

IVsurface(opPr=2.675, S=50, K=55, r=.1, T=.5, div=[.7]*2,
            dYr=[3/12, 5/12], call=True, volEst=.1, eps=10**(-5), its=200)
