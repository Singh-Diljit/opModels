
# QuantFinance

This project implements a wide array of advanced models used in quantitative finance for option pricing and derivative evaluation. By combining theoretical models with practical numerical techniques, it demonstrates a deep understanding of financial modeling, stochastic processes, and computational methods. A key feature of this project is its ability to calculate **Implied Volatility (IV)** across various models using multiple approaches.

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Models and Techniques](#models-and-techniques)
  - [Option Pricing Models](#option-pricing-models)
  - [Stochastic Processes](#stochastic-processes)
  - [Graphical Analysis](#graphical-analysis)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Option Pricing Models**: Implementations of various option pricing models.
- **Stochastic Processes**: Tools for modeling and simulating stochastic processes.
- **Graphical Analysis**: Visualization tools for implied volatility and Greeks.
- **Performance Evaluation**: Functions for calculating and comparing model performance metrics.

## Installation

To install the necessary dependencies, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/QuantFinance.git
   cd QuantFinance
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Here’s a quick example of how to use the QuantFinance library to price an option using the Black-Scholes model:

```python
from qf.models.option import Option
from qf.stochastic.stock import Stock

# Create a stock and an option
stock = Stock(price=100, volatility=0.2, dividend_yield=0.01)
option = Option(stock=stock, strike_price=100, expiration=30, option_type='call')

# Calculate option price
price = option.calculate_price(model='BSM')
print(f"Option Price: {price:.2f}")

# Calculate Greeks
delta = option.calculate_greek('delta')
print(f"Delta: {delta:.4f}")
```

## Folder Structure

```
QuantFinance/
├── README.md
├── .gitignore
├── requirements.txt
├── setup.py
├── LICENSE
├── unittests/  # Placeholder for testing files
└── qf/
    ├── helperFunctions/
    │   ├── helperFuncs.py
    │   ├── moneyness.py
    ├── dividend/
    │   ├── Dividend.py
    │   ├── dividendHelper.py
    ├── stock/
    │   ├── Stock.py
    ├── time/
    │   ├── offline/
    │   │   ├── calander.py
    │   │   ├── generateEnumeration.py
    │   ├── timeHashes/
    │   │   ├── timeDicts.py
    │   │   ├── trDayTally.pickle
    │   ├── fastCalander.py
    │   ├── TradingTime.py
    ├── stochastic/
    │   ├── Index/
    │   │   ├── Index.py
    │   ├── StochProc/
    │   │   ├── SP.py
    │   ├── Processes/
    │   │   ├── BrownianMotion.py
    │   │   ├── CompoundPoisson.py
    │   │   ├── GammaProcess.py
    │   │   ├── Geometric.py
    │   │   ├── JumpDiffusion.py
    │   │   ├── VarianceGamma.py
    │   ├── StochDiffEq/
    │   │   ├── sSDE.py
    │   │   ├── sdeHelper.py
    │   │   ├── discretization.py
    ├── params/
    │   ├── params.py
    ├── techniques/
    │   ├── analytic/
    │   │   ├── BA/
    │   │   │   ├── greeks.py
    │   │   │   ├── IV.py
    │   │   │   ├── price.py
    │   │   ├── BSJ/
    │   │   │   ├── greeks.py
    │   │   │   ├── IV.py
    │   │   │   ├── price.py
    │   │   ├── BSM/
    │   │   │   ├── greeks.py
    │   │   │   ├── IV.py
    │   │   │   ├── price.py
    │   ├── FFT/
    │   │   ├── greeks.py
    │   │   ├── helperFuncs.py
    │   │   ├── IV.py
    │   │   ├── price.py
    │   ├── intCharEq/
    │   │   ├── greeks.py
    │   │   ├── IV.py
    │   │   ├── price.py
    │   ├── putCall/
    │   │   ├── putCallBounds.py
    │   ├── recBinom/
    │   │   ├── greeks.py
    │   │   ├── helperFuncs.py
    │   │   ├── IV.py
    │   │   ├── priceEU.py
    │   │   ├── priceAM.py
    │   │   ├── priceBE.py
    │   ├── recTrinom/
    │   │   ├── greeks.py
    │   │   ├── helperFuncs.py
    │   │   ├── priceEU.py
    │   │   ├── priceAM.py
    │   │   ├── priceBE.py
    │   ├── genBinom/
    │   │   ├── priceEU.py
    │   │   ├── priceAM.py
    │   │   ├── priceBE.py
    │   ├── monteCarlo/
    │   │   ├── SDE/
    │   │   │   ├── priceEU.py
    │   │   │   ├── priceAM.py
    │   │   ├── SP/
    │   │   │   ├── priceEU.py
    │   │   │   ├── priceAM.py
    ├── models/
    │   ├── Model.py
    │   ├── rate/
    │   │   ├── impliedRate.py
    │   ├── price/
    │   │   ├── BA.py
    │   │   ├── BSJ.py
    │   │   ├── BSM.py
    │   │   ├── CRR.py
    │   │   ├── Heston.py
    │   │   ├── recombTOPM.py
    │   │   ├── SVJ.py
    │   │   ├── tree.py
    │   │   ├── VG.py
    │   ├── prepPut/
    │   │   ├── prepetualPut.py
    ├── live/
    │   ├── IVsmile.py
    │   ├── computeRate.py
    ├── graphs/
    │   ├── BlacksApprox/
    │   │   ├── graphIV.py
    │   │   ├── graphGreeks.py
    │   │   ├── graphBSM.py
    │   │   ├── graphHelperBSM.py
    │   ├── BSM/
    │   │   ├── graphIV.py
    │   │   ├── graphGreeks.py
    │   │   ├── graphBSM.py
    │   │   ├── graphHelperBSM.py
    │   ├── CRR/
    │   │   ├── graph.py
    │   ├── TOPM/
    │   │   ├── graph.py
    ├── option/
    │   ├── Option.py
    │   ├── optionMethods.py
    │   ├── optionPayoffs.py
```

## Models and Techniques

### Option Pricing Models

#### 1. Black-Scholes Model (BSM)
The Black-Scholes model is one of the most widely used models for pricing European-style options. It assumes that stock prices follow a geometric Brownian motion and that markets are efficient.

**Pros**:
- **Analytical Solution**: Provides a closed-form solution for option pricing, making it easy to calculate prices and Greeks.
- **Simplicity**: The model's assumptions are straightforward, allowing for easy implementation.

**Cons**:
- **Assumptions**: It assumes constant volatility and interest rates, which may not hold true in real markets.
- **Limited to European Options**: It cannot accurately price American options, which can be exercised at any time.

#### 2. Heston Model
The Heston model is a popular stochastic volatility model that captures the changing volatility of the underlying asset over time. It incorporates mean reversion of volatility, making it more flexible than the Black-Scholes model.

**Pros**:
- **Realistic Volatility Dynamics**: Better reflects market behaviors, particularly during volatile periods.
- **Flexibility**: Can capture the smile effect observed in implied volatility.

**Cons**:
- **Complexity**: More complex than Black-Scholes, requiring numerical methods for implementation.
- **Parameter Estimation**: Estimating the parameters can be challenging and requires historical data.

#### 3. Binomial Models (CRR and Recombining TOPM)
Binomial models use a discrete-time framework to model the price movements of the underlying asset. The Cox-Ross-Rubinstein (CRR) model is a specific type of binomial model commonly used for option pricing.

**Pros**:
- **Versatile**: Can price American options since it allows for early exercise.
- **Intuitive**: The tree structure makes it easy to understand and visualize price movements.

**Cons**:
- **Computationally Intensive**: Requires more computations as the number of time steps increases.
- **Discretization Errors**: The accuracy depends on the number of time steps; too few can lead to inaccurate pricing.

### Stochastic Processes

#### 1. Geometric Brownian Motion (GBM)
GBM is a continuous-time stochastic process that models stock prices, assuming that they follow a random walk with drift. It’s the foundation of the Black-Scholes model.

**Pros**:
- **Simplicity**: Easy to implement and understand, making it suitable for educational purposes.
- **Closed-Form Solutions**: Provides closed-form solutions for option pricing.

**Cons**:
- **Assumption of Constant Volatility**: May not accurately represent real market conditions where volatility varies.
- **No Jumps**: Does not account for sudden market movements.

#### 2. Jump Diffusion Models
These models incorporate sudden, unexpected changes (jumps) in stock prices, in addition to the continuous price movements described by GBM.

**Pros**:
- **Captures Market Behavior**: Better reflects real-world market conditions, especially during earnings reports or economic announcements.
- **Flexibility**: Can model both the diffusion and jump components of price movements.

**Cons**:
- **Complexity**: More complicated to implement and require careful calibration of jump parameters.
- **Numerical Methods**: Often necessitate numerical approaches for option pricing.

### Graphical Analysis

QuantFinance includes visualization tools to help analyze option prices, implied volatility, and the behavior of financial models.

- **Implied Volatility Surface**: Visualizes how implied volatility changes with different strikes and maturities.
- **Greeks Analysis**: Graphs the sensitivities of option prices to various parameters, helping traders make informed decisions.

## Contributing

Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request. Ensure that your code follows the style guidelines and is well-documented. You can also open an issue to discuss potential improvements or new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

For any inquiries or feedback, please reach out to [Your Name](mailto:your.email@example.com).
