"""Implement (inverse) FFT method for pricing an option."""

import numpy as np
from helperFuncs import genFuncs

def prFFT(phi, S, K, r, T, q,
          alpha=1.3, trunc=7, n=10, call=True, ATMeps=.01):
    """Price an option via the (inverse) FFT.

    Parameters
    ----------
    phi    : func  : Characteristic function (fixed stock-related paramaters).
    S      : float : Current price of stock.
    K      : float : Strike price of the option.
    r      : float : Annualized risk-free interest rate, continuously compounded.
    T      : float : Time, in years, until maturity.
    q      : float : Continuous dividend rate.
    alpha  : float : Dampening paramater.
    trunc  : int   : Upper bound of integration is truncated at val=2**trunc.
    n      : int   : Discretization paramater of (truncated) integral is 2**n.
    call   : bool  : If pricing call.
    ATMeps : float : Margin for option being 'at the money' vs 'out the money'.

    Returns
    -------
    tuple : Value at strike = K, array of valutions at varius strikes.

    Example(s)
    ---------
    >>> def phiBSM(S, r, T, vol, q):
            halfVar = vol**2 / 2
            drft = np.log(S) + (r - q - halfVar)*T
            phi = lambda u: np.exp(1j*u*drft - halfVar*T*u**2)

            return phi
    
    >>> phi = phiBSM(S=110, r=.1, T=.5, vol=.25, q=0.005)
    >>> prFFT(phi, S=110, K=110, r=.1, T=.5, q=0.005, alpha=1.3, trunc=7, n=10)
    >>> (10.364093173522244, array([10.36409317, 12.6594454 , 14.91652122, ...,
                                     4.4023249 ,  6.1349503 ,  8.15138504]))
         
    >>> phi = phiBSM(S=100, r=.1, T=.5, vol=.25, q=0.005)
    >>> prFFT(phi, S=100, K=110, r=.1, T=.5, q=0.005, alpha=1.3, trunc=7, n=10,
              call=False, eps=.01)
    >>> (9.901491456593313, array([ 9.90149146, 11.53241545, 13.31609257, ...,
                                    6.48552167,  7.35438554,  8.49520095]))

    """
    k, disc = np.log(K), np.exp(-r*T)
    dampen, twi = genFuncs(phi, S, K, alpha, disc, eps=ATMeps)
    dy_, B = 2 ** (trunc - n), 2 ** trunc
    mul = disc * (B/np.pi) / dampen(k)
    
    Y = np.arange(0, B, dy_)
    Q = np.exp(-1j*k*Y) * twi(Y)
    Q[0] /= 2

    values = mul * np.real(np.fft.ifft(Q))
    if not call: #price a put
        values += -S*np.exp(-q*T) + K*disc

    pos_k = 0
    return values[pos_k], values
