"""Implement SDEs with restricted generality but increased optimazation."""

import numpy as np
import matplotlib.pyplot as plt

class SimpleSDE2:
    def __init__(self, S_0, v_0, r, q, kappa, theta, xi, rho, jumpProc=None):
        
        self.driftS = r-q
        self.shift_v = kappa*theta
        self.drift_v = -kappa
        self.scalBM_v = xi
        self.cov = [[1, rho], [rho, 1]]
        self.seed = [S_0, v_0]
        self.jumpProc = jumpProc
        
    def simulate(self, sims, steps, start=0, end=1):
        dt = (end-start)/steps; dtRoot = np.sqrt(dt)
        
        S = np.zeros((steps+1, sims)); S[0] = self.seed[0]
        v = np.zeros((steps+1, sims)); v[0] = self.seed[1]
        dW = np.random.multivariate_normal([0,0], self.cov, (steps, sims))*dtRoot
        dWS, dWv = dW[:,:,0], dW[:,:,1]
        if self.jumpProc is not None:
            J = self.jumpProc.sample(steps*sims, dt, (steps, sims))
        else:
            J = np.zeros((steps, sims))

        mulS = 1 + self.driftS*dt
        shift = self.shift_v*dt
        mulv = 1 + self.drift_v*dt
        for i in range(1, steps+1):
            rootv = np.sqrt(v[i-1])
            S[i] = S[i-1]*mulS + S[i-1]*rootv*dWS[i-1] + J[i-1]
            v[i] = np.abs(shift + v[i-1]*mulv + self.scalBM_v*rootv*dWv[i-1])
            
        return S, v
    
    def graph(self, sims, steps, start=0, end=1):
        pathS, pathV = self.simulate(sims,steps, start, end)
        times = np.linspace(start, end, steps+1)
        # Plot stock price paths
        plt.figure(figsize=(12, 6))
        mxPathsToShow = min(10, steps)
        for sim in range(min(10, pathS.shape[1])):
            plt.plot(times, pathS[:, sim], lw=1)
        plt.title("Sample Paths of Stock Price (Heston Model)")
        plt.xlabel("Time")
        plt.ylabel("Stock Price")
        plt.grid()
        plt.show()
        plt.savefig("stock_paths.png")  # Save figure
        plt.close()  # Close the figure to free resources
        
        # Plot variance paths
        plt.figure(figsize=(12, 6))
        for sim in range(min(10, pathV.shape[1])):
            plt.plot(times, pathV[:, sim], lw=1)
        plt.title("Sample Paths of Variance (Heston Model)")
        plt.xlabel("Time")
        plt.ylabel("Variance")
        plt.grid()
        plt.show()
        plt.savefig("variance_paths.png")  # Save figure
        plt.close()
        
if __name__ == "__main__":
    t = SimpleSDE2(100, .05, .08, 0.01, 3, .02, .9, .5)
    t.graph(50, 1000)
