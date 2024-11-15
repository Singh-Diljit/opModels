"""Simulate one-dimensional SDE, driven by N processess"""

import numpy as np

def simulate_oneProc(drift, diff, underlyingProc, steps,
                     sims, seed, sampleSet, increments):
    """Apply EM when dX_t = f(t, X)dt + g(t, X)dY_t for Levy process Y.
    drift is a func
    diff is a func
    underlyingProc is a SP
    sampleSet is np.array
    singleInc is bool if single inc or not Assumed true
    """
    dt_, X = increments, np.zeros((steps+1, sims))
    X[0] = seed
    reqSims = steps*sims
    dUnderlying = underlyingProc.sample(sims=reqSims, idx=dt_,
                                        shape=(steps, sims))
    for i, t in enumerate(sampleSet, 1):
        X[i] = X[i-1] + drift(t, X[i-1])*dt_ + diff(t, X[i-1])*dUnderlying[i-1]

    return X

def simulate_multProc(drift, diff, underlyingProc, steps,
                     sims, seed, sampleSet, increments):
    """Apply EM. All procs are Levy. drift and diff[i] are func in 2 var."""
    #generate solution container and step size
    dt_, X = increments, np.zeros((steps+1, sims))
    X[0] = seed

    #generate samples from the underlying Levy Procs.
    numProcs = len(underlyingProc)
    dUnderlying = np.array((numProc, steps, sims))
    reqSims = steps*sims
    for i, Levy in enumerate(underlyingProc):
        dUnderlying[i] = Levy.sample(sims=reqSims, idx=dt_, shape=(steps, sims))

    #simulate solution
    for i, t in enumerate(sampleSet, 1):
        for j in range(numProcs):
            X[i] += diff[j](t, X[i-1]) * dUnderlying[j][i-1]
        X[i] = (X[i-1] + drift(t, X[i-1])*dt_)
        
    return X

def simulateSDE(drift, diff, underlyingProc, steps,
                sims, seed, sampleSet, increments, singleInc):
    dt_ = np.ones((steps,)) * increments if singleInc else increments
    X = np.zeros((steps+1, sims)); X[0] = seed

    numProc = len(underlyingProc)
    dUnderlying = np.array((numProc, steps, sims))
    reqSims = steps*sims
    for i, Levy in enumerate(underlyingProc):
        for j, inc in enumerate(dt_):
            dUnderlying[i][j] = Levy.sample(sims=reqSims, idx=inc,
                                            shape=(sims,))

    for i, t in enumerate(sampleSet, 1):
        for j in range(numProcs):
            X[i] += diff[j](t, X[i-1]) * dUnderlying[j][i-1]
        X[i] = (X[i-1] + drift(t, X[i-1])*dt_)
        
    return X
    
