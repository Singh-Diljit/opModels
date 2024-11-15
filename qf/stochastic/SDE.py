"""Implement a one-dimensional SDE, driven by N processess."""

import numpy as np
import matplotlib.pyplot as plt
from Index import Index
from solver.simulateSDE import *
sys.path.append('../')
from helperFuncs import general, formatting, showData

class SDE:
    """dX_t = f*dt + g_1*dP_1 + ... + g_N*dP_N for t in I."""
    def __init__(self, drift, diffusion, dP, seed=0, rho=None, index=None):
        """
        drift     : func with single output.
        diffusion : list of funcs each with single output.
        dP        : list of all driving Levy Proc.
        seed      : float, is the init value.
        rho       : correlation between proc.
        index     : type = Index.
        """
        self.drift = drift
        self.diffusion = formatting.makeCallable(diffusion)
        self.dP = dP
        self.seed = seed
        self.rho = rho
        self.I = Index() if index is None else Index

    @property
    def numProccess(self):
        """Return number of processes driving the system."""
        return len(self.dP)

    @property
    def initData(self):
        """Labled inputs to __init__ to this instance."""
        
        className = 'SDE'
        initData_ = [
            ('drift',     self.drift),
            ('diffusion', self.diffusion),
            ('dP',        self.dP),
            ('seed',      self.seed),
            ('rho',       self.rho),
            ('index',     self.I)
            ]

        return className, initData_

    def __repr__(self):
        """Return repr(self)."""
        return showData.makeRepr(self.initData)
    
    def simulate(self, sims, steps=100, start=None, end=None):
        """Simulate the SDE on a subIndex."""
        idx = self.I.restrict(start, end)
        sampleSet, increments = idx.makeDiscrete(steps=steps)
        singleInc = general.equalStepSize(increments)
        res = simulateSDE(self.drift, self.diff, self.dP, steps,
                          sims, self.seed, sampleSet, increments,
                          singleInc)
        return res

    def graph(self, sims, steps=100, start=None, end=None):
        """Graph simulated paths."""
        paths = self.simulate(sims, steps=100, start=None, end=None)
        pass
        
        
        
