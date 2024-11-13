"""Implement Index class."""

import numpy as np
import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import helperFunctions.helperFunctions as hf

class Index:
    """Implement an indexing set, used in indexing stochastic processess."""

    def __init__(self, I, continuous=True, discrete=False):
        """Initialize an indexing set.

        Parameters
        ----------
        I         : float, array_like: If array_like given in ascending order.
        continous : bool,  optional  : If 'arr' represents continous set.
        discrete  : bool,  optional  : If 'arr' represents discrete set.

        Initializes
        -----------
        self.I         : array : Indexing set.
        self.continous : bool  : Index is continous. 
        self.discrete  : bool  : Index is a discrete set.
        
        Notes
        -----
        A continous indexing set is defined by:
            I=X, discrete=False, continous=True
        Where X is either a float, array_like of length 1 or 2 with X[0] a
        minimal element of I.

        Need for 'discrete' and 'continous' paramaters are only needed for len 1
        and len 2 array_like inputs where the index set can just be a one or
        two point discerete set.

        """
        I_ = hf.makeArray(I)
        if len(I_) == 1:
            self.I = np.append(I_, np.inf)
        else:
            self.I = I_
        self.continuous = (len(self.I) == 2 and not discrete)
        self.discrete = not self.continuous

    @property
    def type(self):
        """Return, as a string, if X is continous or discete."""
        return 'continuous' if self.continuous else 'discrete'

    @property
    def start(self):
        """Return minimum element in indexing set."""
        return self.I[0]

    @property
    def end(self):
        """Return maximum element in indexing set."""
        return self.I[1]

    @property
    def range(self):
        """Return the start and end of the indexing set."""
        return np.array([self.start, self.end])

    @property
    def size(self):
        """Return the size of the indexing set.

        Notes
        -----
        This function returns the number of elements in self.I if self.discrete;
        otherwise, this function returns the length of the indexing interval.

        """
        return self.end - self.start if self.continuous else len(self.I)

    def membership(self, toCheck):
        """Return if the input is a subset of the indexing set.

        Parameters
        ----------
        toCheck: float, array_like: If array_like given in ascending order.

        Returns
        -------
        res: bool: If toCheck is a subset of self.I.

        """
        if type(toCheck) in {int, float} and self.continuous:
            res = self.start <= toCheck <= self.end

        elif type(toCheck) in {int, float} and self.discrete:
            res = toCheck in self.I

        elif len(toCheck) == 1:
            res = self.membership(toCheck[0])

        elif self.continuous:        
            mnCands, mxCands = toCheck[0], toCheck[-1]
            res = (self.start <= mnCands) and (self.end >= mxCands)
        
        else:
            res = set(toCheck).issubset(set(self.I))

        return res

    def intersection_(self, S):
        """Return the intersection of two indexing sets.

        Parameters
        ----------
        S : Index : Indexing set.

        Returns
        -------
        res : tuple : Data for Index.__init__.

        """
        disc_ = (self.discrete or S.discrete)
        cont_ = not disc_
        if cont_:
            mn = min(self.start, S.start)
            mx = max(self.end, S.end)
            inter = np.array([mn, mx])
            
        elif self.discrete and S.discrete:
            S_ = set(S.I)
            inter = np.array(sorted([x for x in self.I if x in S_]))

        else:
            mn, mx = self.range if self.continuous else S.range
            cands = self.I if self.discrete else S.I
            mnI, mxI = np.searchsorted(cands, [mn, mx], side='left')#
            inter = cands[mnI:mxI]
                
        return inter, cont_, disc_
    
    def intersect(self, S):
        """Change self to the intersection of two indexing sets.

        Parameters
        ----------
        S : Index : Indexing set.

        Initializes
        -----------
        self.I         : array : Indexing set.
        self.continous : bool  : Index is continous. 
        self.discrete  : bool  : Index is a discrete set.

        """
        inter, cont_, disc_ = self.intersection_(S)
        self.I, self.continuous, self.discrete = inter, cont_, disc_
            
    def intersection(self, S):
        """Return the intersection of two indexing sets.

        Parameters
        ----------
        S : Index : Indexing set.

        Returns
        -------
        res : Index : Indexing set.

        """
        inter, cont_, disc_ = self.intersection_(S)
        res = Index(inter, cont_, disc_)
        return res

    def extention_(self, S):
        """Return the extension of two indexing sets.

        Parameters
        ----------
        S : Index : Indexing set, with S.type == self.type.

        Returns
        -------
        res : array : New indexing set.

        Notes
        -----
        If extending two continous intervals they are assumed to overlap.

        """
        if self.continuous:
            inter = np.array([min(S.start, self.start), max(S.end, self.end)])

        else:
            inter = np.sort(np.unique(list(self.I) + list(S.I)))
            
        return inter
        
    def extend(self, S):
        """Change index to extension of itself with another indexing set.

        Parameters
        ----------
        S : Index: Indexing set with S.type == self.type

        Initializes
        -----------
        self.I : array : Indexing set.

        Notes
        -----
        If extending two continous intervals they are assumed to overlap.

        """
        self.inter = self.extention_(S)

    def extention(self, S):
        """Return the extension of two indexing sets.

        Parameters
        ----------
        S : Index : Indexing set, with S.type == self.type.

        Returns
        -------
        res : Index : Extended index.

        """
        inter = self.extension_(S)
        res = Index(inter, self.discrete, self.continuous)
        return res

    @property
    def initDict(self):
        """Dictionary of labled inputs for __init__ to this instance."""

        className = 'Index'
        initOrder = ['I', 'continuous', 'discrete']
        repData = {
            'I'         : self.I,
            'continuous' : self.continuous,
            'discrete'  : self.discrete}
        
        return className, repData, initOrder

    def __repr__(self):
        """Representation of the class instance."""

        className, repData, order = self.initDict
        rep = ', '.join([f'{x}: {repData[x]}' for x in order])
        
        return f'{className}({rep})'

    def __str__(self):
        """Return str(self)"""
        return f'{self.type} index: {self.I}'
