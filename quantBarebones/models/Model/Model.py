"""Barebones Model"""

class qq:
    def __init__(self, phi=None, stochProc=None, analytic=False,
                 priceMults=None, probMults=None):
        self.phi = phi
        self.S_t = stochProc
        self.analytic = analytic

        self.priceJumps = priceMults
        self.probJumps = probMults


