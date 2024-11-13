"""testDiv"""

"""Implement (a minimal) Dividend class."""

import numpy as np

"""
q.discrete  : bool        : Dividend payouts are discrete.
q.continous : bool        : Dividend payouts are continous.
q.div       : array, float: Continous yield or discrete payments.
q.times     : array       : Ascending time until disbusrements.
--
q.discount       : float  : Div payouts time-rate discounted
q.numberPayments : int/inf: Number of payment
q.maxDiv         : float  : Either max div or div if continous
q.total          : float  : Total payout of div
"""
class minimalDiv:
    def __init__(self, div, times=np.inf, cont=True):
        """
        Paramaters
        ----------
        div   : array, float : Payments  
        times : array : Time, in years, until disbusrements dates (ascending)
        cont  : bool  : If cont. or discrete payments

        """
        self.discrete = not cont
        self.continous = cont
        self.div = div
        self.times = times

    #PORTED
    def discount(self, r=0, T=1):
        if self.discrete:
            res = np.sum(np.exp(-r * self.times) * self.div)
        else:
            res = np.exp(-self.div * T)
        return res

    #PORTED
    @property
    def numberPayments(self):
        return np.inf if self.continous else len(self.div)

    #PORTED        
    @property
    def maxDiv(self):
        return self.div if self.continous else np.max(self.div)

    #PORRTED
    def total(self, PV=1, T=1):
        if self.continous:
            res = PV * (np.exp(self.div * T) - 1)
        else:
            res = np.sum(self.div)
        return res

