"""Functions to generate trading day enumeration between 2000 and 2050."""

from calander import tradingDays, enumDate, enumWeekends, enumDateTuple_, tradingHolidays, enumExceptions
from numpy import datetime64
import pickle

def gen_isLeap(year):
    """Return if leap year, 1999 < year < 2100"""
    return year % 4 == 0

def gen_numLeaps(year1, year2=2000):
    """Return the number of leap years in [min_Year, max_Year).
        Valid for 2000 <= min_Year <= max_Year <= 2100"""
    mn, mx = min(year1, year2), max(year1, year2) - 1
    firstLeap = mn + (-mn % 4)
    return 0 if firstLeap > mx else 1 + (mx - firstLeap)//4

def gen_enumYears(yearEnd=2049):
    """Return dict with enumYears[year] = cal days in [1/1/2000, 1/1/year)."""
    enumYears = {y: (y-2000)*365 + gen_numLeaps(y) + 1
                 for y in range(2000, yearEnd+1)}
    
    return enumYears

def gen_trDaysInYear(yearEnd=2049):
    """ trDaysInYear[year] = # trading days in [1/1/year, 12/31/year]."""
    trDaysInYear = {}
    for year in range(2000, yearEnd + 1):
        sD, eD = datetime64(str(year)), datetime64(f'{year}-12-31')
        trDaysInYear[year] = tradingDays(sD, eD)

    return trDaysInYear

def gen_trDayTally(yearEnd=2049):
    Y = yearEnd + 1
    daysFrom2000 = (Y - 2000)*365 + gen_numLeaps(Y + 1) + 1
    trDayTally = {i: 0 for i in range(daysFrom2000+1)}

    i = 0
    for year in range(2000, Y):
        sD, eD = datetime64(str(year)), datetime64(str(year+1))
        daysInYear = 366 if gen_isLeap(year) else 365
        weekends = enumWeekends(year)
        holidays = {enumDateTuple_(x) for x in tradingHolidays(sD, eD).values()}
        enumedDaysOff = weekends | holidays
        for j in range(daysInYear):
            i += 1
            trDayTally[i] = trDayTally[i-1]
            if not (j in enumExceptions[year] or j in enumedDaysOff):
                trDayTally[i] += 1
            
    return trDayTally

def write_trDayTally(yearEnd=2049):
    trDayTally = gen_trDayTally(yearEnd)
    with open('trDayTally.pickle', 'wb') as f: 
        pickle.dump(trDayTally, f, pickle.HIGHEST_PROTOCOL)

write_trDayTally()
