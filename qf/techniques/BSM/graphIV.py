
from scipy.stats import norm
import numpy as np
from bsmIV import *
from graphFuncBSM import *

def volT(opPr, S, K, r, T, q, call=True, volEst=.1, maxIts=100):
    """Return the BSM implied volatility of an option.
    
    This functions uses the Newton-Raphson method to iteratively find
    an approximation of volatility assuming a BSM pricing model.

    Parameters
    ----------
    [See document header]
    opPr  : float : Price of contract.
    S     : float : Current price of stock. (float)
    K     : float : Strike price of the option. (float)
    r     : float : Annualized risk-free interest rate, continuously compounded.
    T     : float : Time, in years, until maturity.
    q     : float : Continous dividend rate.
    call  : bool  : If calculating rho of a call.
    volEst: float : Initial guess at volatility.
    eps   : float : Accepted error in option price error.
        (Not the same as error in IV.)
    maxIts: float : Maximum number of iterations function will perfrom.

    Returns
    -------
    volEst : float : The BSM implied volatility.
    
    Example(s)
    ----------
    >>> vol(19.55, 172.37, 175, .0463, 1, .0055)
    >>> 0.256812757150514
    
    """
    rateTime, divTime = r * T, q * T
    rateDisc, divDisc = np.exp(-rateTime), np.exp(-divTime)
    adjS, adjK = S * divDisc, K * rateDisc

    sqrtT = np.sqrt(T)
    logChange = np.log(S/K) + (rateTime - divTime)

    for _ in range(maxIts):
        prEst = freqVol(volEst, sqrtT, logChange, adjS, adjK, call)
        error = opPr - prEst
        vega_ = freqVega(volEst, sqrtT, logChange, adjS)
        volEst += error / vega_
    
    return volEst

def IVsurface(opPr, S, K, r, T, q, call=True,
              volEst=.1, maxIts=50):

    t = np.linspace(.01, T, num=100)
    A, B = min(S, K), max(S, K)
    X = np.linspace(.25*A, 1.75*B, num=100)
    m = np.log(X/K) / np.sqrt(T) 

    t, X = np.meshgrid(t, X)
    z = volT(opPr, X, K, r, t, q, call, volEst, maxIts)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    surf = ax.plot_surface(t, X, z)

    ax.set_xlabel('time')
    ax.set_ylabel('moneyness')
    ax.set_zlabel('IV')
    plt.title('IV')
    
    plt.show()

IVsurface(19.55, 172.37, 175, .0463, 1, .0055)

