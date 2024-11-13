"""Test price against intchareq. """

from price import bsj
from testModels import *
import numpy as np

a = bsj(S=95, K=100, r=.07, T=1, vol=.25, q=0, lam=1, stdJ=.4, scaleJ=1.1, sumMx=50)
print(a)

B = mertonJ(S=95, K=100, r=.07, T=1, vol=.25,
                lam=1, v=.4, m=1.1, N=50, call=True)
print(B)

"""
phiJ = phiBSJ1(S=95, r=.07, T=1, v=.25, q=0,
             lam=.1, mu=.1, delta=.1)

C = integratePhi(phiJ, S=95, K=100, r=.07, T=1, q=0, call=True)[0]
print(C)
"""
