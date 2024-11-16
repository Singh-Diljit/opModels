"""Implement Brownian motion with drift."""

import numpy as np
import matplotlib.pyplot as plt

class BrownianMotion:
    """Implement X = {c_1*t + c_2*B_t} with index set: [start, end]."""

    def __init__(self, drift=0, mag=1, start=0, end=1):
        """Initialize BrownianMotion paramaters."""
        self.drift = drift
        self.mag = mag
        self.index = [start, end]

    def __repr__(self):
        """Return repr(self)."""
        repData = f'drift={self.drift}, mag={self.mag}, index={repr(self.index)}'
        return f'BrownianMotion({repData})'
    
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
        noise = np.random.normal(loc=0.0, scale=np.sqrt(idx), size=shape)
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
    # Create a BrownianMotion instance
    bm = BrownianMotion(drift=0.1, mag=0.2)
    print(bm != 0)
    # Generate and graph sample paths
    #bm.graph(numPaths=5)
