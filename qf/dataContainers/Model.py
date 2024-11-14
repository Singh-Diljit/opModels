"""Implement Model class."""

class Model:
    def __init__(self, phi=False, stochProc=False, stochDiffEq=False,
                 priceMults=False, probMults=False,
                 analytic=False, params=False, defaultMethod=False):
        """
        phi       : func      : char func
        X         : StochProc : proc
        dX        : sSDE      : dX
        priceMults: func      : priceJumps in Tree (ordered inc)
        probMults : func      : prob of each price Jump
        analytic  : func      : If analytic formula
        lattice   : func      : Tree pricing
        params    : list      : Ordered list of titles of params
        """
        self.phi = phi
        self.X = stochProc
        self.dX = stochDiffEq

        self.priceMults = priceMults
        self.probMults = probMults

        self.analytic = analytic
        self.lattice = False
        self.params = params
        self.defaultMethod = defaultMethod

    @property
    def pricingTech(self):
        techs = []
        if self.analytic:
            techs += ['Closed Form']
        if self.lattice:
            techs += ['Lattice']
        if self.phi:
            techs += ['FFT', 'Direct Integration']
        if self.dX:
            techs += ['Monte-Carlo SDE']
        if self.X:
            techs += ['Monte-Carlo S_t']
            
        return techs

    def defaultTech(self):
        if not self.defaultMethod:
            return self.pricingTech[0]
        else:
            return self.defaultMethod

