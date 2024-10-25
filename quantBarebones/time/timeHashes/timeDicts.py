"""Time Dicts"""

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

#enumYears[year] = calander days from [1/12000 to 1/1/year).
enumYears = {
    2000: 0,     2001: 366,   2002: 731,   2003: 1096,  2004: 1461,
    2005: 1827,  2006: 2192,  2007: 2557,  2008: 2922,  2009: 3288,
    2010: 3653,  2011: 4018,  2012: 4383,  2013: 4749,  2014: 5114,
    2015: 5479,  2016: 5844,  2017: 6210,  2018: 6575,  2019: 6940,
    2020: 7305,  2021: 7671,  2022: 8036,  2023: 8401,  2024: 8766,
    2025: 9132,  2026: 9497,  2027: 9862,  2028: 10227, 2029: 10593,
    2030: 10958, 2031: 11323, 2032: 11688, 2033: 12054, 2034: 12419,
    2035: 12784, 2036: 13149, 2037: 13515, 2038: 13880, 2039: 14245,
    2040: 14610, 2041: 14976, 2042: 15341, 2043: 15706, 2044: 16071,
    2045: 16437, 2046: 16802, 2047: 17167, 2048: 17532, 2049: 17898}

#trDaysInYear[year] = # trading days in [1/1/year, 12/31/year].
trDaysInYear = {
    2000: 252, 2001: 247, 2002: 251, 2003: 251, 2004: 252,
    2005: 252, 2006: 251, 2007: 251, 2008: 252, 2009: 251,
    2010: 251, 2011: 252, 2012: 249, 2013: 251, 2014: 251,
    2015: 251, 2016: 252, 2017: 251, 2018: 251, 2019: 251,
    2020: 252, 2021: 251, 2022: 251, 2023: 250, 2024: 251,
    2025: 250, 2026: 250, 2027: 250, 2028: 251, 2029: 250,
    2030: 250, 2031: 250, 2032: 251, 2033: 251, 2034: 250,
    2035: 250, 2036: 251, 2037: 250, 2038: 250, 2039: 251,
    2040: 250, 2041: 250, 2042: 250, 2043: 250, 2044: 251,
    2045: 250, 2046: 250, 2047: 250, 2048: 251, 2049: 250}
    
@dataclass
class epoch:
    """Class for UNIX epoch."""
    date    : datetime64('1970-01-01')
    time    : '1970-01-01T00:00:00.000'
    day     : 'THU'
    weekEnum: 4
