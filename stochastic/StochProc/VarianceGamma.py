"""Implement a Variance-Gamma process with deterministic component."""

import numpy as np
from GammaProcess import GammaProcess
from BrownianMotion import BrownianMotion
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Index.Index import *

class VarianceGamma:
    """Implement X_t = {a*t  + c*VG_t} with index set: [0, T]."""

    def __init__(self, drift, gammaVar, BMmag, mag=1, det=0, index=None):
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
        self.GP = GammaProcess(mean=1, var=gammaVar)
        self.BM = BrownianMotion(drift=mag*drift, mag=mag*BMmag)
        self.det = det
        self.index = Index(0) if index is None else index

    def sample(self, sims, idx, scale=1):
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
        simsGamma = sims // 2
        simsBM = sims - simsGamma
            
        gammaTimes = self.GP.sample(simsGamma, idx)
        detComponent = self.det * idx
        VGComponent = np.array([self.BM.sample(simsBM, idx=gammaIDX)
                                for gammaIDX in gammaTimes])

        return detComponent + VGComponent

    def sampleIndex(self, sims, scale=1):
        if self.index.continuous:
            sampVals = np.linspace(self.index.start,
                               min(max(100, self.index.start), self.index.end),
                               100)
            vals = [np.mean(self.sample(sims, x, scale)) for x in sampVals]

        else:
            vals = [np.mean(self.sample(sims, x, scale)) for x in self.index.I]

        return vals
        
    def graph(self, sims, idx=None, scale=1):
        if idx is None:
            plt.plot(self.sampleIndex(sims, scale))
        else:
            plt.plot(self.sample(sims, idx, scale))
        plt.show()
