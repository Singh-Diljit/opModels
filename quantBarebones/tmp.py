
SP test class

class X:
    """Test BM class"""
    def __init__(self, S, r, q, v):
        self.S = S
        self.drift = r - q - (v**2)/2
        self.diff = v
    def sample(self, sims, idx, mag=0):
        A = self.diff*np.sqrt(idx)*np.random.normal(size=sims)
        if mag == 0:
            return self.S * np.exp(self.drift*idx + A)
        else:
            return mag * np.exp(self.drift*idx + A)


"""
dX.discretize(sims=sims, steps=steps, path)

path == True: ans = [res[0], ..., res[K]] (K = dX.dim)

               sim0  ...  simM 
                |          |
             | --- step 0 --- |
    res[i] = | --- ...... --- |
             | --- ...... --- |
             | --- step N --- |

path == False:

         | --- res[0][-1] --- |
   ans = | --- .......... --- |
         | --- .......... --- |
         | --- res[K][-1] --- |
        
"""
dX.discretize(sims=sims, steps=steps, path=False)[0]
