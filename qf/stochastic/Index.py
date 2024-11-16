"""Implement Index class."""

import numpy as np
import sys
sys.path.append('../')
from helperFuncs import formatting, showData

class Index:
    """Implement an indexing set, used in indexing stochastic processess."""

    def __init__(self, start=0, end=np.inf, discreteSet=None):
        """Initialize an indexing set.

        Parameters
        ----------
        start       : float      : Start of cont. indexing range.
        end         : float      : End of cont. indexing range.
        discreteSet : array_like : Discrete indexing set.

        Initializes
        -----------
        self.I          : array : Indexing set.
        self.isDiscrete : bool  : If index is a discrete set.

        """
        self.isDiscrete = discreteSet is not None
        if self.isDiscrete:
            self.I = formatting.makeArray(discreteSet)
        else:
            self.I = np.array([start, end])

    @property
    def start(self):
        return self.I[0]

    @property
    def end(self):
        return self.I[-1]

    @property
    def range(self):
        """Return max(Index) - min(Index)."""
        return self.end - self.start

    @property
    def interval(self):
        """Return [start, end]."""
        return np.array([self.start,self.end]) if self.isDiscrete else self.I
    
    def makeDiscrete(self, steps=100):
        """If set is cont. return evenly spaces points in the index."""
        if self.isDiscrete:
            disc_ = self.I
            increments = np.ediff1d(self.I)
        else:
            disc_, increments = np.linspace(self.start, self.end,
                                            steps, retstep=True)
        return disc_, increments

    @property
    def makeSelf(self):
        if self.isDiscrete:
            res = Index(discreteSet = self.I)
        else:
            res = Index(start=self.start, end=self.end)
        return res

    def __bool__(self):
        return (self.I.size > 0)

    @property
    def empty(self):
        return Index(discreteSet=[])
    
    @property
    def numEls(self):
        return len(self.I) if self.isDiscrete else np.inf

    def boundBelow(self, newStart=None):
        """Exclude values below newStart."""
        if self.__bool__ == False:
            print('cat')
            return self.empty
        
        if newStart is None or newStart <= self.start:
            res = self.makeSelf
            
        elif newStart > self.end:
            res = self.empty
        
        elif self.isDiscrete:
            start_ = 0
            for i, x in enumerate(self.I):
                if x >= newStart:
                    start_ = i; break
                    
            res = Index(discreteSet = self.I[start_:])

        else:
            start_ = max(self.start, newStart)
            res = Index(start_, self.end)

        return res

    def boundAbove(self, newEnd=None):
        """Exclude values above newEnd."""
        if self.__bool__ == False:
            return self.empty
            
        if newEnd is None or newEnd >= self.end:
            res = self.makeSelf
            
        elif newEnd < self.start:
            res = self.empty
        
        elif self.isDiscrete:
            newSet = list(self.I)
            while newSet[-1] > newEnd:
                newSet.pop()
            res = Index(discreteSet = newSet)

        else:
            end_ = min(self.end, newEnd)
            res = Index(self.start, end_)

        return res

    def restrict(self, newStart=None, newEnd=None):
        """Exclude values below newStart and above newEnd."""
        res = self.boundAbove(newEnd)
        if bool(res) == False:
            res = self.empty
        else:
            res = res.boundBelow(newStart)
        return res

    @property
    def initData(self):
        """Labled inputs to __init__ to this instance."""
        
        className = 'Index'
        if self.isDiscrete:
            initData_ = [
                ('discreteSet', self.I)
                ]
        else:
            initData_ = [
                ('start', self.I[0]),
                ('end',   self.I[1])
                ]
            
        return className, initData_

    def __repr__(self):
        """Return repr(self)."""
        return showData.makeRepr(self.initData)

    def __str__(self):
        """Return str(self)."""
        return str(self.I)


a = Index(discreteSet = [1, 2, 3, 5, 6, 7])
b = a.restrict(-7, -5)
print(a.makeDiscrete(steps=10))

