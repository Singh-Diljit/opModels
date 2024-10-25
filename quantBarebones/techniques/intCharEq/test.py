from price import integratePhi
from testModels import phiBSM, BSM

phi_1 = phiBSM(S=110, r=.1, T=.5, vol=.25, q=.004)
phi_2 = phiBSM(S=100, r=.08, T=.5, vol=.2, q=.004)


A = integratePhi(phi_1, S=110, K=107, r=.1, T=.5, q=.004, call=False)
#print(A)
(4.120882545489373, -0.30280916820133263)

A = integratePhi(phi_2, S=100, K=110, r=.08, T=.5, q=.004)
#print(A)
(3.3167691850158647, 0.3689885120328471)

A = integratePhi(phi_2, S=100, K=110, r=.08, T=.5, q=.004, call=False)
#print(A)
(9.203407625038103, -0.6310114879671529)

A = integratePhi(phi_2, S=100, K=90, r=.08, T=.5, q=.004, call=False)
#print(A)
(1.064584293450137, -0.13908873256331966)

"""Control group"""
A = BSM(110, 107, .1, .5, .25, .004, call=False, delta=True)
print(A)

A = BSM(100, 110, .08, .5, .2, .004, delta=True)
print(A)

A = BSM(100, 110, .08, .5, .2, .004, call=False, delta=True)
print(A)

A = BSM(100, 90, .08, .5, .2, .004, call=False, delta=True)
print(A)
