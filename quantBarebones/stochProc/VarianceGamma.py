"""Implement a Variance-Gamma process with deterministic component."""

import numpy as np
from GammaProcess import GammaProcess
from BrownianMotion import BrownianMotion

class VarianceGamma:
    """Implement X_t = {a*t  + c*VG_t} with index set: [0, T]."""

    def __init__(self, drift, gammaVar, BMmag, mag=1, det=0, T=1):
        """Initialize VarianceGammas paramaters.

        Paramaters
        ----------
        drift    : float           : Scaling coefficiant for drift.
        gammaVar : float           : Variance in underlying Gamma Process.
        BMmag    : float           : Scaling coefficiant for Brownian motion.
        mag      : float, optional : Scaling coefficiant for stochastic process.
        det      : float, optional : Coefficiant for "+Ct' term.
        T        : float, optional : Upper end-point for index set.

        """
        self.drift = drift
        self.GP = GammaProcess(mean=1, var=gammaVar, T=T)
        self.BM = BrownianMotion(drift=mag*drift, mag=mag*BMmag, T=T)
        self.det = det
        self.T = T

    def sample(self, sims=False, simsGamma=False, simsBM=False, t=1):
        """Sample X_t.

        Paramaters
        ----------
        self     : VarianceGamma   : Stochastic proccess being sampled.
        sims     : int             : Total number of simulations drawn.
        simsGamma: int             : # of times simulated by Gamma process.
        simsBM   : int             : # of BM sims at each point in time.
        t        : float, optional : Provides instance of SP being sampled.

        Returns
        -------
        res : ndarray : Shape=(simsGamma, simsBM)
        
        """
        if sims:
            simsGamma = sims // 2
            simsBM = sims - simsGamma
            
        gammaTimes = self.GP.sample(simsGamma, t)
        detComponent = self.det * t
        VGComponent = self.BM.sample(simsBM, times=gammaTimes)

        return detComponent + VGComponent
        
a = VarianceGamma(1, 2, 2)
print(a.sample(sims=10))
