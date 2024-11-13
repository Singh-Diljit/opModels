"""Fast Calander Functions For 2000-2050."""

import pickle
import timeDicts as *
from calander import dt64_tuple
from generateEnumeration import gen_isLeap, gen_numLeaps

startD = np.datetime64('2000-1-1')

def yearFromEnum(i):
    est = 2000 + i // 365
    if enumYears[est] > i:
        return est + 1
    elif enumYears[est] < i < enumYears[est+1]:
        return 
    
def days(year):
    """# of calander or trading days in [1/1/year, 12/31/year]"""
    return trDaysinYear[year]

with open("trDayTally.pickle", 'rb') as trData:
    trDaysTally = pickle.load(trData)

##MAIN FUNCTION
def enumDate(date):
    """Return i s.t. date = 1/1/2000 +_{trading} i days

    date: datetime64

    """
    return trDaysTally[date-startD]

def isTradingDay(i):
    return i in trDaysTally

def trDays(i, j):
    """Return # of trading days in [min_date, max_date2].

    note i, j are the enumDates of two dates.
    """
    mx, mn = max(i, j), min(i, j)
    return trDaysTally[mx+1] - trDaysTally[mn]

def trDaysYr(year1, year2):
    """Return # of trading days in [1/1/year1, 1/1/year2]."""
    i, j = enumYears[year1], enumYears[year2]
    return trDays(i, j)

def fracYear(i):
    """Return (Number of tr Days In [1/1/year, date]) / (days in year)."""
    year = yearFromEnum(i)
    yrStart = enumYears[year]
    num = trDaysTally[i+1] - trDaysTally[yrStart]
    return num / days(year)

def futDateEnum(i, T):
    """Return enumDate(date + T)."""
    day, month, year = date
    portionDone = fracYear(i)
    i_t = enumDate(date, tradingYear)

    endYr = (year + portionDone + T) // 1
    dYr = endYr - year + 1
    avgDays = (trDaysYr(year, endYr + 1)) / (dYr + 1)
    res = i + avgDays*T
        
    return res
            
def oneDay(date, T, tradingYear=False):
    """Return portion of time from [date, date+T] one day is."""
    i, j = enumDate(date), futDateEnum(date, T, tradingYear)
    mx, mn = max(i, j), min(i, j)
    totDays = trDaysTally[mx+1] - trDaysTally[mn]
    
    return 1 / totDays
