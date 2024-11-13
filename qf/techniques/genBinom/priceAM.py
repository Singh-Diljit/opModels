"""Non-Recombining Binom Tree for American Options"""

import numpy as np

def priceAM(S, K, r, T, up, down, probUp, depth=5000, call=True, levels=0):
    """Price a Americna option via the a recombining binomial tree.

    Parameters
    ----------
    S       : float
    K       : float
    r       : float
    T       : float
    up      : priceUp
    down    : priceDown
    probUp  : float : func fixed with req. params so float
    depth   : int
    call    : bool 
    levels  : int

    Returns
    -------

    
    Example(s)
    ---------
    >>> 

    """
    dT = T / depth
    disc = np.exp(-r * dT)

    #Value at expiry
    S = S*np.ones((2, depth+1))
    S[0] *= up ** np.arange(depth+1, dtype=float)
    S[0] *= down ** np.arange(depth, -1, -1, dtype=float)
    S[1] = up * W[0]

    opPr = np.maximum(S[0] - K, 0) if call else np.maximum(K - S[0], 0)
    rowsOut = [1] * levels
    for i in np.arange(depth-1, -1, -1):
        M = i+1
        opPr[:M] = disc * (probUp * np.ediff1d(opPr[:i+2]) + opPr[:i+1])

        row = (depth+i) % 2
        A, B = (depth-i)//2, (depth-i+1)//2
        if call:
            ex = np.maximum(S[row][A:-B] - K, 0)
        else:
            ex = np.maximum(K - S[row][A:-B], 0)
            
        opPr = np.maximum(opPr[:-1], ex)
        if levels and i < levels:
            rowsOut[i] = opPr[:M]
            
    return opPr[0] if levels == 0 else rowsOut
