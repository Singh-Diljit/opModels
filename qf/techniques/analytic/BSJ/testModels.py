"""test models"""

from scipy.stats import norm
import scipy.integrate
import numpy as np

def BSM(S, K, r, T, vol, q, call=True, delta=False):
    rateTime, divTime = r * T, q * T
    rateDisc, divDisc = np.exp(-rateTime), np.exp(-divTime)
    adjS, adjK = S * divDisc, K * rateDisc
    
    stdDev = vol * np.sqrt(T)
    logChange = np.log(S/K) + (rateTime - divTime)
    d1 = (logChange)/stdDev + stdDev/2
    d2 = d1 - stdDev
    
    if call:
        cdf_d1, cdf_d2 = norm().cdf(d1), norm().cdf(d2)
        value = cdf_d1*adjS - cdf_d2*adjK
        delta_ = cdf_d1

    else:
        cdf_neg_d2, cdf_neg_d1 = norm().cdf(-d2), norm().cdf(-d1)
        value = cdf_neg_d2*adjK - cdf_neg_d1*adjS
        delta_ = -cdf_neg_d1

    return (value, delta_) if delta else value

def integratePhi(phi, S, K, r, T, q, call=True):
    twPhi = lambda u: phi(u-1j) / phi(-1j)

    k = np.log(K)
    trfPhi = lambda u: np.imag(np.exp(-1j*u*k) * phi(u)) / u
    trfTwi = lambda u: np.imag(np.exp(-1j*u*k) * twPhi(u)) / u
    
    A = scipy.integrate.quad(trfPhi, 0, np.inf)[0]
    B = scipy.integrate.quad(trfTwi, 0, np.inf)[0]

    pITMCall = .5 + A/np.pi
    deltaCall = .5 + B/np.pi

    adjS, adjK = S*np.exp(-q*T), K*np.exp(-r*T)
    if call:
        pr = adjS*deltaCall - adjK*pITMCall
        delta = deltaCall

    else: #pricing a put
        pr = adjK*(1 - pITMCall) - adjS*(1-deltaCall)
        delta = deltaCall - 1

    return pr, delta

def phiBSJ(S, r, T, v, q, jumpInt, jumpMean, jumpVar):
    """
    jumpInt : float : Intesity of jump process. (lambda)
    ln(1+J) = N(jumpMean, jumpVar)
    jumpMean: float : Mean of each jump
    jumpVar : float : Variance of 
    """
    jVarHalf = jumpVar/2
    jTerm = jumpMean + jVarHalf
    jBar = np.exp(jTerm) - 1
    
    driftComp = lambda u: r - q - v**2 - jumpInt*jBar
    expTerm = lambda u: np.exp(-jVarHalf*u**2 + 1j*jumpMean*u - 1)
    lnPhi = lambda u: -.5*T*(u*v)**2 + 1j*u*driftComp(u) + jumpInt*expTerm(u)

    phi = lambda u: np.exp(lnPhi(u))

    return phi

def phiBSJ1(S, r, T, v, q, lam, mu, delta):
    #lam = jumpInt
    #mu = jumpMean
    #delta = jumpVar

    alpha = r - q
    a = delta**2/2
    k = -1 + np.exp(mu + a)
    A = lambda u: -1 + np.exp(1j*u*mu-u**2*a)
    
    C = v**2/2
    B = alpha - C - lam*k

    psi = lambda u: lam*A(u) + 1j*u*B - u**2*C 

    phi = lambda u: np.exp(T * psi(u))
    
    return phi

def phiBSM(S, r, T, vol, q):
    halfVar = vol**2 / 2
    drft = np.log(S) + (r - q - halfVar)*T
    phi = lambda u: np.exp(1j*u*drft - halfVar*T*u**2)

    return phi

#ONLINE
import math
def mertonJ(S, K, r, T, vol, lam, v, m, N=50, call=True):
    p = 0
    for k in range(N):
        r_k = r - lam*(m-1) + (k*np.log(m) ) / T
        sigma_k = np.sqrt( vol**2 + (k* v** 2) / T)
        k_fact = math.factorial(k)
        A = (np.exp(-m*lam*T) * (m*lam*T)**k / (k_fact))
        B = BSM(S, K, r_k, T, sigma_k, 0, call)        
        p += A*B
    
    return p
