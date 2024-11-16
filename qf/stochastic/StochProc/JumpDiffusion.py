"""Implement Brownian Motion with drift + coumpound Poisson (lognormal jumps)."""

import numpy as np
import matplotlib.pyplot as plt
from BrownianMotion import *
from CompoundPoisson import *

class JumpDiffusion:
    """Implement X = {c_1*t + c_2*B_t + c_3*J_t} with index set: [0, T]."""

    def __init__(self, magBM, lam, logNormMean=0, logNormDev=1,
                 drift=0, magJP=1, start=0, end=1):
        """Initialize JumpDiffusion paramaters.

        Paramaters
        ----------
        BM : BrownianMotion   : Rate (intensity) of the Poisson process.
        JP : CoumpoundPoisson : Length  of time the rate is given in.

        """
        self.drift = drift
        self.BM = BrownianMotion(mag=magBM, start=start, end=end)
        self.JP = CompoundPoisson(lam, logNormMean, logNormDev,
                                  mag=magJP, start=0, end=1)
        self.index = [start, end]

    def sample(self, sims, idx, shape=None):
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
        if shape is None:
            shape = sims
        noise = self.BM.sample(sims, idx, shape)
        jumps = self.JP.sample(sims, idx, shape)
        return self.drift*idx + noise + jumps
        
    def graph(self, numPaths=1, steps=100):
        """Plot multiple sample paths of the stochastic process."""
        plt.figure(figsize=(10, 6))
        indexSet = np.linspace(self.index[0], self.index[1], steps)
        paths = np.zeros((numPaths, len(indexSet)))

        # Generate samples for each time point
        for i, t in enumerate(indexSet):
            samples = self.sample(sims=numPaths, idx=t)
            paths[:, i] = samples
        
        # Plot each path
        for pathidx in range(numPaths):
            plt.plot(indexSet, paths[pathidx, :],
                     label=f"Sample Path {pathidx + 1}")
        
        # Add labels and legend
        plt.title(f"Sample Paths of {self.__class__.__name__}")
        plt.xlabel("Index (t)")
        plt.ylabel("Value")
        plt.legend()
        plt.grid()
        plt.show()

if __name__ == "__main__":
    jd = JumpDiffusion(drift=.1, magBM=.2, lam=.5)
    jd.graph(numPaths=5)
