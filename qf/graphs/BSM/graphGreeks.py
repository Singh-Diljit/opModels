"""Graph BSM Greeks"""

from bsmGreeks import *
from graphFuncBSM import *
import numpy as np

def graphGreeks(S, K, r, T, vol, q, call=True, greek='delta'):

    labels = getLabelsBSM(S, K, r, T, vol, q, call)
    xTitle, opType = labels['xTitle'], labels['opType']
    yTitle = greek
    graphTitle = f'{greek} of {opType} as {xTitle} Varies'

    titleDic = {'Spot Price': S, 'Strike Price': K,
              'Interest Rate': r, 'Time till Maturity (Years)': T,
              'Volatility': vol, 'Dividends': q}
    
    xVals = titleDic[xTitle]
    greekDic = {'delta': delta, 'gamma': gamma,
              'theta': theta, 'vega': vega,
              'rho': rho}

    yVals = greekDic[greek](S, K, r, T, vol, q)
        
    simpleGraph(xVals, yVals, xTitle, yTitle, graphTitle)

S = np.linspace(.1, 100, num = 25)
graphGreeks(S, K=55, r=.1, T=.5, vol=.3, q=0, greek='delta')
