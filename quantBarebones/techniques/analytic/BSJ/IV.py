"""bsjVol"""

from scipy.stats import norm
from scipy.special import factorial
import numpy as np

def freqVol(vol, sqrtT, logChange, adjS, adjK, call=True):
    """Return the BSM price when volatility is the only variable."""
    stdDev = vol * sqrtT
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK

    else: #pricing a put
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS

    return value

def vol(opPr, S, K, r, T, q, lam, stdJ, scaleJ, sumMx, call=True,
        seed=.15, volEst=.1, eps=10**(-5), maxIts=200):
    """Get IV.

    Note that:
        1. error = opPr - pr_A
        2. vega_ = (pr_A - pr_B) / (vol_A - vol_B)
        3. volEst = volEst + error / vega_

    So:
        error / vega_ = (vol_A - vol_B) * (opPr - pr_A) / (pr_A - pr_B)

    For all prices, pr, we can work instead with with: pr/f. This implies that:
    
        1. vegaAlt = (pr_A/f - pr_B/f) / (vol_A - vol_B) = vega_/f
        2. errorAlt = opPr/f - pr_A/f = error/f

    So:
        errorAlt / vegaAlt = (error/f) / (vega_/f) = error / vega_

    Effectively allowing division by the 'factor term.'

    Paramaters
    ----------
    S      : float    
    K      : float    
    r      : float    
    T      : float
    vol    : float    
    q      : float
    lam    : float : intensity of process
    stdJ   : float : std of lognormal jump
    scaleJ : float : scale factor for jump intensity
    sumMx  : int   : Truncation of Sum
    call   : bool

    Examples
    --------
    >>> vol(opPr=17.88, S=95, K=100, r=.07, T=1, q=0,
            lam=1, stdJ=.4, scaleJ=1.1, sumMx=50)
    >>> 0.24963921962151286

    """
    yMul = lam * scaleJ * T
    factor = np.exp(-yMul)
    interval = np.arange(sumMx)

    r_n = r - lam*(scaleJ-1) + np.log(scaleJ)/T * interval
    weights = (yMul ** interval) / factorial(interval)

    opPr_ = opPr / factor
    eps_ = eps / factor

    rateTime, divTime = r_n * T, q * T
    rateDisc, divDisc = np.exp(-rateTime), np.exp(-divTime)
    adjS, adjK = S * divDisc, K * rateDisc

    sqrtT = np.sqrt(T)
    logChange = np.log(S/K) + (rateTime - divTime)

    prevVolEst = seed
    prEst = np.sum(weights *
                   freqVol(prevVolEst, sqrtT, logChange, adjS, adjK, call))
    
    for _ in range(maxIts):
        vEst_n = np.sqrt(volEst**2 + interval * stdJ**2/T)
        bsmEsts = freqVol(vEst_n, sqrtT, logChange, adjS, adjK, call)

        prevPrEst = prEst
        prEst = np.sum(weights * bsmEsts)
        
        error = opPr_ - prEst
        if abs(error) < eps_:
            break
        
        vega_ = (prEst - prevPrEst) / (volEst - prevVolEst)
        prevVolEst = volEst
        volEst += error / vega_
    
    return volEst

a = vol(opPr=17.88, S=95, K=100, r=.07, T=1, q=0, lam=1, stdJ=.4, scaleJ=1.1, sumMx=50)
print(a) #<-answer should be .25 is 0.24963921962151286

