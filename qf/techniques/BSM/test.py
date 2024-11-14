from price import BSM

A = BSM(110, 107, .1, .5, .25, .004, call=False, delta=True)
print(A)

A = BSM(100, 110, .08, .5, .2, .004, delta=True)
print(A)

A = BSM(100, 110, .08, .5, .2, .004, call=False, delta=True)
print(A)

A = BSM(100, 90, .08, .5, .2, .004, call=False, delta=True)
print(A)

A = BSM(36, 40, .06, 1, .2, .06, call=False)
print(A)
