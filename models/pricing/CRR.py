"""Implement Bimom CRR model."""

import numpy as np

def CRR_priceJumps(vol, dT):
    up = np.exp(vol * np.sqrt(dT))
    return [up, 1/up]

def CRR_probJumps(r, q, dT, priceUp):
    up = (np.exp((r-q)*dT) - priceDown) / (priceUp - priceDown)
    return [up, 1-up]

CRR = Model(priceMults=CRR_priceJumps, probMults=CRR_probJumps)
