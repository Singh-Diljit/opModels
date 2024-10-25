"""Good trinom"""

import numpy as np

def priceJumps(vol, dT):
    u = np.exp(vol * np.sqrt(2*dT))
    return [u, 1, 1/u]

def probJumps(r, vol, q, dT):
    
    dT_ = dT/2
    drift = (r-q) * dT_
    noise = vol * np.sqrt(dT_)

    A = np.exp(drift + noise)
    B = np.exp(2*noise)
    norm = np.square(B - 1)
    
    pU = np.square(A - 1) / norm
    pD = np.square(B - A) / norm
    pS = 1 - pU - pD
    
    return [pU, pS, pD]

recom_TOPM = Model(priceMults=priceJumps, probMults=probJumps)
