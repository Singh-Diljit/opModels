"""Implement the (Moran-)Gamma process."""

import numpy as np

class GammaProcess:
    """Implement X = {c*G_t} with index set: [0, T]."""

    def __init__(self, mean=False, var=False,
                 rate=1, scale=1,
                 mag=1, T=1):
        """Initialize GammaProcess paramaters.

        Paramaters
        ----------
        rate  : float, optional : Rate of jump arrivals.
        scale : float, optional : Scaling paramater (inverse to jump size). 
        mean  : float, optional : 
        var   : float, optional : 
        mag   : float, optional : Scale of stochastic process.
        T     : float, optional : Upper end-point for index set.

        """
        if mean and var:
            mean_, var_ = mean, var
            scale_ = mean / var
            rate_ = mean * scale_
            
        else:
            scale_, rate_ = scale, rate
            var_ = 1 / rate
            mean_ = scale * var_
            
        self.mean = mean_
        self.var = var_
        self.rate = rate_
        self.scale = scale_
        self.mag = mag
        self.T = T
        
    def sample(self, sims, t):
        """Sample X_t.

        Paramaters
        ----------
        self : GammaProcess    : Stochastic proccess being sampled.
        sims : int             : # of simulations drawn at each point in time.
        t    : float, optional : Provides instance of SP being sampled.

        Returns
        -------
        res : ndarray : Array with 'sims' number of samples.
        
        """
        return np.random.gamma(t*self.scale, self.rate / self.mag, sims)
        
a = GammaProcess()
print(a.sample(sims=10, t=1))
