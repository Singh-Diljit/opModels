"""Implement the (Moran-)Gamma process."""

import numpy as np
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Index.Index import *

class GammaProcess:
    """Implement X = {c*G_t} with index set: [0, np.inf]."""

    def __init__(self, mean=False, var=False, rate=1, scale=1, mag=1, index=None):
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
        self.index = Index(0) if index is None else index


    @property
    def initDict(self):
        """Dictionary of inputs to init to self."""
        className = 'GammaProcess'
        initOrder = ['mean', 'var', 'rate', 'scale', 'mag']
        repData = {
            'mean'  : self.mean,
            'var'   : self.var,
            'rate'  : self.rate,
            'scale' : self.scale,
            'mag'   : self.mag}
        
        return className, repData, initOrder

    def __repr__(self):
        """Return repr(self)."""
        className, repData, order = self.initDict
        rep = ', '.join([f'{x}: {repData[x]}' for x in order])
        
        return f'{className}({rep})'
        
    def sample(self, sims, idx, scale=1):
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
        res = np.random.gamma(idx*self.scale, self.rate / self.mag, sims)
        return scale*res
        
    def sampleIndex(self, sims, scale=1):
        if self.index.continuous:
            sampVals = np.linspace(self.index.start,
                               min(max(100, self.index.start), self.index.end),
                               100)
            vals = [np.mean(self.sample(sims, x, scale)) for x in sampVals]

        else:
            vals = [np.mean(self.sample(sims, x, scale)) for x in self.index.I]

        return vals
            
    def graph(self, sims, idx=None, scale=1):
        if idx is None:
            plt.plot(self.sampleIndex(sims, scale))
        else:
            plt.plot(self.sample(sims, idx, scale))
        plt.show()
