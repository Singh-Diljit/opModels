"""Implement Stock class."""

from Dividend import Dividend, noDiv
from emptyAttributes import noVol, noJump, noCorr, noGamma

class Stock:
    """This class implements stock structure."""
    
    def __init__(self, ticker='GENERIC', S=0,
                 q=noDiv, volData=noVol, sdeData=noCorr,
                 jumpData=noJump, gammaData=noGamma):
        """Initialize a stock.

        Paramaters
        ----------
        ticker   : str,      optional: Stock identifier.
        S        : float,    optional: Spot price.
        q        : Dividend, optional: Dividend.
        volData  : dict,     optional: Volatility related data.
        sdeData  : dict,     optional: SDE __init__ related data.
        jumpData : dict,     optional: Jump process related data.
        gammaData: dict,     optional: Gamma process related data.

        Initializes
        -----------
        ticker   : str      : Stock identifier.
        S        : float    : Spot price.
        q        : Dividend : Dividend.
        volData  : dict     : Volatility related data.
        sdeData  : dict     : SDE __init__ related data.
        jumpData : dict     : Jump process related data.
        gammaData: dict     : Gamma process related data.
        
        """
        self.ticker = ticker
        self.S = S
        self.q = q
        self.volData = volData
        self.sdeData = sdeData
        self.jumpData = jumpData
        self.gammaData = gammaData

    @property
    def initDict(self):
        """Dictionary of lablled inputs for __init__ to this instance."""

        className = 'Stock'
        initOrder = ['ticker', 'S', 'q',
                     'volData', 'sdeData', 'jumpData', 'gammaData'] 
                     
        repData = {'ticker'    : self.ticker,
                   'S'         : self.S,
                   'q'         : repr(self.q),
                   'volData'   : self.volData,
                   'sdeData'   : self.sdeData,
                   'jumpData'  : self.jumpData,
                   'gammaData' : self.gammaData}
        
        return className, repData, initOrder

    def __repr__(self):
        """Representation of the class instance."""

        className, repData, order = self.initDict
        rep = ', '.join([f'{x}: {repData[x]}' for x in order])
        
        return f'{className}({rep})'

    def __str__(self):
        """Return str(self)."""
        return '\n'.join([f'{x}: {repData[x]}' for x in self.inputDict])
