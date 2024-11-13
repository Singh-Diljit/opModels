"""CharEq Vol"""

import numpy as np
import scipy.integrate
from price import integratePhi

def IV(opPr, phiVol, S, K, r, T, q, call=True,
       seed=.15, volEst=.1, eps=10**(-5), maxIts=200):
    """Solve for implied volatility.

    Parameters
    ----------
    opPr   : float : Price of option.
    phiVol : func  : Characteristic function (wiht only 'vol' not fixed).
    S      : float : Current price of stock.
    K      : float : Strike price of the option.
    r      : float : Annualized risk-free interest rate, continuously compounded.
    T      : float : Time, in years, until maturity.
    q      : float : Continuous dividend rate.
    call   : bool  : If pricing call.
    seed   : float : Initial guess for volatility.
    eps    : float : Margin for error of option priced with IV vs true vol.
    maxIts : float : Maximum number of iterations function will perfrom.

    Returns
    -------
    volEst : float : Estimated volatility.

    Example(s)
    ---------
    >>>
    >>>
    >>>

    """
    prevVolEst = seed
    seededPhi = phiVol(prevVolEst)
    prEst = integratePhi(seededPhi, S, K, r, T, q, call)[0]
    
    for _ in range(maxIts):
        prevPrEst = prEst
        seededPhi = phiVol(volEst)
        prEst = integratePhi(seededPhi, S, K, r, T, q, call)[0]

        error = opPr - prEst
        if abs(error) < eps:
            break
        
        vega_ = (prEst - prevPrEst) / (volEst - prevVolEst)
        
        prevVolEst = volEst
        volEst += error / vega_
    
    return volEst

def phiBSM(S, r, T, vol, q):
    halfVar = vol**2 / 2
    drft = np.log(S) + (r - q - halfVar)*T
    phi = lambda u: np.exp(1j*u*drft - halfVar*T*u**2)

    return phi

def phiBSM_v(S, r, T, q):
    return lambda vol: phiBSM(S, r, T, vol, q)

#Ans is .25
phi_1 = phiBSM_v(S=110, r=.1, T=.5, q=.004)
A = IV(4.120882545489373, phi_1, S=110, K=107, r=.1, T=.5, q=.004, call=False)
print(A)
0.25000002705223145


#Ans is .2
phi_2 = phiBSM_v(S=100, r=.08, T=.5, q=.004)
A = IV(3.3167691850158647, phi_2, S=100, K=110, r=.08, T=.5, q=.004)
print(A)
0.20000000017822603

#Ans is .2
A = IV(9.203407625038103, phi_2, S=100, K=110, r=.08, T=.5, q=.004, call=False)
print(A)
0.20000000017822664

#Ans is .2
A = IV(1.064584293450137, phi_2, S=100, K=90, r=.08, T=.5, q=.004, call=False)
print(A)
0.19999958041701843
