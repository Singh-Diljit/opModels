"""Collection of time related functions."""

from numpy import datetime64
import numpy as np
from dataclasses import dataclass

monthToInt = {
    'JAN' : 1,
    'FEB' : 2,
    'MAR' : 3,
    'APR' : 4,
    'MAY' : 5,
    'JUN' : 6,
    'JUL' : 7,
    'AUG' : 8,
    'SEP' : 9,
    'OCT' : 10,
    'NOV' : 11,
    'DEC' : 12}
    
intToMonth = {
    1 : 'JAN',
    2 : 'FEB',
    3 : 'MAR',
    4 : 'APR',
    5 : 'MAY',
    6 : 'JUN',
    7 : 'JUL',
    8 : 'AUG',
    9 : 'SEP',
    10 : 'OCT',
    11 : 'NOV',
    12 : 'DEC'}

months365 = {
    'JAN' : 31,
    'FEB' : 28,
    'MAR' : 31,
    'APR' : 30,
    'MAY' : 31,
    'JUN' : 30,
    'JUL' : 31,
    'AUG' : 31,
    'SEP' : 30,
    'OCT' : 31,
    'NOV' : 30,
    'DEC' : 31}

months366 = {
    'JAN' : 31, 
    'FEB' : 29,
    'MAR' : 31,
    'APR' : 30,
    'MAY' : 31,
    'JUN' : 30,
    'JUL' : 31,
    'AUG' : 31,
    'SEP' : 30,
    'OCT' : 31,
    'NOV' : 30,
    'DEC' : 31}

orderingOfWeek = {
    0 : 'SUN',
    1 : 'MON', 
    2 : 'TUE', 
    3 : 'WED', 
    4 : 'THU', 
    5 : 'FRI', 
    6 : 'SAT'}

orderingOfDays = {
    'SUN' : 0,
    'MON' : 1, 
    'TUE' : 2, 
    'WED' : 3, 
    'THU' : 4, 
    'FRI' : 5, 
    'SAT' : 6}

abbreviationToFull = {
    'SUN' : 'Sunday',
    'MON' : 'Monday',
    'TUE' : 'Tuesday',
    'WED' : 'Wedensday',
    'THU' : 'Thursday',
    'FRI' : 'Friday',
    'SAT' : 'Saturday',
    'JAN' : 'January',
    'FEB' : 'Febuary',
    'MAR' : 'March',
    'APR' : 'Arpil',
    'MAY' : 'May',
    'JUN' : 'June',
    'JUL' : 'July',
    'AUG' : 'August',
    'SEP' : 'September',
    'OCT' : 'October',
    'NOV' : 'November',
    'DEC' : 'December'}

holidayList = [
    'New Years',
    'MLK Day',
    'Presidents Day',
    'Good Friday',
    'Memorial Day',
    'Juneteenth',
    'Independance Day',
    'Labor Day',
    'Thanksgiving',
    'Christmas']

#fixedDate follows a (day, month) format
fixedDate = {
    'New Years'        : (1, 1),
    'Juneteenth'       : (19, 6),
    'Independance Day' : (4, 7),
    'Christmas'        : (25, 12)}

#fixedDay follows a (str(month), day_of_week, occurance_of_day)) format
fixedDay = {
    'MLK Day'        : ('JAN', 'MON', 2),    #3rd Monday of JAN
    'Presidents Day' : ('FEB', 'MON', 2),    #3rd Monday of FEB
    'Memorial Day'   : (('MAY', 'MON', -1)), #Last Monday of MAY
    'Labor Day'      : ('SEP', 'MON', 0),    #First Monday of SEP
    'Thanksgiving'   : ('NOV', 'THU', 3)}    #4th Thursday of NOV

daysElapsed = [
    (0, 30), (31, 58), (59, 89), (90, 119),
    (120, 150), (151, 180), (181, 211), (212, 242),
    (243, 272), (273, 303), (304, 333), (334, 364)]

daysElapsedLeap = [
    (0, 30), (31, 59), (60, 90), (91, 120), 
    (121, 151), (152, 181), (182, 212), (213, 243), 
    (244, 273), (274, 304), (305, 334), (335, 365)]

#Note 9/11 was partial trading exception.
exceptions2001 = [(11,9,2001), (12,9,2001), (13,9,2001), (14,9,2001)] #9/11
exceptions2007 = [(1,2,2007)] #Gerald Fords Death
exceptions2012 = [(29, 10, 2012), (30, 10, 2012)] #Hurrican Sandy
exceptions2018 = [(5, 12, 2018)] #Bush Sr. Death

exceptionDates = {year: () for year in range(2000, 2050)}
exceptionDates[2001] = tuple(exceptions2001)
exceptionDates[2007] = tuple(exceptions2007)
exceptionDates[2012] = tuple(exceptions2012)
exceptionDates[2018] = tuple(exceptions2018)
    
@dataclass
class epoch:
    """Class for UNIX epoch."""
    date    : datetime64('1970-01-01')
    time    : '1970-01-01T00:00:00.000'
    day     : 'THU'
    weekEnum: 4
    
def leapYear(year):
    """Return if a given year is a leap year.
    
    Parameters
    ----------
    year: int: Non-abbreviated year (2004 not '04).
    
    Returns
    -------
    bool: Whether the input is a leap year.
    
    Notes
    -----
    ISO 8601 lists the year '0' as a leap year.
        
    Example(s)
    ----------
    >>> leapYear(2005)
    >>> False
    
    """
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

def dayMonthRange(year):
    return daysElapsedLeap if leapYear(year) else daysElapsed

def countLeap(year1, year2, order=False):
    """Count the number of leap days between the start of two years.
    
    Parameters
    ----------
    year1: int           : The non-abbreivated year (2004 not '04).
    year2: int           : The non-abbreivated year (2004 not '04).
    order: bool, optional: If order of inputs matters.
        
    Returns
    -------
    int: Signed number of leap days in range [1/1/year1, 1/1/year2].
        
    Notes
    -----
    If 'order' and 'year2' < 'year1', a negative answer may be returned.
    There are zero leap days in [1/1/X, 1/1/X] so countLeap(X, X) == 0.
        
    Example(s)
    ----------
    >>> countLeap(2000, 2023)
    >>> 6
    
    >>> countLeap(2023, 1999, order=True)
    >>> -6
    
    """
    leapDays, mn, mx = 0, min(year1, year2), max(year1, year2)
    start = mn + (4 - mn%4)
    while mn < mx:
        leapDays += leapYear(mn)
        mn += 4

    return -leapDays if (order and year2 < year1) else leapDays

def countLeapDays(date1, date2, order=False):
    """Count the number of leap days between the start of two dates.

    Parameters
    ----------
    date1: datetime64    : Date.
    date2: datetime64    : Date.
    order: bool, optional: If order of inputs matters.
        
    Returns
    -------
    int: Signed number of leap days in range [date1, date2).
        
    Notes
    ----- 
    If 'order' and 'year2' < 'year1', a negative answer may be returned.
    There are zero leap days in [1/1/X, 1/1/X] so countLeap(X, X) == 0.
        
    Example(s)
    ----------
    >>> countLeapDays((25,2,2000), (2,3,2024))
    >>> 7
    
    >>> countLeapDays((25,2,2050), (2,3,2024), True)
    >>> -6

    """
    mn, mx = np.min(date1, date2), np.max(date1, date2)
    yearCount = countLeap(mn.year, mx.year)
    
    overUnder = lambda date: (leapYear(date.year) and date.month >= 3)
    leapDays = yearCount - overUnder(mn) + overUnder(mx)

    return -leapDays if (order and date1 < date2) else leapDays

def newYearsDay(year):
    """Return the day of the week new years lands on.
    
    Using the fact the year 1899 started on a Sunday this function
    counts days elapsed since Jan. 1 1899 to find the day of Jan. 1
    on any given year.
    
    Parameters
    ----------
    year: int: The non-abbreivated year (2004 not '04).
    
    Returns
    -------
    str: 3 letter string identifying day of 1/1/year.
    
    Example(s)
    ----------
    >>> newYearsDay(1700)
    >>> FRI

    >>> newYearsDay(2024)
    >>> MON
    
    Notes
    -----
    Exploits the fact 365 % 7 == 1 to calculate days elapsed from 1/1/1899
    with "(leaps + deltaYr) % 7" instead of "(leaps + 365*deltaYr) % 7". 
    
    """                  
    deltaYr = year - 1899
    leapDays = countLeap(1899, year, order=True)
    return orderingOfWeek[(leapDays + deltaYr) % 7]

def weekOne(year):
    """Return the days of Jan 1 - Jan 7 for a given year.

    Parameters
    ----------
    year: int: The non-abbreivated year (2004 not '04).
    
    Returns
    -------
    dict: Dictionary of the first calander week in a given year.
        
    Example(s)
    ----------
    >>> weekOne(2000)
    >>> {1: 'SAT', 2: 'SUN', 3: 'MON', 4: 'TUE', 5: 'WED', 6: 'THU', 7: 'FRI'}
        
    """
    offset = orderingOfDays[newYearsDay(year)]
    rearrange = [(i - offset) % 7 for i in range(7)]
    week = {x+1: orderingOfWeek[i] for i, x in enumerate(rearrange)}
    return dict(sorted(week.items()))

def dt64_tuple(date):
    """Return (day, month, year)."""
    y, m, d = map(int, date[:10].split('-'))
    return (d, m, y)

def tuple_dt64(dateTup):
    """Return dt64. d, m, y = tuple"""
    makeISO = lambda n: f'0{str(n)}' if n < 10 else str(n)
    y, m, d = dateTup
    d, m = makeISO(d), makeISO(m)
    return datetime64(f'{y}-{m}-{d}')

def dateToDay(date):
    """Find the day of the week of a given date.

    Parameters
    ----------
    date : datetime64: Date.
    
    Returns
    -------
    dayOfWeek : str: The day of the week.

    Example(s)
    ----------
    >>> dateToDay((24, 12, 2023)
    >>> 'SUN'
        
    """
    weekEnum = date.astype('datetime64[D]').view('int64') - epoch.weekEnum) % 7
    return orderingOfWeek[weekEnum]

def getYear(date):
    """Return the day portion of the date.

    Parameters
    ----------
    date: datetime64: Date to floor.

    Returns
    -------
    int: Year portion of date.  

    """
    return int(str(date)[:5])

def getMonth(date):
    """Return the month portion of the date.

    Parameters
    ----------
    date: datetime64: Date.

    Returns
    -------
    int: month portion of date.  

    """
    return int(str(date)[5:7])

def getDay(date):
    """Return the day portion of the date.

    Parameters
    ----------
    date: datetime64: Date to floor.

    Returns
    -------
    int: Day portion of date.  

    """
    return int(str(date)[8:10])

def floorDate(date, month=True, year=False):
    """Return the first of the month or year for a given date.

    Parameters
    ----------
    date: datetime64: Date to floor.

    Returns
    -------
    first: datetime64: First of month of year.
    
    """
    isoString = f'{getYear(date)}'
    if month:
        numMonth = getMonth(date)
        isoMonth = f'0{numMonth}' if numMonth < 10 else f'{numMonth}'
        isoString += f'-{isoMonth}'
    return datetime64(isoString)

def ceilDate(date, month=True, year=False):
    """Return the first of the following month or year for a given date.

    Parameters
    ----------
    date: datetime64: Date to ceil.

    Returns
    -------
    first: datetime64: First of following month of year.
    
    """
    curMonth = getMonth(date)
    if curMonth == 12 and month=True:
        isoString = f'{getYear(date)+1}'
    elif month:
        month_ = curMonth + 1
        isoMonth = f'0{month_}' if month_ < 10 else f'{month_}'
        isoString = f'{getYear(date)+1}-{isoMonth}'
    else:
        isoString = f'{getYear(date)}' + 1
        
    return datetime64(isoString)

def daysInMonth(date):
    """Return number of days in the month of date."""
    month_, year_ = getMonth(date), getYear(date)
    start, end = dayMonthRange(year)[month_]
    return start - end
        

def monthCalander(date):
    """Return the day for all dates in a month.

    Parameters
    ----------
    date: datetime64: Date whose month's calander is returned.

    Returns
    -------
    cal: dict: A calander of dates: cal['MON'] = (date1, date2, ...).

    Example(s)
    ---------
    >>> monthCalander('jan', 2024)
    >>> {'SUN': (7, 14, 21, 28), 'MON': (1, 8, 15, 22, 29),
        'TUE': (2, 9, 16, 23, 30), 'WED': (3, 10, 17, 24, 31),
        'THU': (4, 11, 18, 25), 'FRI': (5, 12, 19, 26),
        'SAT': (6, 13, 20, 27)}
    
    """
    totDays, start = daysInMonth(date), floorDate(date)
    firstDay = orderingOfDays[dateToDay(start)]
    cal = {day: () for day in orderingOfDays}
    for i in range(7):
        val = firstDay + i
        cal[orderingOfWeek[val]] = (x+1 for x in range(val, daysInMonth, 7))
        
    return cal

def goodFriday(year):
    """Return the date of Good Friday for a year after 1582.

    Parameter
    ---------
    year : int : The non-abbreivated year (2004 not '04).

    Returns
    -------
    dateGoodFriday : datetime64: Date of Good Friday.

    Notes
    -----
    Derivative of Donald Knuth's Easter algorithm.

    """
    goldenNumber = (year % 19) + 1
    century = (year // 100) + 1
    leapShift, moonShift = (3*century)//4 - 12, (8*century + 5)//25 - 5
    sundayData = (5*year)//4 - leapShift - 10
    
    epact = (11*goldenNumber + 20 + moonShift - leapShift) % 30
    if (epact == 25 and goldenNumber > 11) or (epact == 24):
        epact += 1
        
    day = 44 - epact
    if day < 21:
        day += 30
        
    day += 7 - ((day + sundayData) % 7)
    month = 'APR' if day > 31 else 'MAR'
    if month == 'APR':
        day -= 31

    month_ = monthToInt[month]
    easter = (day, month_, year)
    if day > 2:
        day_ = day - 2
        goodFriday_ = (day_, month_, year)
    else: #months365 used below since month_ - 1 > 2
        days_ = months365[intToMonth[month_-1]] + day - 2
        goodFriday_ = (days_, month_-1, year)

    return goodFriday_

def tradingHolidays(date1, date2):
    """Return all trading holidays between in range: [date1, date2).

    Half holidays or full bond holidays are not counted, a full list
    of included holidays are:

        1.  New Year's Day:
                If it lands on Saturday then Friday before is off
                If on Sunday then following Monday is off
        2.  Martin Luther King Jr. Day
                Third Monday in Janaury
        3.  Presidents' Day
                Third Monday in Febuary
        4.  Good Friday
                See 'goodFriday' function.
        5.  Memorial Day
                Last Monday in May
        6.  Juneteenth
                June 19 (after 2020)
        7.  Independance Day
                July 4th
        8.  Labor Day
                First Monday of September
        9.  Thanksgiving Day
                Fourth Thursday of November
        10. Christmas Day
                December 25
    
    Parameters
    ----------
    date1: datetime64: Start date.
    date2: datetime64: End date.
    
    Returns
    -------
    holidays : dict: Dictionary of trading holidays that land on business days.

    Notes
    -----
    This function does not differentiate half trading days from full trading
    days.
    
    Example(s)
    ----------
    >>> tradingHolidays((5, 2, 2023), (7, 5, 2023))
    >>> {'New Years': [], 'MLK Day': [], 'Presidents Day': [(20, 2, 2023)],
        'Good Friday': [(7, 4, 2023)], 'Memorial Day': [], 'Juneteenth': [],
         'Independance Day': [], 'Labor Day': [], 'Thanksgiving': [],
         'Christmas': []}
    
    """
    holidays = {hol:[] for hol in holidayList}
    sD, sM, sY = dt64_tuple(date1)
    eD, eM, eY = dt64_tuple(date2)
    NYDexception = lambda dt: dt[5:10] == '12-31'
    
    for year in range(sY, eY):
        
        #Good Friday
        holidays['Good Friday'] += [goodFriday(year)]

        #Fixed date holidays
        for hol in fixedDate:
            if hol == 'Juneteenth' and year < 2022:
                continue
            
            holDate = tuple_dt64(fixedDate[hol] + (year,))
            holDay = dateToDay(holDate)
            
            if holDay in {'SAT', 'SUN'}:
                adjust = -1 if (holDay == 'SAT') else 1
                holDate = holDate + adjust
            if NYDexception(holDate): #Rule 7.2 of NYSE
                continue
            
            holidays[hol].append(holDate)

        #Fixed day holidays
        for hol in fixedDay:
            month, day, occ = fixedDay[hol]
            day_ = (monthCalander(month, year)[day][occ]
            month_ = monthToInt[month]
            holDate = tuple_dt64((day_, month_, year))
            holidays[hol].append(holDate)

    #Remove holidays before date1 or after date2
    inRange = lambda arr: [x for x in arr if date1 <= x < date2]
    holidays = [hol: inRange(holidays[hol]) for hol in holiday]

    return holidays

def tradingDays(date1, date2):
    """Return the expected number of trading from date1 to the start of date2.

    It is assumed 'date1' <= 'date2'.
    Expected here refers to lack of exceptions is accounted for in final
    enumeration (see generateTradingDay.py)

    Parameters
    ----------
    date1: datetime64: Start date.
    dare2: datetime64: End date.
    
    Returns
    -------
    int : Number of trading days in a given range. Assumes no excpetions.

    Notes
    -----
    This function counts trading days including date1 upto but not including
    date2. On a regular trading week if date1 is Monday and date2 is Friday
    there are 4 trading days from date1 to date2. But if date2 is Saturday,
    Sunday, or Monday the answer is 5 trading days, since Friday has
    fully elapsed.

    Example(s)
    ----------
    >>> tradingDays((8,7,2010), (28,2,2011))
    >>> 159

    """
    holidays = tradingHolidays(date1, date2)
    weekdayHolidays = sum([len(holidays[hol]) for hol in holidays])
    weekdays = np.busday_count(date1, date2)
    return weekdays - weekdayHolidays

def dateToYears(date1, date2):
    """Return the time from date1 to date2 as a fraction of a trading year.
    
    Trading years refers to number of trading days in the given timerange.
    Note time is counted from start of date1 to start of date2, the time
    from date2 itself is not included.
    
    Parameters
    ----------
    date1: datetime64: Start date.
    dare2: datetime64: End date.
        
    Returns
    -------
    T : float: Time in (trading) years between the two dates.

    Example(s)
    ----------
    >>> dateToYears((1,1,2024),(1,1,2025))
    >>> 1.0
    
    """
    yr1, yr2 = getYear(date1), getYear(date2)
    floor1, floor2 = floorDate(date1, year=True), floorDate(date2, year=True)
    ceil1, ceil2 = ceilDate(date1, year=True), ceilDate(date2, year=True)
    
    yrJump = yr2 - yr1 - 1
    ratio1 = tradingDays(date1, ceil1) / tradingDays(floor1, ceil1)
    ratio2 = tradingDays(new2, ceil2) / tradingDays(new2, ceil2)

    T = yrJump + ratio1 + ratio2
    
    return T

def addYears(T, date):
    """Add trading years to the first trading day on or after a given date.
    
    A trading 'day' covers a range of a trading year. Namely,
    from the start of the trading day to the start of the next trading day.
    The trading range is the course of the trading day, the calander range
    can be multiple days.
    
    Parameters
    ----------
    T : float: Time in years.
    date : datetime64 : Date.
        
    Returns
    -------
    endD : datetime64: Date of trading day a prescribed distance from the start.

    Example(s)
    ----------
    >>> addYears(2/252, (1,1,2024))
    >>> (4, 1, 2024)
    
    """
    endD = int(365*T) + date
    while 1:
        if T < dateToYears(date, endD):
            endD -= 1
        elif T >= dateToYears(date, endD + 1):
            endD += 1
        else: #T is bounded by dateToYears range of endD
            break
    
    #Determine if endD is a trading day, adjust if needed
    fixed = endD - 7
    endMinus = endD - 1
    while tradingDays(fixed, endD) == endMinus:
        endD = endMinus
        endMinus -= 1
    
    return endD

def trDays(startD, T):
    """Return total trading days from startD to T years from startD.
    
    Parameters
    ----------
    startD : datetime64: Start date.
    T : float: Time in years.

    Returns
    -------
    trDays() : int:  Time in years of one day.

    Example(s)
    ----------
    >>> trDays('Jan 1 2024', 1.82)
    >>> 457
    
    """
    endDate = addYears(T, startD)
    return tradingDays(startD, endDate)

def oneDay(startD, T):
    """Return proportion of total trading time a range of dates is.
    
    Parameters
    ----------
    startD : datetime64: Start date.
    T : float: Time in years.
        
    Returns
    -------
    oneDay() : float: Time in years of one day.

    Example(s)
    ----------
    >>> oneDay('Jan 1 2024', 2/252)
    >>> 0.003968253968253968
    
    """
    return T / trDays(startD, T)

def timeList(date_arr, start):
    #Return [dateToYears(start, x) for x in date_arr]
    """start and date_arr entries are datetime64"""
    return [dateToYears(start, x) for x in date_arr]

def enumWeekends(year):
    """Return weekends : set, s.t. i in weekends if i is enum(weekend)"""
    daysInYear = 366 if leapYear(year) else 365
    for enum, day in weekOne(year).items():
        if day == 'SAT':
            firstSat = enum
        if day == 'SUN':
            firstSun = enum
            
    firstOcc = min(firstSat, firstSun)
    pos = 1 if firstOcc == firstSat else -1
    upperRange = (daysInYear - firstOcc) // 7 + 1
    
    wknd1 = {7*k + firstOcc for k in range(upperRange)}
    wknd2 = {x+pos for x in wknd1 if (x+pos <= daysInYear and x+pos > 0)}
    return wknd1 | wknd2

def enumDate(date):
    """Return i s.t. d/m/y = 1/1/y + i days"""
    return date - floorDate(date, year=True)

def enumDateTuple_(date_arr):
    return tuple(enumDate(x) for x in date_arr)
