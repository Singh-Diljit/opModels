"""Implement the (Moran-)Gamma process."""

import numpy as np
import matplotlib.pyplot as plt

class GammaProcess:
    """Implement X = {drift*t + c*G_t} with index set: [0, np.inf]."""

    def __init__(self, theta, lam, drift=0, mag=1, start=0, end=1):
        """Initialize GammaProcess paramaters."""
        self.theta = theta #shape or mean rate
        self.lam = lam
        self.drift = drift
        self.mag = mag
        self.index = [start, end]
        
    def sample(self, sims, idx, shape=None):
        """Sample X_t.

        Paramaters
        ----------
        sims  : int   : # of simulations drawn at each point in time.
        idx   : float : Provides instance of SP being sampled.

        Returns
        -------
        res : ndarray : Array with 'sims' number of samples.
        
        """
        if shape is None:
            shape = sims
            
        noise = np.random.gamma(self.theta*idx, scale=1/self.lam, size=shape)
        struc = idx
        return self.drift*struc + self.mag*noise
        
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
    G = GammaProcess(theta=2, lam=1, end=5)
    G.graph(numPaths=5)
