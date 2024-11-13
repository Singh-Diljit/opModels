"""Implement a compound Poisson process with lognormal jumps."""

import numpy as np
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Index.Index import *

class CompoundPoisson:
    """Implement X = {c*J_t} with index set: [0, np.inf]."""

    def __init__(self, rate, rateInter=1, logNormMean=0, logNormDev=1, mag=1,
                 index=None):
        """Initialize CompoundPoisson paramaters.

        Paramaters
        ----------
        rate        : float : Rate (intensity) of the Poisson process.
        rateInter   : float : Length  of time the rate is given in.
        logNormMean : float : Mean of log(Jumps).
        logNormDev  : float : Standard deviotion of log(Jumps).
        mag         : float : Scale of stochastic process.

        """
        self.rate = rate
        self.rateInter = rateInter
        self.lam = rate / rateInter
        
        self.logNormMean = logNormMean
        self.logNormDev = logNormDev
        self.mag = mag
        self.index = Index(0) if index is None else index


    @property
    def initDict(self):
        """Dictionary of inputs to init to self."""
        className = 'CompoundPoisson'
        initOrder = ['rate', 'rateInter', 'logNormMean', 'logNormDev', 'mag']
        repData = {
            'rate'        : self.rate,
            'rateInter'   : self.rateInter,
            'logNormMean' : self.logNormMean,
            'logNormDev'  : self.logNormDev,
            'mag'         : self.mag}
        
        return className, repData, initOrder

    def __repr__(self):
        """Return repr(self)."""
        className, repData, order = self.initDict
        rep = ', '.join([f'{x}: {repData[x]}' for x in order])
        
        return f'{className}({rep})'

    def sample(self, sims, idx, scale=1):
        """Sample X_t.

        Paramaters
        ----------
        sims  : int   : # of simulations drawn at each point in time.
        idx   : float : Provides instance of SP being sampled.
        scale : float : End scaling of samples.

        Returns
        -------
        res : ndarray : Array with 'sims' number of samples. Shape = (sims,)
        
        """
        realizePoisson = np.random.poisson(self.lam*idx, sims)
        realizeJumps = np.random.lognormal(self.logNormMean, self.logNormDev,
                                           size=np.sum(realizePoisson))
        res = np.ones(sims) * self.mag
        idx = 0
        for i, k in enumerate(realizePoisson):
            res[k] *= np.sum(realizeJumps[idx: idx+k])
            idx += k

        return scale*res
        
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
