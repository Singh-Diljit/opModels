"""Implement Model class."""

#from params import techEvals
import sys
sys.path.append('../')
from helperFuncs import showData

class Model:
    def __init__(self,
                 name,
                 phi=None,
                 stochProc=None,
                 stochDiffEq=None,
                 closedFormSolution=False,
                 isLattice=False,
                 priceJumps=None,
                 jumpProbs=None,
                 params=None,
                 defaultMethod=None):
        """
        name : str
        phi       : func      : char func
        X         : StochProc : proc
        dX        : sSDE      : dX
        priceMults: func      : priceJumps in Tree (ordered inc)
        probMults : func      : prob of each price Jump
        analytic  : func      : If analytic formula
        lattice   : func      : Tree pricing
        params    : list      : Ordered list of titles of params
        """
        self.name = name
        self.phi = phi
        self.X = stochProc
        self.dX = stochDiffEq

        self.priceJumps = priceJumps
        self.jumpProbs = jumpProbs

        self.closedFormSolution = closedFormSolution
        self.isLattice = isLattice
        self.params = params
        self.defaultMethod = defaultMethod

    @property
    def initData(self):
        """Labled inputs to __init__ to this instance."""
        className = 'Model'
        initData_ = [
            ('name',               self.name),
            ('params',             self.params),
            ('phi',                f'{self.phi is not None}'),
            ('Stoch Proc.',        f'{self.X is not None}'),
            ('SDE',                f'{self.dX is not None}'),
            ('priceJumps',         self.priceJumps),
            ('jumpProbs',          self.jumpProbs),
            ('closedFormSolution', self.closedFormSolution),
            ('isLattice',          self.isLattice),
            ('defaultMethod',      self.defaultMethod)
            ]
        
        return className, initData_
        
    def __repr__(self):
        """Return repr(self)"""
        return showData.makeRepr(self.initData)

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

    @property
    def defaultTech(self):
        if not self.defaultMethod:
            return self.pricingTech[0]
        else:
            return self.defaultMethod

    @property
    def evals(self):
        res = [(tech_: techEvals[tech_]) for tech_ in self.pricingTech]
        for r in res:
            print(r)
        return res

    @property
    def display_model_info(self):
        """Displays detailed information about the model, including all its attributes."""
        print(f"Model Name: {self.name}")
        print(f"Stochastic Process: {self.stochastic_process}")
        print(f"SDE: {self.sde}")
        print(f"Closed Form Solution: {'Yes' if self.closed_form_solution else 'No'}")
        print(f"Characteristic Function: {'Available' if self.characteristic_function else 'Not available'}")
        if self.is_lattice_model:
            print(f"Lattice Model Details:")
            print(f"  Price Jumps: {self.price_jumps}")
            print(f"  Jump Probability: {self.jump_probability}")
