"""Implement Brownian Motion with drift + coumpound Poisson (lognormal jumps)."""

import numpy as np
from BrownianMotion import BrownianMotion
from CoumpoundPoisson import CoumpoundPoisson

class JumpDiffusion:
    """Implement X = {c_1*t + c_2*B_t + c_3*J_t} with index set: [0, T].

    Notes
    -----
    B_t - Standard Brownian motion
    J_t - coumpound Poisson (lognormal jumps)
    B_t and J_t are assumed to be independant
    
    """

    def __init__(self, BM, JP, T=1):
        """Initialize JumpDiffusion paramaters.

        Paramaters
        ----------
        BM : BrownianMotion   : Rate (intensity) of the Poisson process.
        JP : CoumpoundPoisson : Length  of time the rate is given in.
        T  : float, optional  : Upper end-point for index set.

        """
        self.BM = BM
        self.JP = JP
        self.T = T

    def sample(self, sims, t):
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
        return self.BM.sample(sims, t) + self.JP.sample(sims, t) 

bm = BrownianMotion()
a = CoumpoundPoisson(2)   
b = JumpDiffusion(bm, a)
print(b.sample(sims=10, t=5))
