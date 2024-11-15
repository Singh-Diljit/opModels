"""Optimized simulation for common SDE cases."""

import numpy as np

def simulate_oneProc(drift, diff, underlyingProc, seed, steps, sims,
                     sampleSet, uniformIncrement):
    """drift = c*X_t and diffusion = c_1*X_t.
    drift is given as just c, diff as c_1."""
    dt_, X = uniformIncrement, np.zeros((steps+1, sims))
    X[0] = seed
    reqSims = steps*sims
    dUnderlying = underlyingProc.sample(sims=reqSims, idx=dt_,
                                        shape=(steps, sims))
    for i, t in enumerate(sampleSet, 1):
        X[i] = X[i-1](1 + drift*dt_ + diff*dUnderlying[i-1])

    return X

def simulate_twoProc(drift, diff, underlyingProc, seed, steps, sims,
                     sampleSet, uniformIncrement):
    """drift = c*X_t and diffusion = c_1*X_t.
    drift is given as just c, diff as c_1."""
    dt_= uniformIncrement
    X, Y = np.zeros((2, steps+1, sims))
    X[0:,:] = seed
    Y[0] = seed
    reqSims = steps*sims
    dUnderlying = underlyingProc.sample(sims=reqSims, idx=dt_,
                                        shape=(steps, sims))
    for i, t in enumerate(sampleSet, 1):
        X[i] = X[i-1](1 + drift*dt_ + diff*dUnderlying[i-1])

    return X
