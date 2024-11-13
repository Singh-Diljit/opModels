"""Graphing Functions"""

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np

def array_likeConditionBA(title, data):
    flag = False
    if title in ['Spot Price', 'Strike Price', 'Interest Rate',
                 'Time till Maturity (Years)', 'Volatility']:
        if data.__class__ == np.ndarray and len(data.shape) > 1:
            flag = True
        elif data.__class__ in [list, tuple]:
            if len(data) > 1:
                flag = True
    if flag != True and title in ['Dividends', 'Dividend PayOut Times (Years)']:
        if min(np.array(data).shape) > 1:
            flag = True
    return flag
            

def getLabelsBlacksApprox(S, K, r, T, vol, q, dYr, call):
    opType = 'Call' if call else 'Put'

    titles = ['Spot Price', 'Strike Price',
              'Interest Rate', 'Time till Maturity (Years)',
              'Volatility', 'Dividends',
              'Dividend PayOut Times (Years)']
    
    flag = False
    for i, x in enumerate([S, K, r, T, vol, q, dYr]):
        if flag: break
        if array_likeConditionBA(titles[i], x):
            xTitle = titles[i]
            flag = True
        
    if flag == False:
        xTitle = 'Spot Price'
    return {'xTitle': xTitle, 'opType': opType}
        

def simpleGraph(xVals, yVals, xTitle="x", yTitle="f(x)", title=False):
    """Graph x vs y.

    Parameters
    ----------
    xVals : array_like    : Values of x-coordinates.
    yVals : array_like    : Values of y-coordinates.
    xTitle: str, optional : Title of x-axis.
    yTitle: str, optional : Title of y-axis.
    title : str, optional : Title of graph.

    Returns
    -------
    graph : ??? : Graph of f(x).

    """
    plt.plot(xVals, yVals, marker='o')
    plt.xlabel(xTitle)
    plt.ylabel(yTitle)
    if title: plt.title(title)

    plt.show()

def surface(xVals, yVals, f,
            xTitle="x", yTitle="y", zTitle='f(x, y)', title=False):
    """3D surface"""
    xVals, yVals = np.meshgrid(xVals, yVals)
    zVals = f(xVals, yVals)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    surf = ax.plot_surface(xVals, yVals, zVals)

    ax.set_xlabel(xTitle)
    ax.set_ylabel(yTitle)
    ax.set_zlabel(zTitle)
    if title: plt.title(title)
    
    plt.show()


