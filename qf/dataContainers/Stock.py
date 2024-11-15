"""Implement Stock class."""

import numpy as np
from scipy.stats.stats import pearsonr
from datetime import datetime
import matplotlib.pyplot as plt
sys.path.append('../')
from heleperFuncs import showData
from Dividend import Dividend

class Stock:
    """This class implements stock structure."""
    
    def __init__(self, ticker='GENERIC', S=1, q=0, vol=0):
        """Initialize a stock.

        Paramaters
        ----------
        ticker   : str      : Stock identifier
        S        : float    : Spot price
        q        : Dividend : Dividend
        volData  : dict     : Volatility related data.

        Initializes
        -----------
        ticker   : str      : Stock identifier.
        S        : float    : Spot price.
        q        : Dividend : Dividend.
        volData  : dict     : Volatility related data.

        
        """
        self.ticker = ticker
        self.S = S
        self.q = q
        self.vol = vol

        self.priceHistory = np.array([])
        self.volHistory = np.array([])
        self.timeLog = np.array([])

    @property
    def calculateVol(self):
        """Return std of stock prices."""
        return np.std(self.priceHistory)

    def update(self, newPrice, newVol=None, timeStamp=None):
        """Update spot price and records the change for historical reference."""
        self.timeLog.append(datetime.now() if timeStamp is None else timeStamp)

        self.S = newPrice
        self.priceHistory.append(self.S)

        self.vol = self.calculateVol if newVol is None else newVol
        self.volHistory.append(self.vol)

    @property
    def logReturns(self):
        return np.diff(np.log(self.price_history))

    @property
    def getJumps(self, threshold=3):
        # Determine jump threshold
        log_returns = self.logReturns
        mean_return = np.mean(log_returns)
        std_dev_return = np.std(log_returns)
        jump_threshold = mean_return + threshold * std_dev_return

        # Identify jumps
        jumps = log_returns[log_returns > jump_threshold]
        return jumps

    @property
    def jumpParams(self, threshold=3):
        """Get jump intensity, avg jump size, vol of jump sizes.

        threshold (in std of daily returns) above which a return is
        considered a jump."""
        jumps = self.getJumps(threshold)
        # Calculate jump parameters
        if len(jumps) == 0:
            print("No significant jumps detected in price history.")
            return {"lambda": 0, "mu_J": 0, "sigma_J": 0}

        jumpIntensity = len(jumps) / len(log_returns)  # Proportion of days with jumps
        avgJumpSize = np.mean(jumps)  # Average jump size
        volJumpSize = np.std(jumps)  # Volatility of jump sizes

        return jumpIntensity, avgJumpSize, volJumpSize

    @property
    def priceVolCorrelation(self):
        """Correlation between price and vol."""
        return pearsonr(self.priceHistory, self.volHistory)

    @property
    def volOfVol(self):
        """Return vol of vol."""
        return np.std(self.volHistory)
        
    @property
    def meanVol(self):
        """Average vol."""
        return np.mean(self.volHistory)
    
    @property
    def longVariance(self):
        """Long-term variance"""
        return np.var(self.volHistory)

    @property
    def graphPrice(self):
        """Plot price history."""
        if not self.priceHistory or not self.timeLog:
            print("No data to plot.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(self.timeLog, self.priceHistory,
                 label=f"{self.ticker} Price", color="blue", marker="o")
        plt.title(f"Price History of {self.ticker}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.legend()
        plt.show()

    @property
    def graphVol(self):
        """Plot vol history."""
        if not self.volHistory or not self.timeLog:
            print("No data to plot.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(self.timeLog, self.volHistory,
                 label=f"{self.ticker} Price", color="blue", marker="o")
        plt.title(f"Vol History of {self.ticker}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.legend()
        plt.show()
        
    @property
    def initData(self):
        """Labled inputs to __init__ to this instance."""
        className = 'Stock'                     
        initData_ = [
            ('ticker', self.ticker),
            ('S',      self.S),
            ('q',      repr(self.q),
            ('vol',    self.volData)
             ]
        
        return className, repData, initOrder

    def __repr__(self):
        """Return repr(self)."""
        return showData.makeRepr(self.initData)

    def __str__(self):
        """Return str(self)."""
        return '\n'.join([f'{x}: {repData[x]}' for x in self.inputDict])
