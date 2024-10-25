"""Non-Recombining Binom Tree for european Options"""

import numpy as np

def priceEU(S, K, T, r, up, down, probUp, depth=5000, call=True, levels=0):
    """Price a European option via the a recombining binomial tree.

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
    - : float
    

    """
    dT = T / depth
    disc = np.exp(-r * dT)

    #Value at expiry
    S *= up ** np.arange(depth+1, dtype=float)
    S *= down ** np.arange(depth, -1, -1, dtype=float)
    opPr = np.maximum(S - K, 0) if call else np.maximum(K - S, 0)

    rowsOut = [1] * levels
    for i in np.arange(depth-1, -1, -1):
        opPr[:i+1] = disc * (probUp * np.ediff1d(opPr[:i+2]) + opPr[:i+1])
        opPr = np.maximum(opPr[:-1], 0)

        if levels and i < levels:
            rowsOut[i] = opPr[:i+1]
            
    return opPr[0] if levels == 0 else rowsOut

def priceJumps(vol, dT):
    up = np.exp(vol * np.sqrt(dT))
    return up

def probJumps(r, q, dT, priceUp):
    priceDown = 1/priceUp
    up = (np.exp((r-q)*dT) - priceDown) / (priceUp - priceDown)
    return up

S, K, T, r = 100, 100, .5, .08
vol=.25
q = 0
depth=5000
dT = T/depth
up = priceJumps(vol, dT)
down = 1/up
probUp = probJumps(r, q, dT, up)
a = priceEU(S, K, T, r, up, down, probUp)
print(a)
