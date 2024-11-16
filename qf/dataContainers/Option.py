import numpy as np
import matplotlib.pyplot as plt
from param import *

import sys
sys.path.append('../')
from helperFuncs import showData

class Option:
    def __init__(self, 
                 stock, 
                 strike,
                 maturity,
                 rate,
                 payOff='European', 
                 call=True):

        self.stock = stock
        self.strike = strike
        self.rate = rate
        self.maturity = maturity
        self.payOff = payOff.lower()
        self.call = call; self.put = not self.call

    @property
    def initData(self):
        """Labled inputs to __init__ to this instance."""
        className = 'Option'
        #_, initData_ = self.stock.initData
        initData_ = [
            ('strike',   self.strike),
            ('rate',     self.rate),
            ('maturity', self.maturity),
            ('payOff',   self.payOff),
            ('call',     self.call),
            ]
        
        return className, initData_
        
    def __repr__(self):
        """Return repr(self)"""
        return showData.makeRepr(self.initData)

    def loadParams(self, paramSet):
        vals = {'S'   :  self.stock.S,
                'K'   :  self.strike,
                'r'   :  self.rate,
                'T'   :  self.maturity,
                'vol' :  self.stock.vol,
                'q'   :  self.stock.q,
                'call':  self.call}
        
        res = {x: vals[x] for x in paramSet}
        return res

    def price(self, model, tech=None):
        """Return the price."""
        if tech is None:
            tech = model.default
        inputDict = self.loadParams(model.getParams(tech))
        return model.closedForm(**inputDict)
