from price import integratePhi
import numpy as np

#current phi
def phi(S, r, T, v, q, kappa, theta, xi, rho):
    xiSq = xi**2
    varSq = v**4
    lnS = np.log(S)
    
    A = lambda u: kappa - 1j*u*rho*xi
    d = lambda u: np.sqrt(A(u)**2 + (u**2 + 1j*u)*xiSq)
    g = lambda u: (A(u)-d(u)) / (A(u)+d(u))

    twiD = lambda u: np.exp(-T * d(u))
    lnRat = lambda u: np.log(1 - g(u)*twiD(u)) - np.log(1 - g(u))
    ratio = lambda u: (A(u)-d(u)) / xiSq

    lnPhi = lambda u: (1j*u*lnS + 1j*u*(r-q)*T + ratio(u)*theta*kappa*T
                       - 2*theta*kappa * lnRat(u)/xiSq
                       + varSq*ratio(u) * (1-twiD(u)) / (1-g(u)*twiD(u)))
    phi = lambda u: np.exp(lnPhi(u))
    return phi


S, K = 100, 100
r, T, q = .08, 1, .008

v, a, b, c, cor = .05, 1, .04, .2, -.5

phiHes = phi(S, r, T, v, q, a, b, c, cor)

A = integratePhi(phiHes, S, K, r, T, q, call=True)
print(A)
