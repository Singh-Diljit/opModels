"""MC SDE EU"""

import numpy as np

"""
dX.discretize(sims=sims, steps=steps, path)

path == True: ans = [res[0], ..., res[K]] (K = dX.dim)

               sim0  ...  simM 
                |          |
             | --- step 0 --- |
    res[i] = | --- ...... --- |
             | --- ...... --- |
             | --- step N --- |

path == False:

         | --- res[0][-1] --- |
   ans = | --- .......... --- |
         | --- .......... --- |
         | --- res[K][-1] --- |
        
"""

def priceEU(dX, K, r, T, sims=10**5, steps=100 call=True):
    """Price Euro option via MC on SP."""
    vals = dX.discretize(sims=sims, steps=steps, path=False)[0]
    payOff = np.maximum(vals-K, 0) if call else np.maximum(K-vals, 0)
    return np.exp(-r*T) * np.mean(payOff)
    
def priceAM(SP, K, r, T, sims=10000, steps=100, degree=5, call=True):
    """Longstaff and Schwartz"""
    dT = T/steps
    disc = np.exp(-r*dT)
    P = dX.discretize(sims=sims, steps=steps+, path=False)[0]

    #generate payoffs
    payOff = np.maximum(vals-K, 0) if call else np.maximum(K-vals, 0)

    for i in np.arange(steps-1, 0, -1):
        leastSq = np.polyfit(P[i], opVals[i+1]*disc, degree)
        contVal = np.polyval(leastSq, P[i])
        boolEx = (opVals[i] > contVal)
        opVals[i] = opVals[i]*boolEx + opVals[i+1]*disc*(np.invert(boolEx))

    return disc * np.mean(opVals[1])
