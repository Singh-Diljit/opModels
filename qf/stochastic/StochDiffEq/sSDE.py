"""Implement a class for systems of SDEs."""

import numpy as np
import procHelper
import solver
from Index import Index

####
NEEDED:
1. 
    Let P = [P^1, ..., P^M], dP = [P^1, ..., P^M]. Is sampling done
    via StochProc class (using P) or in simpleSDE class (using dP)?
2. dimProcess uses dP[0].dim property
    
####
"""
Notation
--------

Let dX_t reprsent a system of d SDEs each driven by a combination of M
independent stochastic processes; P^1, ..., P^M:

        dX^1_t    f_1(t, X_t)dt + g^1_1(t, X_t)dP^1_t + ... + g^1_M(t, X_t)dP^M_t
          .                                      .
dX_t =    .     =                                .
          .                                      .
        dX^d_t    f_d(t, X_t)dt + g^d_1(t, X_t)dP^1_t + ... + g^d_M(t, X_t)dP^M_t

Denote:

    1. Drift Vector:
    
        F = <f_1, ..., f_d>
        F(t, X_t) = <f_1(t, X_t), ..., f_d(t, X_t)>

    2. Process Vector:
    
        dP_t = <dP^1_t, ..., dP^M_t>

    3. Diffusion Matrix:
    
            g_1^T   g^1_1, ..., g^1_M
             .              .
        G =  .    =         .
             .              .
            g_d^T   g^d_1, ..., g^d_M

        G(t, X_t) = {g^i_j(t, X_t)}

    4. Extended Proccess Vector:
    
        d_ext = <dt, dP^1_t, ..., dP^M_t>

    5. Drift and Diffusion Matrix:
    
                f_1, g^1_1, ..., g^1_M
                           .
        G_ext =            .
                           .
                f_d, g^d_1, ..., g^d_M

Then:

    1. dX^i_t = f_i(t, X_t)dt + g_i(t, X_t)dP_t

    2. dX_t = F^T(t, X_t)*dt + G(t, X_t)*dP_t

    3. dX_t = G_ext(t, X_t) * d_ext

Notes:

    1. Each process, P^1, ..., P^M, are indepdendent.
    2. Each SDE has indedepdent processess.
    3. dim(P^i) = 1

"""

class sSDE:
    """Implement a system of SDEs."""

    def __init__(self, drift, diff, dP, seed=[], rho=[],
                 index=0, POI=[], T=1):
        """Initialize an sSDE.

        Parameters
        ----------
        drift : array_like           : Drift vector for system.
        diff  : array_like           : Diffusion matrix for system.
        dP    : array_like           : Driving processess.
        seed  : array_like, optional : Initial value of sytem.
        rho   : array_like, optional : Correlation matrix.
        index : Index_like, optional : Data for indexing set of SDE.
        POI   : array_like, optional : Points of interest.
        T     : float,      optional : Max cutoff for sampling methods.

        Initializes
        -----------
        drift_     : array      : Data for drift vector for system.
        diffusion_ : array      : Data for diffusion matrix for system.
        dP         : list       : List of driving processess.
        seed       : array      : Initial value of sytem.
        rho_       : array_like : Data for correlation matrix (matrices).
        index_     : Index_like : Data for indexing set of SDE.
        POI        : array      : Points of interest.
        T          : float      : Max cutoff for sampling methods.

        Notes
        -----
        See Index class for information onf "Index_like".

        """
        self.drift_ = procHelper.makeCallable(drift)
        self.diffusion_ = procHelper.makeCallable(diff)
        self.dP = [dP_ for dp_ in dP]
        self.seed = np.array(seed) if seed else np.array([0]*len(self.drift))
        self.rho_ = rho
        self.index_ = index
        self.T = T
        self.POI = np.array(specialIndices)

    ###Dimension related properties
    @property
    def numEqs(self):
        """Return number of SDEs in the system."""
        return len(self.drift)

    @property
    def numProccess(self):
        """Return number of processes driving the system."""
        return len(self.dP)

    @property
    def dimProcess(self):
        """Return the dimension of the driving processes."""
        return dP[0].dim

    @property
    def shape(self, extended=False):
        """Return a tuple representing the shape of the inputs.

        Paramaters
        ----------
        extended : bool : If counting 'dt' as a process.

        Returns
        -------
        res : tuple : (#SDEs, #Processes (if extended +1), dim(P^i)).

        """
        if extended:
            res = (self.numEqs, self.numProccess + 1, self.dimProcess)
        else:
            res = (self.numEqs, self.numProccess, self.dimProcess)

        return res

    @property
    def dim(self):
        """Return a tuple representing the shape of the system.

        Returns
        -------
        res : tuple : (#SDEs, dim(P^i))

        """
        res = (self.numEqs, self.dimProcess)
        return res

    @property
    def type_(self):
        """Return classification of sSDE; used in optimizing sampling.

        Instances of an sSDE are split into 4 catagories:
            Type (1,1): Single SDE, single driving process.
            Type (1,2): Single SDE, multiple driving processes.
            Type (2,1): Multiple SDEs, single driving process.
            Type (2,2): Multiple SDEs, multiple driving processes.

        Returns
        -------
        res : tuple : Internal classification of system.

        """
        res = tuple([1 if n == 1 else 2 for n in self.shape[:1]])
        return res

    ###Finish initialization of drift, diffusion, rho, and index related data
    @property
    def drift(self):
        """Compute the drift component.

        Let D = self.dim and self.drift_ = [f_1, ..., f_D]
        Then:
            self.drift_(X) = [f_1(X), ..., f_D(X)]

        Returns
        -------
        res: func : A callable drift component.
        
        """
        return procHelper.callMulti(self.drift_)

    @property
    def diffusion(self):
        """Compute the diffusion component.

        Let D = self.dim
            G_i(X) = [g^i_1(X), ..., g^M_i(X)]    
            self.diffusion_ = [G_1, ..., G_D]
        Then:
            self.diffusion(X) = [G_1(X), ..., G_D(X)]

        Returns
        -------
        res: func : A callable diffusion component.

        """
        return procHelper.callMulti(self.diffusion_)

    @property
    def rho(self):
        """Return a collection of correlation matrices.

        Returns
        -------
        res : ndarray : Shape - (#SDEs, #Processes, dim(P^i)).
        
        """
        if not self.rho_:
            res = procHelper.identity3D(self.shape)
        else:
            res = np.array(self.rho_)
            
        return res

    @property
    def index(self):
        """Return a indexing set for sSDE.

        Returns
        -------
        res : Index : Index set.
        
        """
        if isinstance(Index, self.index_):
            mn, mx = Index.start, min(Index.end, self.T)
        else:
            mn, mx = self.index_, self.T
            
        res = Index([mn, mx])    
        return res        
        
    ###Printing and replication related methods
    @property
    def initDict(self):
        """Dictionary of labled inputs for __init__ to this instance."""

        className = 'sSDE'
        initOrder = ['drift', 'diffusion', 'dP', 'seed', 'rho',
                     'index', 'POI', 'T']
        repData = {
            'drift' : self.drift,
            'diff'  : self.diffusion,
            'dP'    : self.dP,
            'seed'  : self.seed,
            'rho'   : self.rho,
            'index' : self.index,
            'POI'   : self.POI,
            'T'     : self.T}
        
        return className, repData, initOrder

    def __repr__(self):
        """Representation of the class instance."""

        className, repData, order = self.initDict
        rep = ', '.join([f'{x}: {repData[x]}' for x in order])
        
        return f'{className}({rep})'

    def __str__(self):
        """Return str(self)"""
        return procHelper.sSDE_str(self.initDict)

    ###Analysisng sSDE via discretization, MCM, and graphing
    def monteCarlo(func, ...):
        """Samples but then uses func (e.g. payOff func) to return MC value."""
        pass
    
    def discretization(self, sims, steps, interval=self.index):
        """Simulate solutions to the system of SDEs.

        Paramaters
        ----------
        sims    : int                  : # of sims drawn at each point in time.
        steps   : int, optional        : # of uniform time discretizations.
        interval: array_like, optional : Start and end points of time interval.
        
        Returns
        -------
        res : ndarray : Drawn samples in shape=(steps, sims)) or (sims,)
        
        """
        #sampFunc = applyEM[self.type_]
        #return sampFunc(self.drift, self.diffusion, sims, steps, interval)
        pass

    def graph(self, sims, steps=self.T*252, interval=[0, self.T]):
        """Simulate solutions to the system of SDEs."""
        pass
