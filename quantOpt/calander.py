"""Collection of time relation functions."""

monthToInt = {'JAN' : 1,
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
    
intToMonth = {1 : 'JAN',
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

months365 = {'JAN' : 31, 
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

months366 = {'JAN' : 31, 
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

orderingOfWeek = {0 : 'SUN',
                  1 : 'MON', 
                  2 : 'TUE', 
                  3 : 'WED', 
                  4 : 'THU', 
                  5 : 'FRI', 
                  6 : 'SAT'}
                  
orderingOfDays = {'SUN' : 0,
                  'MON' : 1, 
                  'TUE' : 2, 
                  'WED' : 3, 
                  'THU' : 4, 
                  'FRI' : 5, 
                  'SAT' : 6}

abbreviationToFull = {'SUN' : 'Sunday',
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

daysElapsed = [(0, 30), (31, 58), (59, 89), (90, 119), 
               (120, 150), (151, 180), (181, 211), (212, 242), 
               (243, 272), (273, 303), (304, 333), (334, 364)]

daysElapsedLeap = [(0, 30), (31, 59), (60, 90), (91, 120), 
                   (121, 151), (152, 181), (182, 212), (213, 243), 
                   (244, 273), (274, 304), (305, 334), (335, 365)]
    
def leapYear(year):
    """Return if a given year is a leap year.
    
    Parameters
    ----------
    year : int
        The non-abbreviated year (2004 not '04).
    
    Returns
    -------
    leapYear(year) : bool
        Whether the input is a leap year.
    
    Notes
    -----
    ISO 8601 (the international standard for communication of date and time)
    lists the year '0' as a leap year.
        
    Example(s)
    ----------
    >>> leapYear(2005)
    >>> False
    
    """
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

def countLeap(year1, year2, order=False):
    """Count the number of leap days between the start of two years.
    
    If 'order==True' and 'year2' < 'year1', the number of leap days between 
    Jan 1 'year1' and Jan 1 'year2' are counted as negative, since the function
    is coutning 'backwards' with respect to time. In this case you can note:
        countLeap(year1, year2, order=True) == -countLeap(year2, year1).
    
    Parameters
    ----------
    year1, year2 : int
        The non-abbreivated year (2004 not '04).
    order : bool, optional
        Whether we take the order of years into account.
        
    Returns
    -------
    leapDays : int
        Number of leap days between start of year1 and the start of year2.
        
    Notes
    ----- 
    This function counts the number of leap days between the start or two
    years, for this reason if 'year1' == 'year2' the function returns 0, as there
    are zero leap days between Jan 1 'Year1' and Jan 1 'Year1'.
        
    Example(s)
    ----------
    >>> countLeap(2000, 2023)
    >>> 6
    
    >>> countLeap(2023, 1999, order=True)
    >>> -6
    
    """
    leapDays = 0
    mn, mx = min(year1, year2), max(year1, year2)
    for yr in range(mn, mx):
        if leapYear(yr): leapDays += 1 

    if order and year2 < year1:
        leapDays *= -1

    return leapDays

def countLeapDays(date1, date2, order=False):
    """Count the number of leap days between two dates.

    This function counts the number of leap days between the start
    of 'date1' and the start of 'date2'.

    When 'order==True' and 'date1' comes after 'date2', the number of
    leap days between the start of 'date1' and start of 'date2' are
    counted as negative, since the function is counting 'backwards' with
    respect to time. In this case you can note:
        countLeapDays(date1, date2, order=True) == -countLeapDays(date2, date1).
        
    Parameters
    ----------
    date1, date2 : tuple
        Date given as a tuple of the form: (day: int, month: int, year: int)
    order : bool, optional
        Whether we take the order of dates into account.
        
    Returns
    -------
    leapDays : int
        Number of leap days between start of date1 and the start of date2.
        
    Notes
    ----- 
    This function counts the number of leap days between the start or two
    dates, for this reason if 'date1' == 'date2' the function returns 0, as there
    are zero leap days between the start of the same day.
        
    Example(s)
    ----------
    >>> countLeapDays((25,2,2000), (2,3,2024))
    >>> 7
    
    >>> countLeapDays((25,2,2050), (2,3,2024), True)
    >>> -6

    See Also
    --------
    This function is based on the very similar 'countLeap' function.
    
    """
    if date2[::-1] < date1[::-1]:
        minDate = date2
        maxDate = date1
    else:
        minDate = date1
        maxDate = date2
    
    year1, year2 = minDate[2], maxDate[2]
    month1, month2 = minDate[1], maxDate[1]

    #Count leap days from year1 to year2
    yearCount = countLeap(year1, year2)
    
    #Count days from year1 to date1 and from year2 to date2
    overCounted = 1 if (leapYear(year1) and month1 >= 3) else 0
    notCounted = 1 if (leapYear(year2) and month2 >= 3) else 0

    leapDays = yearCount - overCounted + notCounted

    if order and minDate == date2:
        leapDays *= -1

    return leapDays

def newYearsDay(year):
    """Return the day of the week new years lands on.
    
    Using the fact the year 1899 started on a Sunday this function
    counts days elapsed since Jan. 1 1899 to find the day of Jan. 1
    on any given year.
    
    Parameters
    ----------
    year : int
        The non-abbreivated year (2004 not '04).
    
    Returns
    -------
    newYears(year) : str
        3 letter string for the day of January first in a given year.
    
    Example(s)
    ----------
    >>> newYearsDay(1700)
    >>> FRI

    >>> newYearsDay(2024)
    >>> MON
    
    Notes
    -----
    The final result "days = (leaps + deltaYr) % 7" is the number of
    days that have elapsed since 1900 taken modolu 7. An accurate 
    count of days elapsed would be: leaps + 365*deltaYr, 
    but since we will take this result modolu 7 and 365 % 7 == 1, 
    it is more economical to replace 365 with 1 in the calculation.
    
    """                  
    deltaYr = year - 1899
    leapDays = countLeap(1899, year, order=True)
    days = (leapDays + deltaYr) % 7

    return orderingOfWeek[days]

def weekOne(year):
    """Return the days of Jan 1 - Jan 7 for a given year.

    Parameters
    ----------
    year : int
        The non-abbreivated year (2004 not '04).
    
    Returns
    -------
    week : dict
        Dictionary of the first calander week in a given year.
        
    Example(s)
    ----------
    >>> weekOne(2000)
    >>> {1: 'SAT', 2: 'SUN', 3: 'MON', 4: 'TUE', 5: 'WED', 6: 'THU', 7: 'FRI'}
        
    """
    offset = orderingOfDays[newYearsDay(year)]
    newArrangement = [(i - offset) % 7 for i in range(7)]
    week = {}
    for i, x in enumerate(newArrangement):
        week[x + 1] = orderingOfWeek[i]

    week = dict(sorted(week.items()))
    
    return week

def elapsedDays(dayCount, date):
    """Return the date a given number of days in the future.
    
    This function converts the number of days that have elapsed after a
    fixed date to an exact date in month-day-year form. For instance,
    366 days after Jan 1 1997 is Jan 2 1998.

    The count is done from start of day to start of day.
    
    Parameters
    ----------
    dayCount : int
        The number of days elapsed from the new years. Can be negative.
    date : tuple, int
        Date the count starts on. Date can be a tuple of form
        (day, month, year) or the non-abbreivated year (2004 not '04)
        which represents Jan 1 of that year.
    
    Returns
    -------
    date : tuple
        Date in (day, month, year) form.
        
    Example(s)
    ----------
    >>> elapsedDays(31, 2024)
    >>> (1, 2, 2024)

    >>> elapsedDays(700, (5, 5, 2022))
    >>> (4, 4, 2024)

    >>> elapsedDays(-3, 2024)
    >>> (29, 12, 2023)
    
    """
    if type(date) == tuple:
        day, month, year = date
        if leapYear(year):
            dayCount += daysElapsedLeap[month-1][0] + day - 1
        else:
            dayCount += (daysElapsed[month-1][0] + day) - 1
                    
    else: year = date

    #Convert negative case to a postive case problem
    while dayCount < 0:
        dayCount += (365 + leapYear(year-1))
        year -= 1
    
    #Deal with postive case
    while dayCount >= (365 + leapYear(year)):
        dayCount = dayCount - (365 + leapYear(year))
        year += 1
        
    daySummed = daysElapsedLeap if leapYear(year) else daysElapsed

    date = ()
    for month_, daysInMonth in enumerate(daySummed, 1):
        monthStart, monthEnd = daysInMonth
        if dayCount <= monthEnd:
            day_ = dayCount - monthStart
            date = (day_+1, month_, year)
            break
    
    return date

def parseDate(dateInput):
    """Given a user-inputed string, return the date as a tuple, verify validity.
    
    Acceptable inputs - strings: 'DpAqY', 'BpDqY', 'fullYpBqD'
        - 'D' is of the form str(num) for num an integer between 1 and 31.
        - 'p' and 'q' are from the set {' ', ',', '/', '-'}.
        - 'A' is a string representing a month, satisfying the following rules:
            * No numerics in 'A'
            * 'A' is case blind (RS == rS == Rs == RS)
            * 'A' requires only the first three letters of a month 
               but can have more, or all (Dec = Dece = decem = december)
            * 'A' can end in a period ('Dec.' is accepted)
        - 'B' is a string representing a month, it includes all forms of 'A'
          as well as strings of the form str(num) where num is an integer
          between 1 and 12.
        - 'Y' is of the form str(num) where num is a two or four digit integer
            * All 2 digit inputs are interpuretted to be years in the 
              21st century.
        - 'fullY' of the form str(num), must be length 4, leading zeros are ok.
              
    Short hand inputs - ints: yearInt
        - yearInt: returns start of the year (yearInt here is an integer)
            - yearInt should not be abbreivated, if yearInt = 24, function
            will read it as the 24th year NOT 2024.

    Dates of the form (d:int, m:int, y:int) get verified and returned.
        
    Parameters
    ----------
    dateInput : str, int, tuple
        Date inputed in the forms described above.
    
    Returns
    -------
    date : tuple
        Parsed date in given by a tuple of the form (day, month, year).
        
    Example(s)
    ----------
    >>> parseDate('5 Jan 25')
    >>> (5, 1, 2025)
    
    >>> parseDate('Dec. 21 2025')
    >>> (21, 12, 2025)
    
    >>> parseDate('12/30 2025')
    >>> (30, 12, 2025)
    
    """
    #Early returns for short hand input of full year
    if type(dateInput) == int:
        year = dateInput if dateInput > 1999 else 2000+dateInput
        return (1, 1, year)

    if type(dateInput) == tuple:
        day, month, year = dateInput
        dateInput = f'{month} {day} {year}'

    if type(dateInput) != str:
        dateInput = str(dateInput)

    nums, mnthStarts = '0123456789', 'jfmasond' + 'JFMASOND'
    
    #If of form 'fullYpBqD' convert to 'BqDpfullY'
    fullYCand = dateInput[:4]
    swap = all([char in nums for char in fullYCand])
    if swap:
        p = dateInput[4]
        dateInput = dateInput[5:] + p + fullYCand

    strDate = dateInput
    #Delete all spaces
    strDate = " ".join(strDate.split())

    #Extract the year
    year = int('20' + strDate[-2:])
    if strDate[-3] in nums:
        strDate = strDate[:-5]
    else: strDate = strDate[:-3]

    #Extract the day and month pair
    for i, x in enumerate(strDate):
        if x in {' ', ',', '/', '-'}:
            a = strDate[:i]
            b = strDate[i+1:]
            break
    
    #'b' is the month and 'a' is the day
    if b[0] in mnthStarts:
        month = monthToInt[b[:3].upper()]
        day = int(a)
    
    #'a' is the month and 'b' is the day
    else:
        if a[0] in mnthStarts:
            month = monthToInt[a[:3].upper()]
        else:
            month = int(a)
        day = int(b)
        
    date = (day, month, year)
    
    #Verify date is valid
    monthDays = months366 if leapYear(year) else months365
    daysInMonth = monthDays[intToMonth[month]]
    
    #Check to see if valid day, month, year combination.
    if (0 > min(day, month)) or (month > 12) or (day > daysInMonth):
        raise Exception('Invalid Date.')
      
    return date

def dateToDay(date):
    """Find the day of the week of a given date.

    Parameters
    ----------
    date : tuple
        Date given as a tuple of the form: (day: int, month: int, year: int).
    
    Returns
    -------
    dayOfWeek : str
        The day of the week.

    Example(s)
    ----------
    >>> dateToDay((24, 12, 2023)
    >>> 'SUN'
        
    """
    day, month, year = date
    if leapYear(year): enumDate= daysElapsedLeap[month-1][0] + day - 1
    else: enumDate= daysElapsed[month-1][0] + day - 1

    startDay = orderingOfDays[newYearsDay(year)]
    dayOfWeek = orderingOfWeek[(startDay + enumDate) %7]

    return dayOfWeek

def countWeekDays(date1, date2):
    """Return the number of weekdays (Mon-Fri) between two dates.

    Parameters
    ----------
    date1, date2 : tuple
        Date given as a tuple of the form: (day: int, month: int, year: int).
    
    Returns
    -------
    countWeekDays() : int
        Number of week days in a given year.

    """
    day1, month1, year1 = date1
    day2, month2, year2 = date2

    #Count days from year1 to year2
    yearCount = 365 * (year2 - year1) + countLeap(year1, year2)

    #Count days from year1 to date1 and from year2 to date2
    if leapYear(year1): overCounted = daysElapsedLeap[month1-1][0] + day1 - 1
    else: overCounted = daysElapsed[month1-1][0] + day1 - 1
        
    if leapYear(year2): notCounted = daysElapsedLeap[month2-1][0] + day2 - 1
    else: notCounted = daysElapsed[month2-1][0] + day2 - 1

    days = yearCount - overCounted + notCounted

    #Find how many days until the first Saturday and Sunday on or after date1
    dayDate1 = dateToDay(date1)
    firstSat = orderingOfDays['SAT'] - orderingOfDays[dayDate1] + 1
    firstSun = 1 if dayDate1 == 'SUN' else firstSat + 1

    sats = (days - firstSat)//7 + 1
    suns = (days - firstSun)//7 + 1

    return days - (sats + suns)

def monthCalander(month, year):
    """Return the day for all dates in a month.

    Parameters
    ----------
    month : str
        Case blind first 3 letters of month whose calander will be returned.
    year : int
        The non-abbreivated year (2004 not '04).

    Returns
    -------
    cal : dict
        A calander of dates with e.g. cal['MON'] = (date1, date2, ...).

    Example(s)
    ---------
    >>> monthCalander('jan', 2024)
    >>> {'SUN': (7, 14, 21, 28), 'MON': (1, 8, 15, 22, 29),
        'TUE': (2, 9, 16, 23, 30), 'WED': (3, 10, 17, 24, 31),
        'THU': (4, 11, 18, 25), 'FRI': (5, 12, 19, 26),
        'SAT': (6, 13, 20, 27)}
    
    """
    month = month.upper()
    if leapYear(year):
        monthRange = daysElapsedLeap[monthToInt[month]-1]
    else:
        monthRange = daysElapsed[monthToInt[month]-1]

    start, end = monthRange
    cal = {day: () for day in orderingOfDays}
    for x in range(start, end+1):
        date = elapsedDays(x, (1, 1, year))
        day = dateToDay(date)
        cal[day] += (date[0],)
        
    return cal

def goodFriday(year):
    """Return the date of Good Friday for a year after 1582.

    Parameter
    ---------
    year : int
        The non-abbreivated year (2004 not '04).

    Returns
    -------
    dateGoodFriday : tuple    
        Date given as a tuple of the form: (day: int, month: int, year: int).

    Notes
    -----
    This is essentially Donald Knuth's algorithm for calculating
    the day of Easter.

    """
    goldenNumber = (year % 19) + 1
    century = (year//100) + 1
    leapShift, moonShift = (3*century)//4 - 12, (8*century + 5)//25 - 5
    sundayData = (5*year)//4 - leapShift - 10
    epact = (11*goldenNumber + 20 + moonShift - leapShift) % 30
    if (epact == 25 and goldenNumber > 11) or (epact == 24):
        epact += 1
    day = 44 - epact
    if day < 21: day += 30
    day += 7 - ((day + sundayData) % 7)
    month = 'APR' if day > 31 else 'MAR'

    if month == 'APR': day -= 31
    easter = (day, monthToInt[month], year)
    dateGoodFriday = elapsedDays(-2, easter)

    return dateGoodFriday

def tradingHolidays(date1, date2):
    """Return all trading holidays between two dates.

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
    date1, date2 : tuple
        Date given as a tuple of the form: (day: int, month: int, year: int).
    
    Returns
    -------
    holidays : dict
        Dictionary of trading holidays that land on business days.

    Notes
    -----
    This function does not differentiate half trading days from full trading
    full trading days.
    
    Markets are typically closed if a US president (past or present) passes
    away. There should be no way to predict the day this occurs to account
    for it.

    Example(s)
    ----------
    >>> tradingHolidays((5, 2, 2023), (7, 5, 2023))
    >>> {'New Years': [], 'MLK Day': [], 'Presidents Day': [(20, 2, 2023)],
        'Good Friday': [(7, 4, 2023)], 'Memorial Day': [], 'Juneteenth': [],
         'Independance Day': [], 'Labor Day': [], 'Thanksgiving': [],
         'Christmas': []}
    
    """
    fixedDate = {'New Years' : (1, 1),
                 'Juneteenth' : (19, 6),
                 'Independance Day' : (4, 7),
                 'Christmas' : (25, 12)}
    
    fixedDay = {'MLK Day' : ('JAN', 'MON', 2),
                'Presidents Day' : ('FEB', 'MON', 2),
                'Memorial Day' : (('MAY', 'MON', -1)),
                'Labor Day' : ('SEP', 'MON', 0),
                'Thanksgiving' : ('NOV', 'THU', 3)}

    holidayList = ['New Years', 'MLK Day', 'Presidents Day', 'Good Friday',
                   'Memorial Day', 'Juneteenth', 'Independance Day',
                   'Labor Day', 'Thanksgiving', 'Christmas']

    holidays = {}
    for hol in holidayList: holidays[hol] = []
    
    startYear, endYear = date1[2], date2[2]+1
    for year in range(startYear, endYear):
        
        #Good Friday
        holidays['Good Friday'] += [goodFriday(year)]

        #Fixed Date holidays
        for hol in fixedDate:
            if hol == 'Juneteenth' and year < 2022: continue
            holDate = fixedDate[hol] + (year,)
            holDay = dateToDay(holDate)
            if holDay in {'SAT', 'SUN'}:
                delDay = -1 if (holDay == 'SAT') else 1
                holDate = elapsedDays(delDay, holDate)
            if holDate == (31, 12, year-1): #Rule 7.2 of NYSE
                continue
            holidays[hol] += [holDate]

        #Fixed day holidays
        for hol in fixedDay:
            month, day, occ = fixedDay[hol]
            holidays[hol] += [(monthCalander(month, year)[day][occ],
                               monthToInt[month], year)]

    #Remove holidays before date1 or after date2
    for hol in holidays:
        tmp = [x for x in holidays[hol]]
        for date in holidays[hol]:
            if date[::-1] < date1[::-1]:
                tmp.remove(date)
            if date[::-1] >= date2[::-1]:
                tmp.remove(date)
        holidays[hol] = tmp

    return holidays

def tradingDays(date1, date2):
    """Return the number of trading from date1 to the start of date2.

    It is assumed 'date1' <= 'date2'.

    Parameters
    ----------
    date1, date2 : tuple
        Date given as a tuple of the form: (day: int, month: int, year: int)
    
    Returns
    -------
    businessDaysYear() : int
        Number of business days in a given year.

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
    weekdays = countWeekDays(date1, date2)
    return weekdays - weekdayHolidays

def dateToYears(date1, date2):
    """Return the time from date1 to date2 as a fraction of a trading year.
    
    Trading years refers to number of trading days in the given timerange.
    Note time is counted from start of date1 to start of date2, the time
    from date2 itself is not included.
    
    Parameters
    ----------
    date1, date2 : tuple
        Date given as a tuple of the form: (day: int, month: int, year: int)
        
    Returns
    -------
    T : float
        Time in (trading) years between the two dates.

    Example(s)
    ----------
    >>> dateToYears((1,1,2024),(1,1,2025))
    >>> 1.0
    
    """
    yr1, yr2 = date1[2], date2[2]
    new1, new2 = (1, 1, yr1), (1, 1, yr2)
    
    yrJump = yr2 - yr1 - 1
    ratio1 = tradingDays(date1, (1,1,yr1+1)) / tradingDays(new1, (1,1,yr1+1))
    ratio2 = tradingDays(new2, date2) / tradingDays(new2, (1,1,yr2+1))

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
    T : float
        Time in years.
    date : tuple
        Date given as a tuple of the form: (day: int, month: int, year: int)
        
    Returns
    -------
    endD : tuple
        Date of trading day a prescribed distance from the start.

    Example(s)
    ----------
    >>> addYears(2/252, (1,1,2024))
    >>> (4, 1, 2024)
    
    """
    endD = elapsedDays(int(365*T), date)
    while 1:
        if T < dateToYears(date, endD):
            endD = elapsedDays(-1, endD)
        elif T >= dateToYears(date, elapsedDays(1, endD)):
            endD = elapsedDays(1, endD)
        else: #T is bounded by dateToYears range of endD
            break
    
    #Determine if endD is a trading day, adjust if needed
    fixed = elapsedDays(-7, endD)
    endMinus = elapsedDays(-1, endD)
    while tradingDays(fixed, endD) == endMinus:
        endD = endMinus
        endMinus = elapsedDays(-1, endD)
    
    return endD

def trDays(startD, T):
    """Return total trading days from startD to T years from startD.
    
    Parameters
    ----------
    T : float
        Time in years.
    startD : str, tuple [See parseDate for all input types]
        Start date.
        
    Returns
    -------
    trDays() : int
        Time in years of one day.

    Example(s)
    ----------
    >>> trDays('Jan 1 2024', 1.82)
    >>> 457
    
    """
    startD = parseDate(startD)
    endDate = addYears(T, startD)
    return tradingDays(startD, endDate)

def oneDay(startD, T):
    """Return proportion of total trading time a range of dates is.
    
    Parameters
    ----------
    T : float
        Time in years.
    startD : str, tuple [See parseDate for all input types]
        Start date.
        
    Returns
    -------
    oneDay() : float
        Time in years of one day.

    Example(s)
    ----------
    >>> oneDay('Jan 1 2024', 2/252)
    >>> 0.003968253968253968
    
    """
    return T / trDays(startD, T)
