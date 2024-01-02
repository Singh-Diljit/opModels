import scipy.integrate
import numpy as np

i = complex(0, 1)
def heston(S, K, v, r, q, T, a, b, c, cor, call=True):
    
    def phi(u):
        beta = a - i*u*c*cor
        d = np.sqrt(beta**2 + c**2*u*(u+i))
        g = (beta - d) / (beta + d)
        
        A_ = (a*b/c**2) * ((beta - d)*T - 2*np.log((g*np.exp(-d*T)-1)/(g-1))) 
        B_ = (beta - d)/c**2 * (1-np.exp(-d*T)) / (1-g*np.exp(-d*T))
        return np.exp(A_ + B_*v)

    logS = np.log(S/K) + (r-q)*T
    def trf(u):
        F = np.exp(i*u*k) * phi(u - i/2)
        return np.real(F) / (4*u**2 + 1)
        
    I = scipy.integrate.quad(trf, 0, np.inf)[0]
    value = S*np.exp(-q*T) - 4*K*np.exp(k/2-r*T)/np.pi * I
    
    if not call:
        value -= np.exp(-q*T)*S - np.exp(-r*T)*K
        
    return value
