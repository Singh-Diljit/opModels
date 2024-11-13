"""Implement Brownian motion with drift."""

import numpy as np
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Index.Index import *

class BrownianMotion:
    """Implement X = {c_1*t + c_2*B_t} with index set: [0, np.inf]."""

    def __init__(self, drift=0, mag=1, index=None):
        """Initialize BrownianMotion paramaters.

        Paramaters
        ----------
        drift : float : Drift componenet of the stochastic process.
        mag   : float : Scale of standard Brownian motion.

        Initializes
        -----------
        self.drift : float : Drift componenet of the stochastic process.
        self.mag   : float : Scale of standard Brownian motion.

        """
        self.drift = drift
        self.mag = mag
        self.index = Index(0) if index is None else index

    def __repr__(self):
        """Return repr(self)."""
        repData = f'drift={self.drift}, mag={self.mag}, index={repr(self.index)}'
        return f'BrownianMotion({repData})'
    
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
        realizeNorm = np.random.normal(scale=np.sqrt(idx), size=sims)
        res = self.drift*idx + self.mag*realizeNorm
        return scale*res

    def sampleIndex(self, sims, scale=1):
        if self.index.continuous:
            sampVals = np.linspace(self.index.start, self.index.end, 1000)
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
