"""Discretization of SDEs."""

##
Include a reflection principle for e.g. vol. see maybe useful mcm file
Graph path - seperate func all toghter
    in EM(..., full, end, poi):
        full = as is
        end = np.mean(X[-1])
        POI = chnage linspace to make sure points are hit -- maybe
        irregular intervals then really just a bunch of these
        so just glue end togther.
MCM(func, X):
    put/call easy this way
    even asain options etc
        
##

def eulerMaruyama_type1(f, g, Y, steps, sims, X_start, start=0, end=1):
    """Apply EM when dX_t = f(t, X)dt + g(t, X)dY_t for Levy process Y."""
    dt_, X = (end-start)/steps, np.zeros((steps+1, sims))  
    X[0] = X_start
    dY_ = Y.samplePoint(dt, shape=(steps, sims))
    for i in range(1, steps):
        t = i*dt + start
        X[i] = X[i-1] + f(t, X[i-1])*dt_ + g(t, X[i-1])*dY_[i-1]
        #X[:,i+1] += X[:,i] + f(t, X[:,i])*dt_ + g(t, X[:,i])*dY_[:,i]
        
    return X

def eulerMaruyama_type2(f, g, Y, Z, steps, sims, X_start, start=0, end=1):
    """Apply EM when dX_t = f(t, X)dt + g(t, X)dY_t + h(t, X)dZ_t
        for Levy process Y and Z."""
    dt_, X = (end-start)/steps, np.zeros((steps+1, sims))  
    X[0] = X_start
    dY_ = Y.samplePoint(dt, shape=(steps, sims))
    dZ_ = Z.samplePoint(dt, shape=(steps, sims))
    for i in range(1, steps+1):
        t = i*dt + start
        X[i] = (X[i-1]
              + f(t, X[i-1])*dt_
              + g(t, X[i-1])*dY_[i-1]
              + h(t, X[i-1])*dZ_[i-1])
        
    return X

def eulerMaruyama_type3(funcs, procs, steps, sims, X_start, start=0, end=1):
    """Apply EM when dX_t = f(t, X)dt + sum_j g_j(t, X)dY^(j)_t
        for Levy process Y^(j).

    funcs = drift, then g_1, ...., g_N for g_i the diff

        """
    dt_, X = (end-start)/steps, np.zeros((steps+1, sims))  
    X[0] = X_start
    dP = [p.samplePoint(dt, shape=(steps, sims)) for p in procs]
    for i in range(steps-1):
        X[:, i+1] += X[:,i]
        t = i*dt + start
        for j, f in enumerate(funcs):
            X[:, i+1] += f(t, X[:,i]) * dP[j][i]
        
    return X

###REQUIRES when calling funcs make them into np.arrays. <-that is the case!
def eulerMaruyama_type4(drift, diff, Y, steps, sims, X_start, start=0, end=1):
    """Apply EM when dX_t = f_1(t, X)dt + g_1(t, X)dY_t for Levy process Y.
                     dY_t = f_2           g_2       dY_t"""
    dt_, X = (end-start)/steps, np.zeros((2, steps+1, sims))  
    X[0] = X_start
    dY_ = Y.samplePoint(dt, shape=(2, steps, sims))
    for i in range(1, steps):
        t = i*dt + start
        X[i] = X[i-1] + drift(t, X[i-1])*dt_ + diff(t, X[i-1])*dY_[i-1]
        #X[:,i+1] += X[:,i] + f(t, X[:,i])*dt_ + g(t, X[:,i])*dY_[:,i]
        
    return X

###REQUIRES when calling funcs make them into np.arrays. <-that is the case!
def eulerMaruyama_type5(drift, diff, Y, Z, steps, sims, X_start, start=0, end=1):
    """Apply EM when dX_t = f_1(t, X)dt + g_1(t, X)dY_t + Z for Levy process Y.
                     dY_t = f_2           g_2       dY_t +Z"""
    dt_, X = (end-start)/steps, np.zeros((steps+1, sims, 2))  
    X[0] = X_start
    dim_ = (steps, sims, 2)
    dP = np.dstack(Y.samplePoint(dt, shape=dim_, Z.samplePoint(dt, shape=dim_))
    for i in range(1, steps+1):
        t = i*dt + start
        X[i] = (X[i-1]
              + drift(t, X[i-1])*dt_ + np.sum(diff(t, X[i-1])*dP[i-1], axis=0)
        
    return X

def eulerMaruyama_type6(drift, diff, P, steps, sims, X_start, start=0, end=1):
    """Apply EM when dX_t = f_1(t, X)dt +sum for Levy process Y.
                     for arb many SDE"""
    D = len(drift) #number SDEs
    dt_, X = (end-start)/steps, np.zeros((steps+1, sims, D))
    X[0] = X_start
    dim_ = (steps, sims, D)
    dP = np.dstack([p.samplePoint(dt, shape=dim_) for p in P])
    for i in range(1, steps+1):
        t = i*dt + start
        X[i] = (X[i-1]
              + drift(t, X[i-1])*dt_ + np.sum(diff(t, X[i-1])*dP[i-1], axis=0)
        
    return X

applyEM = {
    (1,1): EM_11,
    (1,2): EM_12,
    (2,1): EM_21,
    (2,2): EM_22}

def eulerMaruyama(..., type_):
    return applyEM[type_](...)
