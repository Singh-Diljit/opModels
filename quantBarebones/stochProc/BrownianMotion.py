"""Implement Brownian motion with drift."""

import numpy as np

class BMQ:
    """Implement X = {c_1*t + c_2*B_t} with index set: [0, T]."""
    
    def __init__(self, drift=0, mag=1, T=1):
        """Initialize BrownianMotion paramaters.

        Paramaters
        ----------
        drift: float, optional : Drift componenet of the stochastic process.
        mag  : float, optional : Scale of standard Brownian motion.
        T    : float, optional : Upper end-point for index set.

        """
        self.drift = drift
        self.mag = mag
        self.T = T

    def samplePoint(self, sims, t=None):
        """Sample X_t.

        Paramaters
        ----------
        self : BrownianMotion : Stochastic proccess being sampled.
        sims : int            : # of simulations drawn at each point in time.
        t    : float, optional: Provides instance of SP being sampled.

        Returns
        -------
        res : ndarray : Array with 'sims' number of samples. Shape = (sims,)
        
        """
        if t == None:
            t = self.T
        realizeNorm = np.random.normal(scale=np.sqrt(t), size=sims)
        res = self.drift*t + self.mag*realizeNorm
        return res

    def sampleArray(self, sims, times):
        """Draw samples from the stochastic process over a given sub-index set.

        Paramaters
        ----------
        self : BrownianMotion : Stochastic proccess being sampled.
        sims : int            : # of simulations drawn at each point in time.
        times: array_like     : Times SP is sampled over.

        Returns
        -------
        res : ndarray : Drawn samples in shape=(steps, sims));
            row_i = res[i, :] is a single simulation across points in time.
            col_i = res[:, i] is all sumulations at one point in time.
        
        """
        times = np.array(times)
        detProc = np.array([self.drift*times] * sims) if self.drift else 0
        steps = max(times.shape)
        mean = np.zeros(steps)
        cov = np.zeros((steps, steps))
        np.fill_diagonal(cov, self.mag*np.sqrt(times))
        
        diffProc = np.random.multivariate_normal(mean, cov, size=sims)
        
        return detProc + diffProc

    def sampleInterval(self, sims, steps, interval=[0, 1]):
        """Draw samples from the stochastic process over an interval of time.

        Paramaters
        ----------
        self    : BrownianMotion : Stochastic proccess being sampled.
        sims    : int            : # of simulations drawn at each point in time.
        steps   : int            : # of uniform time discretizations.
        interval: array_like, optional : Start and end points of time interval.
        
        Returns
        -------
        res : ndarray : Drawn samples in shape=(steps, sims));
            row_i = res[i, :] is a single simulation across points in time.
            col_i = res[:, i] is all sumulations at one point in time.
        
        """
        T_s, T_e = interval
        return self.sampleArray(sims, np.linspace(T_s, T_e, steps))

    def sample(self, sims,
               t=False,
               times=False,
               steps=1*252, interval=[0, 1]):
        """Sample X_t for a given t, or {X_t} for t \in S.

        Paramaters
        ----------
        self    : BrownianMotion   : Stochastic proccess being sampled.
        sims    : int              : # of simulations drawn at each point in time.
        t       : float, optional  : Provides instance of SP being sampled.
        times   : array_like, optional : Times SP is sampled over.
        steps   : int, optional        : # of uniform time discretizations.
        interval: array_like, optional : Start and end points of time interval.
        
        Returns
        -------
        res : ndarray : Drawn samples in shape=(steps, sims)) or (sims,)
        
        """
        if t:
            res = self.samplePoint(sims, t)
        elif times.all:
            res = self.sampleArray(sims, times)
        else:
            res = self.sampleInterval(sims, steps, interval=[0, self.T])

        return res
