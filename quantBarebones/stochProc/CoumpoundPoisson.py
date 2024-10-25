"""Implement a coumpound Poisson process with lognormal jumps."""

import numpy as np

class CoumpoundPoisson:
    """Implement X = {c*J_t} with index set: [0, T]."""

    def __init__(self, rate, rateInter=1,
                 logNormMean=0, logNormDev=1,
                 mag=1, T=1):
        """Initialize CoumpoundPoisson paramaters.

        Paramaters
        ----------
        rate       : float           : Rate (intensity) of the Poisson process.
        rateInter  : float, optional : Length  of time the rate is given in.
        logNormMean: float, optional : Mean of log(Jumps).
        logNormDev : float, optional : Standard deviotion of log(Jumps).
        mag        : float, optional : Scale of stochastic process.
        T          : float, optional : Upper end-point for index set.

        """
        self.lam = rate / rateInter
        self.logNormMean = logNormMean
        self.logNormDev = logNormDev
        self.mag = mag
        self.T = T

    def sample(self, sims, t):
        """Sample X_t.

        Paramaters
        ----------
        self : CoumpoundPoisson: Stochastic proccess being sampled.
        sims : int             : # of simulations drawn at each point in time.
        t    : float, optional : Provides instance of SP being sampled.

        Returns
        -------
        res : ndarray : Array with 'sims' number of samples.
        
        """
        realizePoisson = np.random.poisson(self.lam*t, sims)
        realizeJumps = np.random.lognormal(self.logNormMean, self.logNormDev,
                                           size=np.sum(realizePoisson))
        res = np.ones(sims) * self.mag
        idx = 0
        for i, k in enumerate(realizePoisson):
            res[i] *= np.sum(realizeJumps[idx: idx+i])
            idx += k

        return res
