"""First order greeks for BSJ."""

from scipy.stats import norm
import numpy as np

def firstOrder(h, S, K, r, T, vol, y, v, m, N, greek='delta'):
    """Compute first order sensitivites via difference quotiant.

    Parameters
    ----------
    h    : float : Radius of paramater interval. 
    S    : float : Current price of stock.
    K    : float : Strike price of the option.
    r    : float : Annualized risk-free interest rate, continuously compounded.
    T    : float : Time, in years, until maturity.
    vol  : float : Volatility of the stock.
    y = intensity of process
    v = std of lognormal jump
    m = scale factor for jump intensity
    N = truncate infin
    call : bool  : If pricing call.
    greek: str   : Paramater whose sensativity is being measured.

    Returns
    -------
    float : Approximation of greek.

    Example(s)
    ---------
    >>> firstOrder(h=.1, ...)
    >>> 
    
    """
    if greek == 'theta':
        prA = BSJump(S, K, r, T-h, vol, y, v, m, N)
        prB = BSJump(S, K, r, T+h, vol, y, v, m, N)

    if greek == 'rho':
        prA = BSJump(S, K, r-h, T, vol, y, v, m, N)
        prB = BSJump(S, K, r+h, T, vol, y, v, m, N)
        
    if greek == 'delta':
        prA = BSJump(S-h, K, r, T, vol, y, v, m, N)
        prB = BSJump(S+h, K, r, T, vol, y, v, m, N)

    if greek == 'vega':
        prA = BSJump(S, K, r, T, vol-h, y, v, m, N)
        prB = BSJump(S, K, r, T, vol+h, y, v, m, N)

    diffQ = (prB - prA) / (2*h)
    return diffQ
