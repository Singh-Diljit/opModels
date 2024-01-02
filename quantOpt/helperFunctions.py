"""A collection of functions used to aid more complicated files."""

from numpy import exp

def futureValue(presentVal, rate, time, coumpounded=float('inf')):
    """Return the future value.

    Parameters
    ----------
    presentVal : float
        Current value of asset.
    rate : float
        Interest rate, taken yearly. (2% is inputted as .02)
    time : float
        Time in years that interest rate will compound.
    coumpounded : float, optional
        Fraction of year the interest rate coumpounds.
    
    Returns
    -------
    futureValue() : float
        Future value of asset taking into account interest and time.
        
    Example(s)
    ----------
    >>> futureValue(100, .02, 5)
    >>> 110.51709180756477
    
    """
    if coumpounded == float('inf'):
        factor = exp(rate * time)
    else:
        timesCoumpounded = time / coumpounded
        factor = (1 + rate*coumpounded) ** (timesCoumpounded)
        
    return presentVal * factor

def discounted(futureVal, rate, time, coumpounded=float('inf')):
    """Return the rate discounted value.

    Parameters
    ----------
    futureVal : float
        Future value of asset.
    rate : float
        Interest rate, taken yearly. (2% is inputted as .02)
    time : float
        Time in years that interest rate will compound.
    coumpounded : float, optional
        Fraction of year the interest rate coumpounds.
    
    Returns
    -------
    discounted() : float
        Discounted value of asset taking into account interest and time.
        
    Example(s)
    ----------
    >>> discounted(100, .02, 5)
    >>> 90.48374180359595
    
    """
    if coumpounded == float('inf'):
        factor = exp(-rate * time)
    elif coumpounded != 0:
        timesCoumpounded = time / coumpounded
        factor = (1 + rate*coumpounded) ** (-timesCoumpounded)
    else: factor = 1
        
    return futureVal * factor

def discountedDiscrete(payments, paymentTimes, rate, coumpounded=float('inf')):
    """Return the rate discounted value of discrete payments.

    Parameters
    ----------
    payments : list
        Payout amounts.
    paymentTimes : list
        Payout schedule, time of each entry is time from now in years of payout.
    rate : float
        Time in years that interest rate will compound.
    coumpounded : float, optional
        Intervals the interest rate coumpounds.
    
    Returns
    -------
    value : float
        Discounted value of payments taking into account interest and payouts.
        
    Example(s)
    ----------
    >>> discountedDiscrete([10, 20, 5], [1, 2, 2.5], .1)
    >>> 29.316993157276258

    """
    return sum([discounted(p, rate, t, coumpounded)
                for p, t in zip(payments, paymentTimes)])

def expVal(probability, value):
    """Return the expected value of an event.

    Parameters
    ----------
    probability : float
        Likelyhood of occurance (between 0 and 1, inclusive).
    value : float
        Value of event.
    
    Returns
    -------
    expVal() : float
        Expected value of event.
        
    """
    return probability * value

def exerciseType(optionType):
    """Return if a contract is an American, European, or Bermuda option.

    This is used in a function where choices of input are:
        "American Call", "American Put", "European Call"
        "European Put", "Bermuda Call", "Bermuda Put"
    
    Parameters
    ----------
    optionType : str
        Type of option being priced.

    Returns
    -------
    (am, eu, be) : tuple (of bools)
        If the option is American, European, Bermuda, respectively.

    Example(s)
    ----------
    >>> exerciseType('American Call')
    >>> (True, False, False)
           
    """
    optionType = optionType.lower()
    am = 'american' in optionType
    eu = 'european' in optionType
    be = 'bermuda' in optionType
    
    return (am, eu, be)
    
def isCall(optionType):
    """Return if an option is a call (or put).
    
    Parameters
    ----------
    optionType : str
        Type of option being priced. Choices are: 
            "American Call", "American Put", "European Call"
            "European Put", "Bermuda Call", "Bermuda Put"

    Returns
    -------
    isCall() : bool
        If the option is a call.

    Example(s)
    ----------
    >>> isCall('American Call')
    >>> True
            
    """
    return True if 'call' in optionType.lower() else False

def overlapRange(points, x, N, fwd, eps=10**-4):
    """Return the intersection of a list of ranges and a list of multiples.

    Given a list points, [p_1, ..., p_M], and a list of
    multiples of x: [0, x, ...,(N-1)x], find all i s.t. there
    exists p_j in P and  p_j <= x*i < p_j + fwd, with eps accepted
    error in comparing floats.
    
    Parameters
    ----------
    points : list
        Non-decreasing list of floats.
    x : float
        Base value.
    N : int
        Total number of steps.
    fwd : float
        Defines range of each point.
    eps : float, optional
        Accepted error in comparing floats.
        
    Returns
    -------
    res : set
        Set of integers satisfying condition

    Example(s)
    ----------
    >>> overlapRange([1/10, 1/6, 1/5, 1/2], 1/36, 72, .005, eps=10**-4)
    >>> {18, 6}
    
    """
    res, P = set(), len(points)
    i, j = 0, 0
    pos = 0
    while i < N and j < P:
        if pos <= points[j] - eps:
            i += 1
            pos += x
        elif pos > points[j] + fwd + eps:
            j += 1
        else: #pos is within range
            res.add(i)
            i += 1
            pos += x

    return res
