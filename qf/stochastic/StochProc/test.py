import numpy as np
from BrownianMotion import BrownianMotion
from CompoundPoisson import CompoundPoisson
from Geometric import Geometric
import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Index.Index import *

I = Index(0, 1)
BM = BrownianMotion(0, 1, I)
BM.graph(sims=1000)
