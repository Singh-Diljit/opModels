"""Implement Dividend class."""

import numpy as np
import divHelper as divH

class Dividend:
    """This class implements dividend structure."""
    
    def __init__(self, div, discrete=None,
                 times=None, dates=None, startDate='today'):
        """Initialize a dividend.

        Parameters
        ----------
        div       : array_like, float : Discrete payments or continuous yield.
        times     : array_like : Ascending times, in years, until disbursements.
        dates     : array_like : Dates of future disbursements.
        startDate : date_like  : Start date.
        life      : float      : Time dividend is modeled for.
        
        Initializes
        -----------
        self.disc   : bool        : Dividend payouts are discrete.
        self.cont : bool        : Dividend payouts are continuous.
        self.div        : array, float: Continuous yield or discrete payments.
        self.times      : array       : Ascending time until disbursements.

        Notes
        -----
        For defination of array_like, see documentation of numpy.

        For definition of date_like, see this project's time module. Generally,
        ISO8601 compliant strings are accepted, in addition to all other forms
        accepted by numpy's datetime64 module. For more robust input options
        see parseDate function in time.offline, not implemented due to speed
        concerns when processing many date_like arguments.

        """
        self.disc, self.div = divH.extractDiv(div, discrete, times, dates)
        self.cont = not(self.disc)
        if self.disc and (times is None) and (dates is None):
            raise Exception('Payment dates needed.')
        self.times = divH.getTimes(self.disc, times, dates, startDate)

    @property
    def discrete(self):
        return self.disc

    @property
    def continuous(self):
        return self.cont

    @property
    def type(self):
        """Return, as a string, if dividend is continuous or discrete."""
        return 'discrete' if self.discrete else 'continuous'

    def discount(self, r=0, T=1):
        """Return discounted payouts. (Not generally the present value).

        Parameters
        ----------
        r : float : Annualized risk-free interest rate, continuously compounded.
        T : float : Time, in years, until maturity.

        Returns
        -------
        res : func : Discounted dividend.

        """
        if self.discrete:
            res = np.sum(np.exp(-r * self.times) * self.div)
        else:
            res = np.exp(-self.div * T)
            
        return res

    def presentValue(self, PV=1, r=0, T=1):
        """Return the present value."""
        if self.discrete:
            res = np.sum(np.exp(-r * self.times) * self.div)
        else:
            res = PV*(np.exp((self.div-r)*T) - 1)
            
        return res

    @property
    def numberPayments(self):
        """Return the number of disbursements."""
        return np.inf if self.continuous else len(self.div)

    @property
    def maxDiv(self):
        """Return the maximum dividend payment."""
        return self.div if self.continuous else np.max(self.div)

    @property
    def rate(self):
        """Return the continuous dividend yield (estimate if needed).

        Returns
        -------
        res : float : Possibly estimated continuous dividend yield.

        Notes
        -----
        If dividend disbursement is given discreetly, the rate is estimated
        over the life of the dividend-model.

        Estimation is sensitive to data given, for best results include full
        data (until year end for last included date).
       
        """
        if self.discrete:
            range_ = self.times[-1] - self.times[0]
            if range_ == 0:
                range_ = self.times[0]
                
        res = self.div if self.continuous else np.sum(self.div) / range_
        return res

    @property
    def initDict(self):
        """Dictionary of inputs to init to self."""
        className = 'Dividend'
        initOrder = ['type', 'div', 'times']
        repData = {
            'type'     : self.type,
            'div'      : self.div,
            'times'    : self.times}
        
        return className, repData, initOrder

    def __repr__(self):
        """Return repr(self)."""
        className, repData, order = self.initDict
        if self.continuous: order.pop()
        rep = ', '.join([f'{x}: {repData[x]}' for x in order])
        
        return f'{className}({rep})'

    def __str__(self):
        """Return str(self)"""
        if self.discrete:
            res = f'Payments of: {self.div} \nDisbursed in {self.times} years.'
        else:
            res = f'Continuous dividend rate of {self.rate}.'
            
        return res
