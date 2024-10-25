"""Implement Dividend class."""

import numpy as np
import dividendHelper as divH

class Dividend:
    """This class implements dividend structure."""
    
    def __init__(self, div, times=[], dates=[], startDate='today', life=np.inf):
        """Initialize a dividend.

        Paramaters
        ----------
        div      : array_like, float   : Discrete payments or ontinous yield.
        times    : array_like, optional: Ascending time until disbusrements.
        dates    : array_like, optional: Dates of future disbursements.
        startDate: date_like , optional: Determines time until disbursements.
        life     : float     , optional: Time dividend is modelled for.
        
        Initializes
        -----------
        self.discrete  : bool        : Dividend payouts are discrete.
        self.continous : bool        : Dividend payouts are continous.
        self.div       : array, float: Continous yield or discrete payments.
        self.payTimes  : array       : Ascending time until disbusrements.
        self.life      : float       : Time dividend is modelled for.

        Notes
        -----
        For defination of array_like, see documentation of numpy.

        For defination of date_like, see this projects time module. Generally,
        ISO8601 complaint strings are accepted, in addition to all other forms
        accepted by numpy's datetime64 module. For more robust input options
        see parseDate function in time.offline, not implemented due to speed
        concerns when proccessing many date_like arguments.
        
        """
        self.discrete, self.continous = divH.resolve_DiscCont(div, times, dates)
        self.div = div if self.continous else np.array(div)
        if self.discrete and not np.any(self.div):
            self.cont_, self.dis_ = True, False #functionaly these things)
            self.div_ = 0
        self.times = np.array(times)
        #self.life = life
        #self.payTimes = divH.makePayTimes(self.discrete, times,
        #                                  dates, startDate)

    def discount(self, r=0, T=1):
        if self.discrete:
            res = np.sum(np.exp(-r * self.times) * self.div)
        else:
            res = np.exp(-self.div * T)
        return res

    @property
    def numberPayments(self):
        return np.inf if self.continous else len(self.div)
            
    @property
    def maxDiv(self):
        return self.div if self.continous else np.max(self.div)

    def total(self, PV=1, T=1):
        if self.continous:
            res = PV * (np.exp(self.div * T) - 1)
        else:
            res = np.sum(self.div)
        return res

    ##EXTRA UNTESTED USELES??
    @property
    def type(self):
        """Return, as a string, if dividend is continous or discete."""
        return 'discrete' if self.discrete else 'continous'
    
    @property
    def rate(self):
        """Return the continous dividend yield.

        Returns
        -------
        res : float : Continous dividend yield, possibly estimated.

        Notes
        -----
        If dividend disbursement is given discretely, this rate is estimated
        using over the life of the dividend-model.

        Estimation is sensative to data given, for best results include full
        years of data.
        
        """
        res = self.div if self.continous else np.sum(self.div) / self.life
        return res


    ##EXTRA UNTESTED
    @property
    def initDict(self):
        """Dictionary of lablled inputs for __init__ to this instance."""

        className = 'Dividend'
        initOrder = ['type', 'div', 'payTimes', 'life']
        repData = {
            'type'     : self.type,
            'div'      : self.div,
            'payTimes' : self.payTimes,
            'life'     : self.life}
        
        return className, repData, initOrder

    def __repr__(self):
        """Representation of the class instance."""

        className, repData, order = self.initDict
        rep = ', '.join([f'{x}: {repData[x]}' for x in order])
        
        return f'{className}({rep})'

    def __str__(self):
        """Return str(self)"""
        if self.discrete:
            res = f'Payments of: {self.div} \nDisbursed in {self.payTimes} years.'
        else:
            res = f'Continous dividend rate of {self.rate}.'
            
        return res
