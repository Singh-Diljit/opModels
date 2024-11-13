"""FFT Greeks"""

import numpy as np

def fftGreekGen(genPhi, S, K, r, T, q,
                alpha=1.3, trunc=7, n=10, call=True, ATMeps=.01,
                greek='delta'):
    """Price an option via the (inverse) FFT.

    Parameters
    ----------
    genPhi : func  : Characteristic function (fixed stock-related paramaters).
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
    greek  : str   : Information on variable input.

    Returns
    -------
    tuple : Greek at strike = K, array of desired Greek at varius strikes.

    Example(s)
    ---------
    >>>
    >>>
    >>>

    """
    atmFlag = isATM(S, K, eps=ATMeps)
    lnK = np.log(K)
    dy_, B = 2 ** (trunc - n), 2 ** trunc
    dampen = dampConst(lnK, alpha, atmFlag)
    mul = B * dampen

    twi = genPhi_FT(genPhi, r, T, alpha, atmFlag, greek):

    Y = np.arange(0, B, dy_)
    #In below also divide by difference (h in diff quotion? or did i do it)
    Q = np.exp(-1j*k*Y) * np.ediff1d(twi(Y))
    Q[0] /= 2

    values = mul * np.real(np.fft.ifft(Q))
    return values[0], values
