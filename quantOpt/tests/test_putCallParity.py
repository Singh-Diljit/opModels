"""Unittests for putCallParity.py"""

import unittest
from putCallParity import putCallParity, impliedRate, getRiskFreeRate
from helperFunctions import discounted, expVal
from numpy import log as ln
from statistics import NormalDist as normal

def BSM_(spotPrice, strikePrice, intRate, T, vol, dividend):
    """Return the BSM price of a put and a call.

    NOTE: This function has been AMENDED for use in this unittest.
          Amendments: Instead of just one, both a put and a call
          are priced.
          
    PLEASE SEE BSM FILE FOR IMPLEMENTED BSM FUNCTION.

    Parameters
    ----------
    spotPrice : float
        Current price of stock.
    strikePrice : float
        Strike price of the option.
    intRate : float
        Annualized risk-free interest rate, continuously compounded.
    T : float
        Time, in years, until maturity. Function assumes T != 0.
    vol : float
        Volatility of stock.
    dividend : float, list
        Either continous dividend rate, or list of payouts.
        
    Returns
    -------
    BSM_() : tuple
        The BSM price of a call and a put.
        
    """
    stdDev = vol * (T**.5)
    logChange = ln(spotPrice/strikePrice) + (intRate-dividend)*T
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev

    costStrike = discounted(strikePrice, intRate, T)
    divDiscSpot = discounted(spotPrice, dividend, T)

    #Price put    
    prITM, prOTM = normal().cdf(-d2), normal().cdf(-d1)
    put_ = expVal(prITM, costStrike) - expVal(prOTM, divDiscSpot)
    
    #Price call
    prITM, prOTM = normal().cdf(d1), normal().cdf(d2)
    call_ = expVal(prITM, divDiscSpot) - expVal(prOTM, costStrike)

    return call_, put_

class putCallParityTest(unittest.TestCase):
    """Test of 'putCallParity' function."""

    def test_continousDiv(self, eps=.0001):
        """Test case where dividends are modelled being paid continously.

        Accepted error in comparing floats is by defualt set to eps = .0001.

        BSM is used with the parameters required for put-call parity
        (and vol=.1) to generate reasonable put and call prices. These prices
        are used to agaisnt the 'putCallParity' function to verify pricing.

        As implemented BSM requires continous dividends, to test putCallParity
        in the case of discrete dividends note only one line of code is changed,
        and is is just subtraction by a tested, simple, function.

        The BSM function as used for this unittest is slightly amended
        to save computing time, namely it prices both puts and calls at
        the same time. 
        
        """
        spotPrices = [65 + i for i in range(5)]
        strikePrices = [75 + i for i in range(-5, 5)]
        expirys = [.25, .5, 1, 2]
        intRates = [i/100 for i in range(-5, 5)]
        divs = [.001*i for i in range(5)]

        for S in spotPrices:
            for K in strikePrices:
                for T in expirys:
                    for r in intRates:
                        for q in divs:
                            C, P = BSM_(S, K, r, T, .1, q)
                            failMessage = (f'C: {C}, P: {P}, K: {K},'
                                          +f' r: {r}, T: {T}, div: {q}')
                            C_ = putCallParity(P, S, K, r, T, q, priceCall=True)
                            P_ = putCallParity(C, S, K, r, T, q)
                            errorC, errorP = abs(C - C_), abs(P - P_)
                            self.assertTrue((errorC  < eps),
                                            failMessage + ' Pricing Call')
                            self.assertTrue((errorP  < eps),
                                            failMessage + ' Pricing Put')

class impliedRateTest(unittest.TestCase):
    """Test of 'impliedRate' function.

    Note: The validity of the function is being tested, not the assumptions
    of the model. While possible to generate call and put prices that align
    (up to some model) with the paramaters it is not requred to test this
    function.

    """

    def test_continousDiv(self, eps=.0001):
        """Test case where dividends are modelled being paid continously.

        Accepted error in comparing floats is by defualt set to eps = .0001.
        
        """
        callPrices = [x for x in range(25, 50, 5)]
        spotPrices = [65 + i for i in range(5)]
        strikePrices = [75 + i for i in range(-5, 5)]
        expirys = [.25, .5, 1, 2]
        intRates = [i/100 for i in range(-5, 5)]
        divs = [.001*i for i in range(5)]
        
        for C in callPrices:
            for S in spotPrices:
                for K in strikePrices:
                    for T in expirys:
                        for r in intRates:
                            for q in divs:
                                P = putCallParity(C, S, K, r, T, q)
                                failMessage = (f'C: {C}, P: {P}, K: {K},'
                                              +f' r: {r}, T: {T}, div: {q}')
                                imRate = impliedRate(C, P, S, K, T, q)
                                error = abs(r - imRate)
                                self.assertTrue((error  < eps), failMessage)

    def test_discreteDiv(self, eps=.0001):
        """Test case where dividends are paid discretely.

        Accepted error in comparing floats is by defualt set to eps = .0001.
        
        """
        callPrices = [x for x in range(25, 40, 5)]
        spotPrices = [65 + i for i in range(5)]
        strikePrices = [75 + i for i in range(-5, 5, 2)]
        expirys = [.25, 1, 2]
        intRates = [i/100 for i in range(-5, 5)]

        for T in expirys:
            for S in spotPrices:
                divTotal = S/40
                divsM = [divTotal / 12] * int(12*T)
                divsQ = [divTotal / 4] * int(4*T)
                divsY = [divTotal / 2] * int((T//1))
                timeM = [i/12 for i in range(1, int(12*T) + 1)]
                timeQ = [i/4 for i in range(1, int(4*T) + 1)]
                timeY = [i/4 for i in range(1, int(T//1) + 1)]
                divPairs = [(divsM, timeM), (divsQ, timeQ), (divsY, timeY)]
                for K in strikePrices:
                    for C in callPrices:
                        for r in intRates:
                            for q, payouts in divPairs:
                                P = putCallParity(C, S, K, r, T, q, payouts)
                                failMessage = (f'C: {C}, P: {P}, K: {K},'
                                              +f' r: {r}, T: {T}, div: {q}'
                                              +f' divTimes: {payouts}')
                                imRate = impliedRate(C, P, S, K, T, q, payouts)
                                error = abs(r - imRate)
                                self.assertTrue((error  < eps),
                                                failMessage + f' ans: {imRate}')

if __name__ == "__main__":
    unittest.main()
