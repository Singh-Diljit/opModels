"""Supporting functions used for custom class __repr__ and __str__."""

def makeRepr(classData):
    """Return repr(className).

    def className:
        def __init__(self, varName_0, ..., varName_N):
            ...

    className: str
    initData : list : [(varName_i, value of varName_i) for i in range N]

    """
    className, initData = classData
    inner = ', ' if len(initData) > 1 else ''
    repData = inner.join([f'{name}={str(val)}' for name, val in initData])
    
    return f'{className}({repData})'

def showSingleSDE(drivingProcs, coeff, indexSet):
    """Return a string representing a single SDE."""
    indivProcs = [f'{str(coeff[i])} * (proc)'
                  for i, proc in enumerate(drivingProcs)]
    inner = ' + ' if len(indivProcs) > 1 else ''
    
    return inner.join([x for x in indivProcs]) + f'   Index: {str(indexSet)}'
    
def SDE_to_string(initData, numProc, numEq):
    """Return a string representing a single SDE or system of SDEs."""
    res = [showSingleSDE(sde_) for sde_ in initData['Equations']]
    
    return '\n'.join([x for x in res])
