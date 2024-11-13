"""Implement Brownian Motion with drift + coumpound Poisson (lognormal jumps)."""

import numpy as np
from BrownianMotion import BrownianMotion
from CompoundPoisson import CompoundPoisson

import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Index.Index import *

class JumpDiffusion:
    """Implement X = {c_1*t + c_2*B_t + c_3*J_t} with index set: [0, T].

    Notes
    -----
    B_t - Standard Brownian motion
    J_t - coumpound Poisson (lognormal jumps)
    B_t and J_t are assumed to be independant
    
    """

    def __init__(self, BM, JP):
        """Initialize JumpDiffusion paramaters.

        Paramaters
        ----------
        BM : BrownianMotion   : Rate (intensity) of the Poisson process.
        JP : CoumpoundPoisson : Length  of time the rate is given in.

        """
        self.BM = BM
        self.JP = JP
        self.index = BM.index.intersection(JP.index)

    def sample(self, sims, idx, scale=1):
        """Sample X_t.

        Paramaters
        ----------
        self : JumpDiffusion  : Stochastic proccess being sampled.
        sims : int            : # of simulations drawn at each point in time.
        t    : float, optional: Provides instance of SP being sampled.

        Returns
        -------
        res : ndarray : Array with 'sims' number of samples.
        
        """
        return scale*self.BM.sample(sims, idx) + scale*self.JP.sample(sims, idx) 
        
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

I = Index(0, 1)
BM = BrownianMotion(0, 1, I)
BM.graph(sims=1000)

gBM = Geometric(BM)
gBM.graph(sims=1000)
