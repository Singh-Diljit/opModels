"""Implement exp(X) for X a stochastic process."""

import numpy as np
import matplotlib.pyplot as plt

class Geometric:
    """Implement a*t + b*exp(X) for X_t with index set: [0, np.inf]."""

    def __init__(self, X, drift=0, mag=1, start=0, end=None):
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
        self.drift = drift
        self.mag = mag
        self.X = X
        self.index = X.index if end is None else [start, end]
        
    def sample(self, sims, idx, shape=None):
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
        if shape is None:
            shape = sims
        noise = np.exp(self.X.sample(sims, idx, shape))
        det = 0 if self.drift==0 else self.drift*idx
        return det + self.mag*noise

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
            plt.plot(indexSet, paths[pathidx, :], lw=1,
                     label=f"Sample Path {pathidx + 1}")
        
        # Add labels and legend
        plt.title(f"Sample Paths of exp({self.X.__class__.__name__})")
        plt.xlabel("Index (t)")
        plt.ylabel("Value")
        if numPaths < 6: plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    from BrownianMotion import *
    mu, sigma, S = .1, .3, 100
    T, steps, sims = 1, 100, 100
    drift = (mu - 0.5 * sigma**2)
    bm = BrownianMotion(drift=drift, mag=sigma)
    gbm = Geometric(bm, mag=S, end=T)
    
    # Generate and graph sample paths
    gbm.graph(sims, steps)
