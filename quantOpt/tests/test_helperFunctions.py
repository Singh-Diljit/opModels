"""Unittesting for helperFunctions.py"""

import unittest
import helperFunctions as hf
from numpy import exp, log as ln

class discountedDiscreteTest(unittest.TestCase):
    """Test of 'discountedDiscrete' function."""

    def test_discDiscCont(self):
        """Test 'discountedDiscrete' when interest is coumpounded continusly."""

        payCands = [[1,10], [0], [2,10,20,40]]
        timeCands = [[.5, 1], [1], [.25, .5, .75, 1]]
        rateCands = [.01*i for i in range(-20, 20)]

        for testNum, payments in enumerate(payCands):
            times = timeCands[testNum]
            for rate in rateCands:
                failMessage = (f'Payments: {payments}, times: {times}'
                              +f' rate: {rate}')
                ans = 0
                for i, p in enumerate(payments):
                    ans += p * exp(-rate * times[i])

                self.assertEqual(hf.discountedDiscrete(payments, times, rate),
                                 ans, failMessage)

    def test_discountedDisc(self):
        """Test 'discountedDiscrete' when interest is coumpounded discretely.

        Accepted error is .0001 when comparing floats.
        
        """
        eps = .0001
        payCands = [[1 ,5], [1], [1, 2, 3, 2.5]]
        timeCands = [[.5, 1], [1], [.25, .5, .75, 1]]
        rateCands = [.01*i for i in range(1, 15)]
        coumpoundCands = [.25, .5, .75, 1]
        
        for testNum, payments in enumerate(payCands):
            times = timeCands[testNum]
            for rate in rateCands:
                for cmp in coumpoundCands:
                    failMessage = (f'Payments: {payments}, times: {times}'
                                  +f' yearly rate: {rate}, coumpounded: {cmp}')
                    ans = 0
                    r_ = rate * cmp
                    for i, p in enumerate(payments):
                        ans += p * (1+r_) ** (-times[i]/cmp)
                        
                    res = hf.discountedDiscrete(payments, times, rate, cmp)
                    error = abs(res - ans)
                    self.assertTrue((error < eps), failMessage)

class parseOptionTest(unittest.TestCase):
    """Test of 'exerciseType' and 'isCall' function."""

    def test_exerciseType(self):
         """Test of 'exerciseType' function."""
         am = (True, False, False)
         eu = (False, True, False)
         be = (False, False, True)
        
         opts = {"American Call" : am, "American Put" : am,
                 "European Call" : eu, "European Put" : eu,
                 "Bermuda Call" : be, "Bermuda Put" : be}

         for op in opts:
             failMessage = f'Option = {op}'
             self.assertEqual(hf.exerciseType(op), opts[op], failMessage)

    def test_isCall(self):
         """Test of 'isCall' function."""
         
         call, put = True, False
         opts = {"American Call" : call, "American Put" : put,
                 "European Call" : call, "European Put" : put,
                 "Bermuda Call" : call, "Bermuda Put" : put}

         for op in opts:
             failMessage = f'Option = {op}'
             self.assertEqual(hf.isCall(op), opts[op], failMessage)
        
if __name__ == "__main__":
    unittest.main()
