"""Draw BOPM-CRR."""

import numpy as np

#BERMUDA USES dT*i in excersiceDates

def drawBOPM(S, K, r, T, vol, q, depth=50,
             call=True, eu=False, am=False, be=False,
             exerciseDates=[]):
    """Print the tree generated by a BOPM of an option.
    
    Parameters
    ----------
    S       : float
    K       : float
    r       : float
    T       : float
    priceUp : float : func fixed with req. params so float
    probUp  : float : func fixed with req. params so float
    depth   : int
    call    : bool 
    levels  : int
    
    Returns
    -------
    A plot of binomial lattice and relevant data.
        
    Example(s)
    ----------
    >>>

    """
    #Check well-definedness of probability
    if depth < np.ceil(T * (r - q)**2 / vol**2):
        raise ValueError(
            f'Need: depth >= {np.ceil(T*(r-q)**2/vol**2)}.')

    #Frequently used values
    dT = T / depth
    disc = np.exp(-r * dT)

    up = np.exp(vol * np.sqrt(dT))
    down = 1/up
    pU = (np.exp((r-q)*dT) - down) / (up - down)
    pD = 1 - pU
    
    #Option Type
    if not any([eu, am, be]):
        european, american, bermuda = True, False, False
    else:
        european, american, bermuda = eu, am, be
    
    optType = ""
    if american:
        optType += 'American '
    elif european:
        optType += 'European '
    else:
        optType += 'Bermuda '
    if call: optType += 'call' if call else 'put'
    
    writtenData = (f"""
        ==========================BOPM========================

        |====================  PARAMETERS ====================
        |
        |K             : {K}                    
        |S0            : {S}
        |r             : {r}
        |T             : {T}
        |vol           : {vol}
        |div           : {q}
        |Option        : {optType}
        |height        : {depth}
        |exerciseDates : {exerciseDates}
        |
        |==================  Extracted Data ==================
        |
        |min height    : {np.ceil(T*(r-q)**2/vol**2)}
        |upFactor      : {up}
        |downFactor    : {down}
        |probUp        : {pU}
        |probDown      : {pD}
        |
        |=====================================================""")
    print(writtenData)
        
    #Value at expiry
    if european:
        S *= up ** np.arange(-depth, depth+1, 2, dtype=float)
        opPr = np.maximum(S - K, 0) if call else np.maximum(K - S, 0)

    else:
        W = np.zeros((2, depth+1))
        W[0] = np.arange(-depth, depth+1, 2, dtype=float)
        W[1] = np.arange(-depth+1, depth+2, 2, dtype=float)
        S *= up ** W
        opPr = np.maximum(S[0] - K, 0) if call else np.maximum(K - S[0], 0)
        
    #Value at earlier times
    for i in np.arange(depth-1, -1, -1):
        data = (f"""
        |==================  Level Data ==================
        |Height : {i+1}
        |Time   : {dT * (i+1)}
        |Nodes  : {len(opPr[:i+2])}""")
        print(data)
        print("        |" + ", ".join(str(round(x, 3)) for x in opPr[:i+2]))
        print("        |====================================================")
        opPr[:i+1] = disc * (pU * np.ediff1d(opPr[:i+2]) + opPr[:i+1])

        if european:
            opPr = np.maximum(opPr[:-1], 0)
        elif american or dT*i in exerciseDates:
            A, B = (depth-i)//2, (depth-i+1)//2
            if call:
                ex = np.maximum(S[(depth+i)%2][A:-B] - K, 0)
            else:
                ex = np.maximum(K - S[(depth+i)%2][A:-B], 0)

    data = (f"""
        |==================  Level Data ==================
        |Height : {0}
        |Time   : {0}
        |Nodes  : {1}""")
    print(data)
    print("        |" + str(round(opPr[0], 3)))
    print("        |====================================================")
    
    return opPr[0]

drawBOPM(100, 90, .08, .5, .1, .04, 5, call=False, am=True) 
