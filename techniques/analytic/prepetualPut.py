"""Price a perpetual put."""

def perpetualPut(S, K, r, vol, q):
    """Price an American put that never expires.

    Parameters
    ----------
    S   : float : Current price of stock.
    K   : float : Strike price of the option.
    r   : float : Annualized risk-free interest rate, continuously compounded.
    vol : float : Volatility of the stock.
    q   : float : Continuous dividend rate.

    Returns
    -------
    value : float : Value of put.

    Notes
    -----
    Model assumes r != 0, mathematically this is becuase we are solving
    a quadtratic of the form (x^2 + bx + c) and r = 0 implies the discriminant
    the trivial constant term.

    Example(s)
    ---------
    >>> perpetualPut(S=150, K=100, r=.08, vol=.2, q=.005)
    >>> 1.8344292693352149
    
    """
    volSq = vol ** 2
    
    #Solve the associated quadratic
    const = r - q - volSq/2
    discr = const**2 + 2*r*volSq
    root = -(const + discr**.5) / volSq

    #Solution to ODE
    mnRoot = root - 1
    mul = -K / mnRoot
    base = mnRoot/root * S/K
    value = mul * (base ** root)
    
    return value
