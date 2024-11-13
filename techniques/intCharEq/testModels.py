"""testModels"""

def phiBSM(S, r, T, vol, q):
    halfVar = vol**2 / 2
    drft = np.log(S) + (r - q - halfVar)*T
    phi = lambda u: np.exp(1j*u*drft - halfVar*T*u**2)
    return phi

from scipy.stats import norm
import numpy as np

def BSM(S, K, r, T, vol, q, call=True, delta=False):
    """Price an American option paying discrete dividends.

    Parameters
    ----------
    S    : float : Current price of stock. (float)
    K    : float : Strike price of the option. (float)
    r    : float : Annualized risk-free interest rate, continuously compounded.
    T    : float : Time, in years, until maturity.
    vol  : float : Volatility of the stock.
    q    : float : Continous dividend rate.
    call : bool  : If pricing call.
    delta: bool : If returning delta of option.

    Returns
    -------
    res: float, tuple : float - Price of option, tuple - price and delta.
    
    Example(s)
    ---------
    >>> BSM(100, 110, .08, .5, .2, .004)
    >>> 3.3167691850161702
    
    >>> BSM(100, 90, .08, .5, .2, .004, call=False, delta=True)
    >>> (1.0645842934501353, -0.13908873256331983)
    
    """
    rateTime, divTime = r * T, q * T
    rateDisc, divDisc = np.exp(-rateTime), np.exp(-divTime)
    adjS, adjK = S * divDisc, K * rateDisc
    
    stdDev = vol * np.sqrt(T)
    logChange = np.log(S/K) + (rateTime - divTime)
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev
    
    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK
        delta_ = cdf_d1

    else:
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS
        delta_ = -cdf_neg_d1

    return (value, delta_) if delta else value

