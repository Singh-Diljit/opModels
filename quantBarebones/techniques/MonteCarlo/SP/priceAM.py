"""MC SP AM"""
import numpy as np
import math

class X:
    """Test BM class"""
    def __init__(self, S, r, q, v):
        self.S = S
        self.drift = r - q - (v**2)/2
        self.diff = v
    def sample(self, sims, idx, mag=0):
        A = self.diff*np.sqrt(idx)*np.random.normal(size=sims)
        if mag == 0:
            return self.S * np.exp(self.drift*idx + A)
        else:
            return mag * np.exp(self.drift*idx + A)

def priceAM(SP, K, r, T, sims=10000, steps=100, degree=5, call=True):
    """Longstaff and Schwartz"""
    dT = T/steps
    disc = np.exp(-r*dT)
    
    P = np.zeros((steps+1, sims), dtype=np.float64)
    P[0] = SP.S
    for i in np.arange(1, steps+1):
        P[i] = P[i-1] * SP.sample(sims, dT, mag=1)

    #generate payoffs
    opVals = np.maximum(P - K, 0) if call else np.maximum(K - P, 0)

    for i in np.arange(steps-1, 0, -1):
        leastSq = np.polyfit(P[i], opVals[i+1]*disc, degree)
        contVal = np.polyval(leastSq, P[i])
        boolEx = (opVals[i] > contVal)
        opVals[i] = opVals[i]*boolEx + opVals[i+1]*disc*(np.invert(boolEx))

    return disc * np.mean(opVals[1])
S, K, T = 36, 40, 1
r, q, v = .06, .06, .2
SP = X(S, r, q, v)
A = priceAM(SP, K, r, T, call=False)
print(A)
