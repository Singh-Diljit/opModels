"""Test."""

from testDiv import minimalDiv
from putCallBounds import *
import numpy as np

"""putCallParity""" #Fomula is correct

q = minimalDiv(.01)
putCallParity(0.5287, 100, 110, .08, .5, q)
#6.714290387487309

putCallParity(6.714290387487309, 100, 110, .08, .5, q, priceCall=True)
#0.5286999999999997

qDisc = minimalDiv(np.array([.73, .82, .76, .8]), np.array([.5, 1, 1.5, 2]),cont=False) 
putCallParity(2, 100, 110, .05, 2.25, qDisc)
#3.216647529846469

zeroC = minimalDiv(0)
putCallParity(2, 100, 110, .05, 2.25, zeroC, True)
#3.7042918180632682

zeroD = minimalDiv(np.array([0]), np.array([0]), cont=False)
putCallParity(2, 100, 110, .05, 2.25, zeroD, True)
#3.7042918180632682

"""putCallBound""" #Formula is correct

putCallBound(2.03, 36, 37, .055, .5)
#(2.026363254477799, 3.03)

putCallBound(2.03, 37, 35, .055, .5, boundCall=True)
#(4.029999999999999, 4.979386110629113)

"""lowerBoundRate""" #Math is correct
lowerBoundRate(0.5287, 6.714290387487309, 100, 110, .5)
#0.07058389984817895


