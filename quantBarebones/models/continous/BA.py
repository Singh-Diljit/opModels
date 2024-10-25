"""Implement BA model."""

import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now you can import from stochProc and other modules
from stochProc.BrownianMotion import BMQ
from stochProc.Geometric import GeoQ
from models.Model.Model import qq

def phiBSM(S, r, T, vol, q):
    halfVar = vol**2 / 2
    drft = np.log(S) + (r - q - halfVar)*T
    phi = lambda u: np.exp(1j*u*drft - halfVar*T*u**2)

    return phi

def stochProcBSM(S, r, vol, q):
    driftBSM = r-q-(vol**2)/2
    BMa = BMQ(drift=driftBSM, mag=vol)
    return GeoQ(BMa, mag=S)
    
BA = qq(phi=phiBSM, stochProc=stochProcBSM, analytic=True)

a = BA.S_t(100, .08, .25, 0)
print(a.sample(10, 1))
