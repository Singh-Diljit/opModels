"""Implement a Variance-Gamma process with deterministic component."""

import numpy as np
import matplotlib.pyplot as plt
from GammaProcess import *
from BrownianMotion import *

class VarianceGamma:
    """Implement X_t = {a*t  + b*VG_t} with index set: [0, T]."""

    def __init__(self, magGamma, theta, lam,
                 magBM, drift=0, magVG=1, start=0, end=1):
        """Initialize VarianceGammas paramaters."""
        self.GP = GammaProcess(theta, lam, mag=magGamma, start=start, end=end)
        self.BM = BrownianMotion(mag=magBM, start=start, end=end)
        self.drift = drift
        self.magVG = magVG
        self.index = [start, end]

    def sample(self, sims, idx, shape=None):
        """Sample X_t."""
        if shape is None:
            shape = sims
        gammaTimes = self.GP.sample(sims, idx, shape)
        BMvals = self.BM.sample(sims, gammaTimes, shape)
        return self.drift*idx + self.magVG*(BMvals + gammaTimes)
        
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
        if numPaths<5: plt.legend()
        plt.grid()
        plt.show()

if __name__ == "__main__":
    vg = VarianceGamma(magGamma=.1, theta=1, lam=.2, magBM=.2)
    vg = VarianceGamma(magGamma=.07, theta=.21, lam=.15, magBM=.05, end=5)
    vg.graph(numPaths=50)
