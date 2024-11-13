"""Solve for implied volatility when using (inverse) FFT to price an option."""

import numpy as np
from price import prFFT

def IV(opPr, phiVol, S, K, r, T, q, alpha=1.3, trunc=7, n=10, call=True,
       seed=.15, volEst=.1, ATMeps= .01, IVeps=.0001, maxIts=200):
    """Solve for implied volatility via the (inverse) FFT.

    Parameters
    ----------
    opPr   : float : Price of option.
    phiVol : func  : Characteristic function (wiht only 'vol' not fixed).
    S      : float : Current price of stock.
    K      : float : Strike price of the option.
    r      : float : Annualized risk-free interest rate, continuously compounded.
    T      : float : Time, in years, until maturity.
    q      : float : Continuous dividend rate.
    alpha  : float : Dampening paramater.
    trunc  : int   : Upper bound of integration is truncated at val=2**trunc.
    n      : int   : Discretization paramater of (truncated) integral is 2**n.
    call   : bool  : If pricing call.
    seed   : float : Initial guess for volatility.
    volEst
    ATMeps : float : Margin for option being 'at the money' vs 'out the money'.
    IVeps  : float : Margin for error of option priced with IV vs true vol.
    maxIts : float : Maximum number of iterations function will perfrom.

    Returns
    -------
    volEst : float : Estimated volatility.

    Example(s)
    ---------
    >>> WORKS SEE TEST FILE
    >>>
    >>>

    """

    prevVolEst = seed
    seededPhi = phiVol(prevVolEst)
    prEst = prFFT(seededPhi, S, K, r, T, q, alpha, trunc, n, call, ATMeps)[0]
    
    for _ in range(maxIts):
        prevPrEst = prEst
        seededPhi = phiVol(volEst)
        prEst = prFFT(seededPhi, S, K, r, T, q, alpha, trunc, n, call, ATMeps)[0]

        error = opPr - prEst
        if abs(error) < IVeps:
            break
        
        vega_ = (prEst - prevPrEst) / (volEst - prevVolEst)
        
        prevVolEst = volEst
        volEst += error / vega_
    
    return volEst

def IV2(opPr, phiVol, S, K, r, T, q, alpha=1.3, trunc=7, n=10, call=True,
       seed=.15, volEst=.1, ATMeps= .05, IVeps=.0001, maxIts=200):
    """DOES NOT WORK ABOVE WORKS, KEPT TO MAKE ABOVE FASTER"""
    atmFlag = isATM(S, K, eps=ATMeps)
    dy_, B = 2 ** (trunc - n), 2 ** trunc
    lnK = np.log(K)
    dampen = dampConst(alpha, lnK, atmFlag)
    mul = B * dampen

    opPrNormalized = opPr / mul
    epsNormalized = IVeps / mul

    disc = np.exp(-r*T)
    twi = phiVol_FT(phiVol, alpha, disc, atmFlag)
    
    Y = np.arange(0, B, dy_)
    eVec = np.exp(-1j*lnK*Y)

    prevVol = seed
    Q = eVec * twi(prevVol, Y)
    Q[0] /= 2
    prEstNormalized = np.real(np.fft.ifft(Q))[0]

    for _ in range(maxIts):
        prevPrNorm = prEstNormalized
        Q = eVec * twi(volEst, Y)
        Q[0] /= 2
        prEstNormalized = np.real(np.fft.ifft(Q))[0]        
        error = opPrNormalized - prEstNormalized
        if abs(error) < epsNormalized:
            break
        vega_ = (prevPrNorm - prEstNormalized) / (prevVol - volEst)

        prevVol = volEst
        volEst += error / vega_
    
    return volEst
