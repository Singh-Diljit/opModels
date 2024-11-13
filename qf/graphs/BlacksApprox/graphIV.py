"""Graph IV in Black's approximation."""

import numpy as np
from scipy.stats import norm

def makeDivTime(dYr, div, T):
    """Return s.t. resYr[i], resDiv[i] = div truncated at time T[i]"""
    divTimes = np.array(dYr + [-1])
    divPayouts = np.array(div + [0])

    resShape = (len(T), len(divTimes))
    divTimeRes, divPayoutRes = np.zeros(resShape), np.zeros(resShape)

    indicator = np.zeros(resShape)
    for i, t in enumerate(T):
        tmp = (divTimes < t)
        indicator[i] = tmp
        divTimeRes[i] = divTimes * tmp
        divPayoutRes[i] = divPayouts * tmp

    divTimeRes[:, -1] = T
    indicator[:, -1] = 1
    return divTimeRes, divPayoutRes, indicator

def freqVolT(vol, rootTime, logChange, adjS, adjK, call=True, indic=1):
    """Return Black's Approximation when volatility is the only variable."""
    stdDev = np.array([vol * rootT for rootT in rootTime.T]).T
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        prITM, prOTM = norm().cdf(d1), norm().cdf(d2)
        value = prITM*adjS - prOTM*adjK

    else: #pricing a put
        prITM, prOTM = norm().cdf(-d2), norm().cdf(-d1)
        value = prITM*adjK - prOTM*adjS

    prices = np.amax(value*indic, axis=1)
    return prices, stdDev

def freqVegaT(h, prA, stdDev, rootTime, logChange, adjS, adjK, call=True, indic=1):
    """Return vega when volatility is the only variable."""
    stdDev += np.array([h * rootT for rootT in rootTime.T]).T
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        prITM, prOTM = norm().cdf(d1), norm().cdf(d2)
        value = prITM*adjS - prOTM*adjK

    else: #pricing a put
        prITM, prOTM = norm().cdf(-d2), norm().cdf(-d1)
        value = prITM*adjK - prOTM*adjS

    prB = np.amax(value*indic, axis=1)
    diffQ = (prB - prA) / h
    
    return diffQ

def volT(opPr, S, K, adjK, divDisc, rateTime, rootTime,
         call=True, volEst=.1, eps=10**(-5), its=200, indic=1):
    """Compute the implied volatility of an option via Black's Approximation.
    
    This functions uses the Newton-Raphson method to iteratively find
    an approximation of volatility.

    Parameters
    ----------
    opPr     : Price of contract.
    S        : Spot stock price.
    K        : Strike price of the option.
    adjK     : 2D-Array of strike price discounted at dividend
               payout times given different maturities.
    divDisc  : 2D-Array of dividends discounted at various maturities.
    rateTime : 2D-array of dividend payout schedule times risk-free
               rate at various maturities (inlcuding maturity time).
    rootTime : 2D-array of the square-root of dividend payout schedule
               (inlcuding maturity time).
    call     : If pricing call.
    volEst   : Initial guess at volatility.
    eps      : Accepted error in optionPrice error.
        (Not the same as error in IV.)
    its      : Maximum number of iterations function will perfrom.

    Returns
    -------
    res : Array of IV's assoicated with different maturaties.
    
    Example(s)
    ----------
    >>>
    >>>
    
    """
    adjS = S - divDisc
    logChange = np.log(adjS / K) + rateTime

    h = .05
    for _ in range(its):
        prEst, stdDev = freqVolT(volEst, rootTime, logChange, adjS, adjK, call, indic)
        error = opPr - prEst
        if np.all(abs(error) < eps):
            break
        vega = freqVegaT(h, prEst, stdDev, rootTime, logChange, adjS, adjK, call, indic)
        h = error / vega
        volEst += h
    
    return volEst

def vol_VectTS(opPr, S, K, r, T, div, dYr,
               call=True, volEst=.1, eps=10**(-5), its=200):
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
    res : ndarray : res[i] = IV at each time in T for a fixed spot = S[i]
    
    Example(s)
    ----------
    >>>
    >>>
    
    """
    dYr, div, indic = makeDivTime(dYr, div, T)
    rateTime = r * dYr
    disc = np.exp(-rateTime)
    divDisc = np.cumsum(disc*div, axis=1)

    adjK = K * disc
    rootTime = np.sqrt(dYr) + (1-indic)
    
    res = np.zeros((len(S), len(T))) #matrix
    for i, spot in enumerate(S):
        res[i] = volT(opPr, spot, K, adjK, divDisc, rateTime, rootTime,
                      call, volEst, eps, its, indic)

    return res

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
    t = np.linspace(.1, T, num=5) #make 100
    A, B = min(S, K), max(S, K)
    X = np.linspace(.25*A, 1.75*B, num=5) #make 100
    m = np.log(X/K) / np.sqrt(T) 

    z = vol_VectTS(opPr, X, K, r, t, div, dYr,
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

IVsurface(19.55, 172.39, 175, .0463, 1, [.5, .5], [.5, .8],
          call=True, volEst=.1, eps=10**(-5), its=50)
