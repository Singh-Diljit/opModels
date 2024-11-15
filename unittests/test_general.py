"""Test helperFuncs module."""

import unittest
import numpy as np
import sys
sys.path.append('../../qf/helperFuncs')
from general import *
from formatting import *
from showData import *

class TestOverlapRange(unittest.TestCase):
    """Test: 'overlapRange' function.

    See function documentation for more details.

    Summary of 'overlapRange'
    -------------------------
    Return the intersection of a list of ranges and a list of multiples.

    Parameters
    ----------
    points : list  : Non-decreasing list of floats.
    x      : float : Base value.
    N      : int   : Total number of steps.
    fwd    : float : Defines range of each point.
    eps    : float : Accepted error in comparing floats.
        
    Returns
    -------
    res : set : Set of integers satisfying overlap condition.
    
    """
    def failureData(self, points, x, N, fwd, eps, ans, res):
        """Used to return relevant data for failed test instance."""
        
        inputs = [f'points={points}',
                  f'x={x}',
                  f'N={N}',
                  f'fwd={fwd}',
                  f'eps={eps}']
        
        failureMsg = 'For Parameters:'
        for param in inputs:
            failureMsg += f'\n {param}'

        failureMsg += f'\n Output  : {res} \n Expected: {ans}'
        
        return failureMsg
        
    def test_hasOverlap(self):
        """Test cases when non-trivial overlap is expected."""
        
        #Inputs
        points = [1/10, 1/6, 1/5, 1/2]
        x, N = 1/36, 72
        fwd, eps = .005, 10**-4

        #Expected answer and function result
        ans = {18, 6}
        res = overlapRange(points, x, N, fwd, eps)

        #Compare
        failureMessage = self.failureData(points, x, N, fwd, eps, ans, res)
        self.assertEqual(ans, res, failureMessage)

    def test_noOverlap(self):
        """Test cases when trivial overlap is expected."""
        
        # Base point ('x') is too large.
        
        #Inputs
        points = [.5, 3]
        x, N = 4, 10
        fwd, eps = .5, 10**-4

        #Expected answer and function result
        ans = set()
        res = overlapRange(points, x, N, fwd, eps)

        #Compare
        failureMessage = self.failureData(points, x, N, fwd, eps, ans, res)
        self.assertEqual(ans, res, failureMessage)
        
        # Not enough steps ('N' is too small).
        
        #Inputs
        points = [.5, 3]
        x, N = .01, 40
        fwd, eps = 2, 10**-4

        #Expected answer and function result
        ans = set()
        res = overlapRange(points, x, N, fwd, eps)

        #Compare
        failureMessage = self.failureData(points, x, N, fwd, eps, ans, res)
        self.assertEqual(ans, res, failureMessage)
              
    def test_edgeCases(self):
        """Test edge cases."""
        
        # Point set is empty ('Point' == []).
        
        #Inputs
        points = []
        x, N = 4, 10
        fwd, eps = .5, 10**-4

        #Expected answer and function result
        ans = set()
        res = overlapRange(points, x, N, fwd, eps)

        #Compare
        failureMessage = self.failureData(points, x, N, fwd, eps, ans, res)
        self.assertEqual(ans, res, failureMessage)
        
        # Zero steps ('N' == 0).
        
        #Inputs
        points = [.5]
        x, N = .5, 0
        fwd, eps = 2, 10**-4

        #Expected answer and function result
        ans = set()
        res = overlapRange(points, x, N, fwd, eps)

        #Compare
        failureMessage = self.failureData(points, x, N, fwd, eps, ans, res)
        self.assertEqual(ans, res, failureMessage)

class TestMakeArray(unittest.TestCase):
    """Test: 'makeArray' function.

    See function documentation for more details.

    Summary of 'makeArray'
    ----------------------
    Convert input into an array.

    Parameters
    ----------
    X : * : Data to convert into an array.

    Returns
    -------
    res : array : Array with data from input.

    Notes
    -----
    * Input should be either an iterable or an instance of a supported
    datatype. See numpy documentation for supported datatypes for an
    array.

    """
    def failureData(self, X, ans, res):
        """Return data if a test fails."""
        
        inputs = [f'X={X}']
        failureMsg = 'For Parameters: \n {param}'
        failureMsg += f'\n Output  : {res} \n Expected: {ans}'
        
        return failureMsg
    
    def test_isArray(self):
        """Test when input type is: np.array."""

        #Set up test instances
        testInputs = [[0], [1,2,3], [1,2,3]]
        for X in testInputs:
            #Inputs
            Y = np.array(X)
            
            #Expected answer and function result
            ans = Y
            res = makeArray(Y)

            #Compare
            failureMessage = self.failureData(X, ans, res)
            self.assertIsNone(np.testing.assert_array_equal(ans, res),
                              failureMessage)
            
    def test_isList(self):
        """Test when input type is: list."""

        #Set up test instances
        testInputs = [[0], [1,2,3], [1,2,3]]
        for X in testInputs:
            #Expected answer and function result
            ans = np.array(X)
            res = makeArray(X)

            #Compare
            failureMessage = self.failureData(X, ans, res)
            self.assertIsNone(np.testing.assert_array_equal(ans, res),
                              failureMessage)
            
    def test_isSingle(self):
        """Test when input type is: int or float."""

        #Set up test instances
        testInputs = [0, 4, 3.0]
        for X in testInputs:
            #Expected answer and function result
            ans = np.array([X])
            res = makeArray(X)

            #Compare
            failureMessage = self.failureData(X, ans, res)
            self.assertIsNone(np.testing.assert_array_equal(ans, res),
                              failureMessage)

class TestMakeRepr(unittest.TestCase):

    def test_None(self):
        className = 'testClass'
        initData = [('varName_1', None)]
        ans = 'testClass(varName_1=None)'
        self.assertEqual(makeRepr(className, initData), ans)
        #test2
        initData = [('varName_1', None), ('varName_2', None)]
        ans2 = 'testClass(varName_1=None, varName_2=None)'
        self.assertEqual(makeRepr(className, initData), ans2)
        

if __name__ == '__main__':
    unittest.main()
