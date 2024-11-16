"""Implement SDEs driven by arb many ind. Levy proc."""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
from helperFuncs.formatting import paddedVec, wrapList, reduceZero

class SimpleSDE:
    """dX_t = c_1*X_t*dt + arb many SP that are ind."""
    def __init__(self, drift, diffusion, P, seed=1):
        """
        drift     : float
        diffusion : float or array_like of floats
        stochProc : single SP or array_like of SP
        """
        self.drift = drift
        diff_ = paddedVec(diffusion, desiredLen=2)
        P_ = wrapList(P)
        self.diffusion, self.P = reduceZero(diff_, P_)
        self.seed = seed

    @property
    def numProc(self):
        return len(self.diffusion)

    def simulate(self, sims, steps, start=0, end=1):
        dt = (end-start)/steps

        #container for sim paths
        numProc = self.numProc
        X = np.zeros((steps+1, sims)); X[0] = self.seed
        
        #Realize Stoch Procs
        dP = np.zeros((numProc, steps, sims))
        for i, proc in enumerate(self.P):
            dP[i] = proc.sample(sims=steps*sims, idx=dt, shape=(steps, sims))
            dP[i] *= self.diffusion[i]

        dP = dP.sum(axis=0)
        det = self.drift*dt
        for i in range(1, steps+1):
            X[i] = X[i-1]*(1 + det + dP[i-1])

        return X

    def graph(self, sims, steps, start=0, end=1):
        # Time points corresponding to the steps
        time = np.linspace(start, end, steps+1)
        paths = self.simulate(sims, steps, start, end).T
        # Plot the sample paths
        plt.figure(figsize=(10, 6))
        for pathIdx in range(sims):
            plt.plot(time, paths[pathIdx], lw=1)
        
        # Add labels and title
        plt.title(f"Sample Paths of the SDE (Euler–Maruyama, T={end})")
        plt.xlabel("Time")
        plt.ylabel("State Variable")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    from StochProc.BrownianMotion import *
    BM = BrownianMotion()
    test = SimpleSDE(drift=.7, diffusion=2, P=BM)
    test.graph(5, 1000)
    
