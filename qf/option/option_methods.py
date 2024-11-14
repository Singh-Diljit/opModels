"""Methods needed for the option class."""

class Option:
    def __init__(self, ...):

    @property
    def paramDict(self):
        #how to get val??
        res = {p: val for p in params.totalParams}
        return res
        
    def getParams(self, paramList):
        """Return [option.p for p in paramList]."""
        return [self.paramDict[p] for p in paramList]

    def phi(self, M):
        """Return Characteristic function (fixed stock-related paramaters).
        M - A model with phi.
        """
        reqP = self.getParams(M.params['phi'])
        return lambda reqP: model.phi(*reqP)

    #repeat this func for other common greeks
    def phiVol(self, M):
        """Return Characteristic function (all but vol fixed)."""
        reqP = self.getParams(M.params['phiVol'])
        return lambda reqP: model.phiVol(*reqP)

    def genPhi(self, M, greek):
        """greek - str"""
        if greek = 'vega': res = phiVol
        elif greek = 'delta': res = phiS
        ...
        return res

    def type(self):
        put or call

    def cost(self):
        current cost of option

    def price/delta/IV(self, M, extraInputs, method=False):
        """method = False means use M.defaultMethod
        method : str : FFT, MCM SP, MCM SDE, analytic, integrate phi.
        extraInputs e.g. sims
        """
        F = getTech[M, method]
        reqP = techParams[F.__name__]
        op_Params = self.getParams(reqP)
        model_Params = M.getParams(reqP)
        totParams = paramOrder(reqP, op_Params, model_Params, extraInputs)
        return F(totParams)
        




    def __init__(self, stock, K, r, T, payOff, startDate=()):
        self.stock = stock
        self.strike = K
        self.rate = r
        self.time = T
        self.payOff = payOff
        self.payOffType = payOff.__name__
        self.now = False if not startDate else parseDate(startDate)
        if self.now and not self.stock.div.startDate:
            self.stock.div.startDate = self.now
        self.call = True if self.payOffType == 'call' else False
        
    @property
    def unload(self):
        return [self.strike, self.rate, self.time, self.payOffType, self.now]
    
    def __repr__(self):
        """Representation of the class instance."""
        repData = {'Stock' : self.stock.ticker,
                   'Spot Price' : self.stock.price,
                   'Strike' : self.strike,
                   'Rate' : self.rate,
                   'Dividend' : self.stock.div,
                   'Volatility' : self.stock.vol,
                   'Time' : self.time,
                   'Var Reversion Rate' : self.stock.rateVar,
                   'Long Var' : self.stock.longVar,
                   'Vol of Vol' : self.stock.volVol,
                   'Pay Off Type' : self.payOffType}

        rep = ', '.join([f'{x}: {repData[x]}' for x in repData])
        return f'Option({rep})'

    def __str__(self):
        """Return str(self)."""
        repData = {'Stock' : self.stock.ticker,
                   'Spot Price' : self.stock.price,
                   'Strike' : self.strike,
                   'Rate' : self.rate,
                   'Dividend' : self.stock.div,
                   'Volatility' : self.stock.vol,
                   'Time' : self.time,
                   'Var Reversion Rate' : self.stock.rateVar,
                   'Long Var' : self.stock.longVar,
                   'Vol of Vol' : self.stock.volVol,
                   'Pay Off Type' : self.payOffType}

        return '\n'.join([f'{x}: {repData[x]}' for x in repData])
        
