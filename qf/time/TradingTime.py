"""Implement TradingTime class."""

from numpy import datetime64 as dt64
import datetime as dt
import fastCalander
from calander import dt64_tuple, dateToDay
import timeDicts

class TradingTime:
    """This class implements trading time structure."""

    def __init__(self, date):
        """Initialize trading time.

        Paramaters
        ----------
        time: datetime64_like: Marker for time to initialize.

        Initializes
        -----------
        date: datetime64: Orginal input.
        ical: int       : Enumeration of date since 1/1/2000.
        n   : int       : Represents trading day following or on date.

        Notes
        -----
        See np.datetime64 documentation for full range of accepted inputs.
        
        """
        self.date = dt64(date)
        self.ical = self.date - fastCalander.startD
        self.n = fastCalander.enumDate(self.date)
        self.day, self.month, self.year = calander.dt64_tuple(self.date)

    @property
    def dayOfWeek(self):
        return calander.dateToDay

    @property
    def TradingDay(self):
        """Return if full or partial trading day."""
        return fastCalander.isTradingDay

    @property
    def partialTradingDay(self):
        """Return if full or partial trading day."""
        return not self.fullTradingDay

    def __sub__(self, X):
        """Return self.time - X, for X a trading day or time in years."""
        if type(X) == 'TradingTime':
            res = ... #answer is time in years
        else:
            res = TradingTime()
            
        return res

    def __add__(self, X):
        """Return X + self.time, for X a trading day or time in years."""
        if type(X) == 'TradingTime':
            res = ... #answer is time in years
        else:
            res = TradingTime()
            
        return res

    def __sub__(self, X):
        """Return self.time + X, for X a trading day or time in years."""
        return self.__add__(X)

    def exceptions(self, Y):
        """Return all exceptions interval: [self.time, Z]; Z = Y or X + Y."""
        pass 

    def trYears(self, arr):
        """Return an array of time in years from self.time to times in arr."""
        return np.array([X - self.time for X in arr])

    @property
    def fracYear(self):
        """Return the fraction of the trading year elapsed by self.time."""
        return fastCalander.oneDay(self.ical, T)

    def oneDay(self, T):
        """Return portion of time from [date, date+T] one day is."""
        return fastCalander.oneDay(self.ical, T)

    def __rsub__(self, X):
        """Return X - self.time, for X a trading day or time in years."""
        if type(X) == 'TradingTime':
            res = ... #answer is time in years
        else:
            res = TradingTime()
            
        return res

    @property
    def initDict(self):
        """Dictionary of lablled inputs for __init__ to this instance."""

        className = 'TradingTime'
        initOrder = ['time']                 
        repData = {'time' : self.time}
    
        return className, repData, initOrder

    def __repr__(self):
        """Representation of the class instance."""
        
        className, repData, order = self.initDict
        rep = ', '.join([f'{x}: {repData[x]}' for x in order])
        return f'{className}({rep})'

    def __str__(self):
        """Return str(self)."""
        return '\n'.join([f'{x}: {repData[x]}' for x in self.inputDict])
