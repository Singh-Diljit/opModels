"""Implement a compound Poisson process with lognormal jumps."""

import numpy as np
import matplotlib.pyplot as plt

class CompoundPoisson:
    """Implement X = {drift*t + mag*Y_t} with index set: [0, np.inf]."""

    def __init__(self, lam, logNormMean=0, logNormDev=1,
                 drift=0, mag=1, start=0, end=1):
        self.lam = lam
        self.logNormMean = logNormMean
        self.logNormDev = logNormDev
        self.drift = drift
        self.mag = mag
        self.index = [start, end]

    def __repr__(self):
        """Return repr(self)."""
        repData1 = f'lam={self.lam}, logNormMean={self.logNormMean}, logNormDev={self.logNormDev}'
        repData2 = f'drift={self.drift}, mag={self.mag}, index={repr(self.index)}'
        
        return f'CompoundPoisson({repData1}, {repData2})'

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

        realizePoisson = np.random.poisson(lam=self.lam*idx, size=sims)
        realizeJumps = np.random.lognormal(
            mean=self.logNormMean,
            sigma=self.logNormDev,
            size=np.sum(realizePoisson)
            )
        
        noise = np.zeros(sims)
        prev = 0
        for i, N_t in enumerate(realizePoisson):
            noise[i] = np.sum(realizeJumps[prev:prev+N_t])
            prev += N_t

        noise = noise.reshape(shape)
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
    J = CompoundPoisson(drift=1, mag=2, lam=.5)
    J.graph(numPaths=5)
