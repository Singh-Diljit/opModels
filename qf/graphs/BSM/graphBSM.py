"""Graph Model"""

import numpy as np
from scipy.stats import norm
from graphFuncBSM import *
from bsm import BSM

def graphBSM(S, K, r, T, vol, q, call=True):
    labels = getLabelsBSM(S, K, r, T, vol, q, call)
    xTitle, opType = labels['xTitle'], labels['opType']
    yTitle = f'Value of {opType}'
    graphTitle = f'Price of {opType} as {xTitle} Varies'

    dic = {'Spot Price': S, 'Strike Price': K,
              'Interest Rate': r, 'Time till Maturity (Years)': T,
              'Volatility': vol, 'Dividends': q}
    
    xVals = dic[xTitle]
    yVals = BSM(S, K, r, T, vol, q, call)
        
    simpleGraph(xVals, yVals, xTitle, yTitle, graphTitle)

K = np.linspace(40, 60, num=10)
graphBSM(50, K, .1, .5, .3, 0)
