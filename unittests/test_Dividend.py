"""Test select functions from divHelper.py, Dividend class from Dividend.py"""

import unittest
import numpy as np
import sys
sys.path.append('../quantFinance/dividend')
from divHelper import *

class Test_extractDiv(unittest.TestCase):
    """Test: 'overlapRange' function.

    See function documentation for more details.

    Summary of 'overlapRange'
    -------------------------
    Return dividend and dividend type (discrete or continuous).

    Parameters
    ----------
    div      : array_like, float : Dividend payment quantity.
    discrete : bool      , None  : Dividend type.
    times    : array_like, None  : Ascending time until disbursements.
    dates    : array_like, None  : Dates of future disbursements.

    Returns
    -------
    res : tuple : Dividend type (bool) and dividend (np.array or float).

    """
    def failureData(self, div, discrete, times, dates, ans, res):
        """Used to return relevant data for failed test instance."""
        
        inputs = [f'div={div}',
                  f'discrete={discrete}',
                  f'times={times}',
                  f'dates={dates}']
        
        failureMsg = 'For Parameters:'
        for param in inputs:
            failureMsg += f'\n {param}'

        failureMsg += f'\n Output  : {res} \n Expected: {ans}'
        
        return failureMsg

    def test_notlabeledContinuous_isContinuous(self):
        """Test cases when dividend is identified as continuous."""

        #Set up test instances
        divInputs = [0, [0, 0], np.array([]), []]
        timeDateInputs = [None, [], [4], [1, 2, 3], np.datetime64('today')]
        testInputs = zip(divInputs, timeDateInputs, timeDateInputs)

        labelInputs = [None, False]
        #Expected answer
        ans = (False, 0)
        
        for div, time, date in testInputs:
            for discrete in labelInputs:
            
                #Expected answer and function result
                res = extractDiv(div, discrete, time, date)

                #Compare
                failureMessage = self.failureData(
                    div, discrete, time, date, ans, res)
                self.assertEqual(ans, res, failureMessage)

    def test_labeledContinuous_isContinuous(self):
        """Test cases when dividend is labeled as continuous."""

        # Dividend presented as a list or array.
        
        #Set up test instances
        testIters = [[1], (4), [0], np.array([9]), []]
        for div in testIters:

            #Inputs
            discrete = False
            time, date = None, None
            
            #Expected answer and function result
            ans = (False, np.sum(div))
            res = extractDiv(div, discrete, time, date)

            #Compare
            failureMessage = self.failureData(
                div, discrete, time, date, ans, res)
            self.assertEqual(ans, res, failureMessage)
            
        # Dividend presented as int or float.
        
        #Set up test instances
        testNumeric = [1, 0, 4.2]
        for div in testNumeric:

            #Inputs
            discrete = False
            time, date = None, None
            
            #Expected answer and function result
            ans = (False, div)
            res = extractDiv(div, discrete, time, date)

            #Compare
            failureMessage = self.failureData(
                div, discrete, time, date, ans, res)
            self.assertEqual(ans, res, failureMessage)

    def test_notLabeled_isDiscrete(self):
        """Test cases when dividend is identified as discrete."""
        
        # Time determines discrete.
        
        #Set up test instances
        testTimes = [[1, 2, 3], np.array([1, 2, 3])]
        for time in testTimes:

            #Inputs
            div = [7, 5, 3]
            discrete = None
            date = None
            
            #Expected answer and function result
            ans = (True, np.array([x for x in div]))
            res = extractDiv(div, discrete, time, date)

            #Compare
            failureMessage = self.failureData(
                div, discrete, time, date, ans, res)
            self.assertEqual(ans[0], res[0], failureMessage)
            self.assertIsNone(np.testing.assert_array_equal(ans[1], res[1]),
                              failureMessage)

        # Date determines discrete.
        
        #Set up test instances
        today = np.datetime64('today')
        testDates = [[today, today+1], np.array([today-10, today])]
        for date in testDates:

            #Inputs
            div = [7, 5]
            discrete = None
            time = None
            
            #Expected answer and function result
            ans = (True, np.array([x for x in div]))
            res = extractDiv(div, discrete, time, date)

            #Compare
            failureMessage = self.failureData(
                div, discrete, time, date, ans, res)
            self.assertEqual(ans[0], res[0], failureMessage)
            self.assertIsNone(np.testing.assert_array_equal(ans[1], res[1]),
                              failureMessage)

class Test_getTimes(unittest.TestCase):
    """Test: 'getTimes' function.

    See function documentation for more details.

    Summary of 'getTimes'
    -------------------------
    Return an array of times in years of dividend payouts.

    Parameters
    ----------
    discrete   : bool             : If dividend is discrete.
    times      : array_like, None : Ascending times (years) until disbursements.
    dates      : array_like, None : Dates of future disbursements.
    startDate  : date_like , None : Start date.

    Returns
    -------
    res : array : Array of times in years of dividend payouts.

    """
    def failureData(self, discrete, times, dates, startDate, ans, res):
        """Used to return relevant data for failed test instance."""
        
        inputs = [f'discrete={discrete}',
                  f'times={times}',
                  f'dates={dates}'
                  f'startDate={startDate}']
        
        failureMsg = 'For Parameters:'
        for param in inputs:
            failureMsg += f'\n {param}'

        failureMsg += f'\n Output  : {res} \n Expected: {ans}'
        
        return failureMsg
    
    def test_dateIsNone(self):
        """Test cases when date==None."""
        
        #Inputs
        discrete = False
        times = [1, 2]
        dates, startDate = None, np.datetime64('today')

        ans = np.array([np.inf])
        funcRes = getTimes(False, None, None, np.datetime64('today'))
        self.assertEqual(ans, funcRes)

        ans = np.array([4])
        funcRes = getTimes(True, [4], None, np.datetime64('today'))
        self.assertEqual(ans, funcRes)        

    def test_dateNotNone(self):
        dates = [j + np.datetime64('today') for j in range(10)]
        ans = np.array([x for x in range(10)])/365
        funcRes = getTimes(True, None, dates, np.datetime64('today'))
        self.assertIsNone(np.testing.assert_array_equal(ans, funcRes))

if __name__ == '__main__':
    unittest.main()
