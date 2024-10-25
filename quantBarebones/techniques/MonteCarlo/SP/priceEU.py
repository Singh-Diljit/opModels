"""MC SP EU"""

import numpy as np

def rationalPricing(vals, asset=True):
    """val = np.array"""
    return np.array([x for i, x in enumerate(vals) if x>0])

def priceEU(S_t, K, r, T, sims=50000, call=True):
    """Price Euro option via MC on SP."""
    disc = np.exp(-r*T)
    S_T = rationalPricing(S_t.sample(sims, T))
    opVals = np.maximum(S_T - K, 0) if call else np.maximum(K - S_T, 0)

    return disc * np.mean(opVals)
