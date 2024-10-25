"""Implement exp(X) for X a stochastic process."""

import numpy as np

class GeoQ:
    """Implement K*exp(X) for X a stochastic process with index set: [0, T]."""

    def __init__(self, X, mag=1):
        """Initialize JumpDiffusion paramaters.

        Paramaters
        ----------
        X  : StochasticProcess : Process being exponatiated.
        mag: float, optional   : Scale of exp(X).

        """
        self.X = X
        self.mag = mag
        self.T = X.T

    def sample(self, sims, t=1):
        """Sample K*exp(X_t) at point t.

        Paramaters
        ----------
        self    : Geometric  : Stochastic proccess being sampled.
        sims    : int              : # of simulations drawn at each point in time.
        t       : float, optional  : Provides instance of SP being sampled.
        
        """
        return self.mag * np.exp(self.X.sample(sims=sims, t=t))
