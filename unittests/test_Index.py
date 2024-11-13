"""Test Index"""

import unittest
import numpy as np
import sys
sys.path.append('../quantFinance/stochastic/Index')
from Index import *

class TestIndex(unittest.TestCase):

    def test_init(self):
        a = Index(5)
        #print(a.I, a.continuous, a.discrete)

        a = Index([5, 6], discrete=True)
        #print(a.I, a.continuous, a.discrete)

    def test_ranges(self):
        a = Index([2, 3])
        #print(a.range, a.start, a.end, a.size)
        #print(a)

        a = Index([5, 7, 6])
        #print(a)
        #print(a.range, a.start, a.end, a.size)

    def test_membership(self):
        a = Index([5, 6])
        #for y in [[5, 6]]:
            #print(f'y={y}: {a.membership(y)}')

        a = Index([5, 7, 6], discrete=True)
        #for y in [[6]]:
            #print(f'y={y}: {a.membership(y)}')

    def test_membership(self):
        a = Index([5, 6])
        b = Index([5.5, 10])
        c =a.extend(b)
        print(c)

        a = Index([5, 7, 6], discrete=True)

if __name__ == '__main__':
    unittest.main()

