""" test """

from price import price
import numpy as np
from priceAM import priceAM

def priceJumps(vol, dT):
    up = np.exp(vol * np.sqrt(dT))
    return up

def probJumps(r, q, dT, priceUp):
    priceDown = 1/priceUp
    up = (np.exp((r-q)*dT) - priceDown) / (priceUp - priceDown)
    return up


S, K, T, r, vol, depth = 100, 100, .5, .08, .25, 5000
q = 0
dT = T/depth
priUp = priceJumps(vol, dT)
proUp = probJumps(r, q, dT, priUp)

A = priceAM(S, K, r, T, priUp, proUp, depth, call=True)
print(A)
9.040821700571652

A = priceAM(S, K, r, T, priUp, proUp, depth, call=False)
print(A)
5.11976561573942

