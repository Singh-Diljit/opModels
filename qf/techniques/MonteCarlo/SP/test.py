"""test"""
from priceEU import *
from priceAM import *

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

S, r, q, vol = 36, .06, .06, .2
K, T = 40, 1
S_t = X(S, r, q, vol)

A = priceEU(S_t, K, r, T, call=False)
print(A)
#Agrees with BSM

A = priceAM(S_t, K, r, T, call=False)
print(A)

#BSM price is 5.1190960266969086
#EU MC price is 5.117882848131343
#AM MC price is 5.165913353020875
