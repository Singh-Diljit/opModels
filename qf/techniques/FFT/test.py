"""test"""

import numpy as np
from price import prFFT
from testModels import *

"""Control group"""
phi_1 = phiBSM(S=110, r=.1, T=.5, vol=.25, q=.004)
#A = integratePhi(phi_1, S=110, K=107, r=.1, T=.5, q=.004, call=False)
(4.120882545489373, -0.30280916820133263)

phi_2 = phiBSM(S=100, r=.08, T=.5, vol=.2, q=.004)
#A = integratePhi(phi_2, S=100, K=110, r=.08, T=.5, q=.004)
(3.3167691850158647, 0.3689885120328471)

#A = integratePhi(phi_2, S=100, K=110, r=.08, T=.5, q=.004, call=False)
(9.203407625038103, -0.6310114879671529)

#A = integratePhi(phi_2, S=100, K=90, r=.08, T=.5, q=.004, call=False)
(1.064584293450137, -0.13908873256331966)

"""FFT Price"""
phi_1 = phiBSM(S=110, r=.1, T=.5, vol=.25, q=.004)
A = prFFT(phi_1, S=110, K=107, r=.1, T=.5, q=.004, call=False)[0]
#print(A)
4.121458188841389


phi_2 = phiBSM(S=100, r=.08, T=.5, vol=.2, q=.004)
A = prFFT(phi_2, S=100, K=110, r=.08, T=.5, q=.004)[0]
#print(A)
3.317255748918776

A = prFFT(phi_2, S=100, K=110, r=.08, T=.5, q=.004, call=False)
#print(A)
#(9.203894188941014,
# array([ 9.20389419, 10.80948423, 12.69935053, ...,  6.51198708,
#        7.07570943,  7.95676429]))

A = prFFT(phi_2, S=100, K=90, r=.08, T=.5, q=.004, call=False)
#print(A)
#(1.0654041381043378,
# array([ 1.06540414,  3.54253946,  5.7179566 , ..., -6.73580893,
#       -4.25734426, -1.59219072]))

"""FFT IV"""
from IV import IV

#phi_1 = phiBSM_v(S=110, r=.1, T=.5, q=.004)
#phi_2 = phiBSM_v(S=100, r=.08, T=.5, q=.004)

#Ans is .25
phi_1 = phiBSM_v(S=110, r=.1, T=.5, q=.004)
A = IV(4.121458188841389, phi_1, S=110, K=107, r=.1, T=.5, q=.004, call=False)
#print(A)
0.2500000270522303

#Ans is .2
phi_2 = phiBSM_v(S=100, r=.08, T=.5, q=.004)
A = IV(3.317255748918776, phi_2, S=100, K=110, r=.08, T=.5, q=.004)
#print(A)
0.19999900977112453

#Ans is .2
A = IV(9.203894188941014, phi_2, S=100, K=110, r=.08, T=.5, q=.004, call=False)
#print(A)
0.1999990097711245

#Ans is .2
A = IV(1.0654041381043378, phi_2, S=100, K=90, r=.08, T=.5, q=.004, call=False)
#print(A)
0.1999995804170147

