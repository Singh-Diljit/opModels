import pandas as pd
import yFinance as yf

def optChain(symbol, date):
    """Return a simplified option-chain for a symbol at a certain expiry."""

    symb = yf.Ticker(symbol)
    chain = symb.option_chain(date)
    chain = pd.DataFrame().append(chain.calls).append(chain.puts)

    chain['CALL'] = chain['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    chain[['bid', 'ask', 'strike']] = (
        chain[['bid', 'ask', 'strike']].apply(pd.to_numeric))
    chain['mark'] = (chain['bid'] + chain['ask']) / 2
    
    #Drop unnecessary and meaningless columns
    chain = chain.drop(columns =
                       ['contractSize', 'currency', 'change', 'bid', 'ask',
                        'openInterest', 'impliedVolatility',
                        'contractSymbol' ,'percentChange', 'lastTradeDate',
                        'lastPrice', 'inTheMoney'])
    return chain

def getRiskFreeRate(T=1):
    """Return the put-call parity implied risk free rate via SPX contracts.
    
    Put-call parity is empirically accurate in highly liquid markets
    when the underlying is trading around the strike price ('at the money').
    This function uses that fact to emprically find the risk-free rate.
    
    Becuase the risk-free rate empirically varies as you look further
    into the future, this function is robust to using different
    ranges of time, though they are estimated to conform to the options chain.
    Theoritically any shift in T should not make a difference, but as noted
    it does when T ranges over a number of months/years. This slight shift
    of a few days has neglible affect on the implied riskfree rate.
    
    Parameters
    ----------
    T : float, optional
        Rough time until expiry of contracts used in implied rate calculations.
        
    Returns
    -------
    rate : float
        Realized risk-free rate.
    
    Example(s)
    ----------
    >>> getRiskFreeRate()
    >>>
    
    >>> getRiskFreeRate(2)
    >>>
    
    """
    #spx = yf.Ticker('^SPX')
    spx = yf.Ticker('META')
    optionDates = spx.options
    startDate = tuple(int(x) for x in optionDates[0].split('-')[::-1])
    endDate = calander.elapsedDays(T*365, startDate)
    endDay, endMonth, endYear = endDate
    estDate = ''

    #Get rough options expiry date
    for date in optionDates:
        year, month, day = [int(x) for x in date.split('-')]
        if year == endYear and month == endMonth: #Fix to closest date
            estDate = (day, month, year)
            spxDate = date

    estDate, spxDate = (17, 1, 2025), '2025-01-17' #Delete
    T_ = calander.dateToYears(startDate, estDate)
    
    #Get spot price
    spotPr = spx.history(interval='1m', period='1d')['Close'][-1]
    
    #Find prices of ATM calls and puts
    chain = optChain('META', spxDate)
    strikePr, diff = 0, float('inf') #^SPX

    for row_, strike_ in enumerate(chain['strike']):
        if abs(strike_ - spotPr) < diff:
            diff = abs(strike_ - spotPr)
            strikePr = strike_
            row = row_

    diff = float('inf')
    for row_, strike_ in enumerate(chain['strike']):
        if abs(strike_ - strikePr) < diff and not chain.iloc[row_]['CALL']:
            diff = abs(strike_ - strikePr)
            rowP = row_
            
    callPr = chain.iloc[row]['mark']
    putPr = chain.iloc[rowP]['mark']
    emp = putCallParity(callPr, spotPr, strikePr, 0.048, T_, 0)
    #print(putPr, emp)
    #avg div of .0184 every quarter
    finalDiv = 4*int((T_)//1)
    rate = impliedRate(callPr, putPr, spotPr, strikePr, T_,
                       [.0184/4]*finalDiv,
                       divPayout=[.25*i for i in range(1, finalDiv)])
    
    return rate
