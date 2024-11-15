import numpy as np
import matplotlib.pyplot as plt

class Option:
    def __init__(self, 
                 stock, 
                 strike,
                 maturity,
                 rate,
                 payOff='European' 
                 call=True, 
                 model=None):

        self.stock = stock
        self.strike = strike
        self.rate = rate
        self.maturity = maturity
        self.payOff = style.lower()
        self.call = call; self.put = not self.call
        self.model = model

    @property
    def initData(self):
        """Labled inputs to __init__ to this instance."""
        className = 'Option'
        intiData_ = stock.initData
        initDataNew_ = [
            ('strike',   self.strike),
            ('rate',     self.rate),
            ('maturity', self.maturity),
            ('payOff',   self.payOff),
            ('call',     self.call),
            ('model',    self.model.name),
            ]
        
        return className, initData_
        
    def __repr__(self):
        """Return repr(self)"""
        return showData.makeRepr(self.initData)
    
    def price(self) -> float:
        """
        Calculates the option price based on the associated model.

        Returns:
        --------
        float
            The calculated option price.
        """
        if not self.model.closed_form_solution:
            raise NotImplementedError("Non-closed-form solutions require numerical methods.")
        
        # Example pricing logic for Black-Scholes (closed form)
        from scipy.stats import norm
        
        S = self.stock.price_history[-1]  # Current stock price
        K = self.strike
        r = self.stock.risk_free_rate
        T = self.maturity
        sigma = self.stock.volatility_history[-1]  # Current volatility
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if self.option_type == 'call':
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif self.option_type == 'put':
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            raise ValueError("Invalid option type: must be 'call' or 'put'.")

    def greeks(self) -> dict:
        """
        Calculates the Greeks for the option.

        Returns:
        --------
        dict
            A dictionary of calculated Greeks: delta, gamma, theta, vega, rho.
        """
        # Greeks calculation (example for Black-Scholes model)
        S = self.stock.price_history[-1]
        K = self.strike
        r = self.stock.risk_free_rate
        T = self.maturity
        sigma = self.stock.volatility_history[-1]
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        delta = norm.cdf(d1) if self.option_type == 'call' else norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * norm.cdf(d2 if self.option_type == 'call' else -d2))
        vega = S * norm.pdf(d1) * np.sqrt(T)
        rho = K * T * np.exp(-r * T) * (norm.cdf(d2) if self.option_type == 'call' else -norm.cdf(-d2))
        
        return {"delta": delta, "gamma": gamma, "theta": theta, "vega": vega, "rho": rho}

    def implied_volatility(self, market_price: float) -> float:
        """
        Calculates the implied volatility based on the market price of the option.

        Parameters:
        -----------
        market_price : float
            The observed market price of the option.

        Returns:
        --------
        float
            The implied volatility.
        """
        from scipy.optimize import brentq

        def bs_price(sigma):
            self.stock.volatility_history[-1] = sigma
            return self.price() - market_price

        return brentq(bs_price, 1e-6, 4.0)  # Bound between low and high volatilities

    def graph_price(self, steps=100):
        """
        Plots the option price as a function of the underlying stock price.
        """
        prices = []
        stock_prices = np.linspace(0.5 * self.stock.price_history[-1], 1.5 * self.stock.price_history[-1], steps)
        for price in stock_prices:
            self.stock.price_history[-1] = price
            prices.append(self.price())
        
        plt.plot(stock_prices, prices, label='Option Price')
        plt.xlabel('Stock Price')
        plt.ylabel('Option Price')
        plt.title('Option Price vs Stock Price')
        plt.legend()
        plt.show()

    def graph_greeks(self, greek: str, steps=100):
        """
        Plots a Greek as a function of the underlying stock price.
        """
        values = []
        stock_prices = np.linspace(0.5 * self.stock.price_history[-1], 1.5 * self.stock.price_history[-1], steps)
        for price in stock_prices:
            self.stock.price_history[-1] = price
            values.append(self.greeks()[greek])
        
        plt.plot(stock_prices, values, label=f'{greek.capitalize()}')
        plt.xlabel('Stock Price')
        plt.ylabel(f'{greek.capitalize()}')
        plt.title(f'{greek.capitalize()} vs Stock Price')
        plt.legend()
        plt.show()
