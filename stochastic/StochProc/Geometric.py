"""Implement exp(X) for X a stochastic process."""

import numpy as np
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Index.Index import *

class Geometric:
    """Implement K*exp(X) for stoch. process X with index set: [0, np.inf]."""

    def __init__(self, X, mag=1):
        """Initialize JumpDiffusion paramaters.

        Paramaters
        ----------
        X   : StochasticProcess : Process being exponatiated.
        mag : float             : Scale of exp(X).

        Initializes
        -----------
        self.X   : float : Stochastic process to exponentiate.
        self.mag : float : cale of exp(X).

        """
        self.X = X
        self.mag = mag
        self.index = X.index

    @property
    def initDict(self):
        """Dictionary of inputs to init to self."""
        className = 'Geometric'
        XData = X.initDict
        initOrder = XData[3]
        repData = X.initDict.add() #add mag to this
        repData = {
            'X'   : self.mean,
            'mag' : self.var}
        
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
        res = self.mag * np.exp(self.X.sample(sims, idx))
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
