"""Unittests for calander.py"""

import unittest
import calander

class leapYearTest(unittest.TestCase):
    """Test of 'leapYear' function."""

    def test_knownLeapYears(self):
        """Test 'leapYear' for non-century leap years between 0 and 2500."""
        
        for year in range(0, 2501):
            if (year % 4 == 0) and (year % 100 != 0):
                failMessage = f'{year} should not be a leap year.'
                self.assertTrue(calander.leapYear(year), failMessage)
                
    def test_notLeapYears(self):
        """Test 'leapYear' for non-century non-leap years between 0 and 2500."""
        
        for year in range(0, 2501):
            if (year % 4 != 0) and (year % 100 != 0):
                failMessage = f'{year} should be a leap year.'
                self.assertFalse(calander.leapYear(year), failMessage)
        
    def test_centuries(self):
        """Test 'leapYear' for turn of century years between 0 and 2500."""
        
        for century in range(26):
            year = 100 * century
            if year % 400 == 0:
                failMessage = f'{year} should not be a leap year.'
                self.assertTrue(calander.leapYear(year), failMessage)
                
            else:
                failMessage = f'{year} should be a leap year.'
                self.assertFalse(calander.leapYear(year), failMessage)

class countLeapTest(unittest.TestCase):
    """Test of 'countLeap' function."""

    def altCountLeap(self, startYear, endYear):
        """Return the number of leap days between start of two years.

        An alternative method of counting leap days. Note this method
        assumes 'startYear' < 'endYear'.

        Parameters
        ----------
        startYear, endYear : int
            The non-abbreivated year (2004 not '04).
        
        Returns
        -------
        leapDays : int
            Number of leap days between start of 'startYear' and
            start of 'endYear'.

        Example(s)
        ----------
        >>> altCountLeap(2000, 2023)
        >>> 6
    
        """
        count = 0
        for yr in range(startYear, endYear):
            if (yr % 4 == 0) and (yr % 100 != 0):
                count += 1
            elif (yr % 400 == 0):
                count += 1
                
        return count
            
    def test_SameYear(self):
        """Test 'countLeap' when year paramaters are equal."""
        
        for yr in range(2501):
            self.assertEqual(calander.countLeap(yr, yr, order=False), 0)
            self.assertEqual(calander.countLeap(yr, yr, order=True), 0)
        
    def test_orderEqualsFalse(self):
        """Test 'countLeap' when 'order == False'.
        
        When 'order == False', the other two parameters are interchangable.
        This allows, without loss of generality, to assume the first input
        is less than or equal to the second input. The equality cases was
        verified above, so it is assumed the first input is strictly less than
        the second input.

        Also note, while the case of zero leap days is tested for, the case
        of non-zero leap days is not considered an edge case so it is not
        tested directly but is tested implicitly by the majority of tests
        ran in the other scenerios.
        
        """
        #Using 'calander.leapYear' function build a list with indices
        #representing years and entries answering if that year is a leap year.
        isLeap = [calander.leapYear(idx) for idx in range(1950, 2201)]
        N = len(isLeap)
        
        #Only the first paramater is a leap year
        failMessage = 'Only the first parameter is leap year.'
        for i in range(N-1):
            if not isLeap[i]: continue
            year1 = 1950 + i
            for j in range(i+1, N):
                if not isLeap[j]:
                    year2 = 1950 + j
                    failData = f' Years: {year1} and {year2}.'
                    self.assertEqual(calander.countLeap(year1, year2),
                                     self.altCountLeap(year1, year2),
                                     failMessage + failData)
                        
        #Only second parameter is leap year
        failMessage = 'Only the second parameter is leap year.'
        for i in range(N-1):
            if isLeap[i]: continue
            year1 = 1950 + i
            for j in range(i+1, N):
                if isLeap[j]:
                    year2 = 1950 + j
                    failData = f' Years: {year1} and {year2}.'
                    self.assertEqual(calander.countLeap(year1, year2),
                                     self.altCountLeap(year1, year2),
                                     failMessage + failData)
                        
        #Both paramaters are leap years
        failMessage = 'Both parameters are leap years.'
        for i in range(0, N-2, 4):
            if not isLeap[i]: continue
            leap1 = 1952 + i #Start at the first classified leap year
            for j in range(i+4, N-1, 4):
                if isLeap[j]:
                    leap2 = 1952 + j
                    failData = f' Years: {year1} and {year2}.'
                    self.assertEqual(calander.countLeap(leap1, leap2),
                                     self.altCountLeap(leap1, leap2),
                                     failMessage + failData)
                
        #No paramaters are leap years
        failMessage = 'No paramaters are leap years.'
        for i in range(i, N-1):
            if isLeap[i]: continue
            year1 = 1950 + i
            for j in range(i+1, N):
                if not isLeap[j]:
                    year2 = 1950 + j
                    failData = f' Years: {year1} and {year2}.'
                    self.assertEqual(calander.countLeap(year1, year2),
                                     self.altCountLeap(year1, year2),
                                     failMessage + failData)
                        
        #Zero leap days between the start of the two years
        for x in range(N):
            if not isLeap[x]: continue
            leap = 1950 + x
            for i in range(1,3):
                for j in range(i+1, 4):
                    failMessage = f'Years are: {leap+i} and {leap+j}'
                    self.assertEqual(calander.countLeap(leap+i, leap+j),
                                         0, failMessage)
                
    def test_orderEqualsTrue(self):
        """Test 'countLeap' when 'order == True'.
        
        When computing 'countLeap(year1, year2, order=True)' if
        'year1' <= 'year2' no new processes occur in 'countLeap', it is
        the same set of code as 'countLeap(year1, year2, order=False)'
        and that is tested in the 'test_orderEqualsFalse' function.
        
        What remains to be tested is when 'order == True' and 'year2' < 'year1.'
        In this case the only piece of new code is the fact the current count
        is negated.

        What is tested is given 'year2' < 'year1' does the following hold:
            countLeap(year1, year2, order=True) = -countLeap(year2, year1)?

        """
        for yr2 in range(1950, 2200):
            for yr1 in range(yr2+1, 2201):
                self.assertEqual(calander.countLeap(yr1, yr2, order=True),
                                 -calander.countLeap(yr1, yr2))

class countLeapDaysTest(unittest.TestCase):
    """Test of 'countLeapDays' function."""

    def test_sameDay(self):
        """Test 'countLeapDays' when date paramaters are the same date."""

        #Same day on a leap year but the day is not a leap day
        failMessage = 'The dates are the same, on a leap year, not a leap day.'
        notLeap2024 = (29, 4, 2024)
        self.assertEqual(calander.countLeapDays(notLeap2024, notLeap2024),
                         0, failMessage)
        self.assertEqual(calander.countLeapDays(notLeap2024, notLeap2024, order=True),
                         0, failMessage + ' [order == True]')

        #Same day, and year is not a leap year
        failMessage = 'The dates are the same and not on a leap year.'
        notLeap2026 = (29, 4, 2026)
        self.assertEqual(calander.countLeapDays(notLeap2026, notLeap2026),
                         0, failMessage)
        self.assertEqual(calander.countLeapDays(notLeap2026, notLeap2026, order=True),
                         0, failMessage + ' [order == True]')
        #Same day, and day is a leap day
        failMessage = 'The dates are the same leap day.'
        leapDay2024 = (29, 2, 2024)
        self.assertEqual(calander.countLeapDays(leapDay2024, leapDay2024),
                         0, failMessage)
        self.assertEqual(
            calander.countLeapDays(leapDay2024, leapDay2024, order=True),
            0,
            failMessage + ' [order == True]')

    def test_sameYear(self):
        """Test 'countLeapDays' when the dates are on the same year.

        The unittest for same dates is done seperataly so assume that
        the dates are unique. Furthermore, when 'order == False', the other
        two parameters are interchangable. This allows, without loss of
        generality, to assume the first input is less than or equal to the
        second input. The equality cases was verified above, so it is assumed
        the first input is strictly less than the second input.
        
        When 'order == True' a new process is only run if 'date1' comes
        after 'date2', otherwise it is the same case as when 'order == False.'
        Thus when 'order == True' it can be assumed 'date1' comes after 'date2'

        """
        #Leap day between the two dates
        date1Cands = [(1,1,2024), (5,2,2024), (29,2,2024)]
        date2Cands = [(1,4,2024), (5,5,2024), (12,31,2024)]
        for date1 in date1Cands:
            for date2 in date2Cands:
                failMessage = f'Dates are: {date1} and {date2}.'
                self.assertEqual(calander.countLeapDays(date1, date2),
                                 1, failMessage)
                
                self.assertEqual(calander.countLeapDays(date2, date1, order=True),
                                 -1, failMessage + ' [order == True]')
                
        #Leap year but no leap days between the dates
        failMessage = 'Both dates are on a leap year, after the leap day.'
        date1Cands = [(1,3,2024), (10,3,2024), (30,3,2024)]
        date2Cands = [(1,4,2024), (5,5,2024), (31,12,2024)]
        for date1 in date1Cands:
            for date2 in date2Cands:
                self.assertEqual(calander.countLeapDays(date1, date2),
                                 0, failMessage)
                
                self.assertEqual(calander.countLeapDays(date2, date1, order=True),
                                 0, failMessage + ' [order == True]')       

        failMessage = 'Both dates are on a leap year, before or on the leap day.'
        date1Cands = [(1,1,2024), (5,2,2024), (10,2,2024)]
        date2Cands = [(12,2,2024), (28,2,2024), (29,2,2024)]
        for date1 in date1Cands:
            for date2 in date2Cands:
                self.assertEqual(calander.countLeapDays(date1, date2),
                                 0, failMessage)
                
                self.assertEqual(calander.countLeapDays(date2, date1, order=True),
                                 0, failMessage + ' [order == True]')

        #No leap between them not leap year
        failMessage = 'No date is on a leap year.'
        date1Cands = [(1,3,2025), (28,2,2025), (30,3,2025)]
        date2Cands = [(1,4,2025), (5,5,2025), (31,12,2025)]
        for date1 in date1Cands:
            for date2 in date2Cands:
                self.assertEqual(calander.countLeapDays(date1, date2),
                                 0, failMessage)
                
                self.assertEqual(calander.countLeapDays(date2, date1, order=True),
                                 0, failMessage + ' [order == True]')

    def test_differentYear(self):
        """Test 'countLeapDays' when the dates are on the different years.

        'countLeapDays' relies on 'countLeap' for multi-year calculations.
        The latter function is tested above in this file. The goal of this test file
        is to make sure 'countLeapDays' interacts with 'countLeap' as expected.
        For this we can assume the difference in years is any fixed number, 4 year
        differencers are assumed, to highlight any double leap year errors.

        Furthermore, when 'order == False', the other
        two parameters are interchangable. This allows, without loss of
        generality, to assume the first input is less than the
        second input.
        
        When 'order == True' a new process is only run if 'date1' comes
        after 'date2', otherwise it is the same case as when 'order == False.'
        Thus when 'order == True' it can be assumed 'date1' comes after 'date2'

        The examples to test are based on all combinations of the following diagram:
           Jan 1 20     Feb 29 20    Dec 31 20  Jan 1 24     Feb 29 24    Dec 31 24
               |------------|------------|..........|------------|------------|
               A     B     CD     E      F          G     H     IJ     K      L
        Where A, D, F, G, J, L are the dates written above them. C and I are
        one day before the leap day of that given year. B, E, H, K are dates
        between their respective surronding written dates.
        
        """
        preLeapOrLeap20 = [(1,1,20), (1,2,20), (28,2,20), (29,2,20)]
        afterLeap20 = [(1,5,20), (31,12,20)]
        preLeapOrLeap24 = [(1,1,24), (1,2,24), (28,2,24), (29,2,24)]
        postLeap24 = [(1,5,24), (31,12,24)]

        for date1 in preLeapOrLeap20:
            for date2 in preLeapOrLeap24:
                failMessage = f'Dates are: {date1}, {date2}'
                self.assertEqual(calander.countLeapDays(date1, date2),
                                 1, failMessage)
                
            for date2 in postLeap24:
                failMessage = f'Dates are: {date1}, {date2}'
                self.assertEqual(calander.countLeapDays(date1, date2),
                                 2, failMessage)

        for date1 in afterLeap20:
            for date2 in preLeapOrLeap24:
                failMessage = f'Dates are: {date1}, {date2}'
                self.assertEqual(calander.countLeapDays(date1, date2),
                                 0, failMessage)
                
            for date2 in postLeap24:
                failMessage = f'Dates are: {date1}, {date2}'
                self.assertEqual(calander.countLeapDays(date1, date2),
                                 1, failMessage)
              
        for date2 in preLeapOrLeap24:
            for date1 in preLeapOrLeap20:
                failMessage = f'Dates are: {date1}, {date2}'
                self.assertEqual(calander.countLeapDays(date2, date1, order=True),
                                 -1, failMessage + ' [order == True]')
                
            for date1 in afterLeap20:
                failMessage = f'Dates are: {date1}, {date2}'
                self.assertEqual(calander.countLeapDays(date2, date1, order=True),
                                 0, failMessage + ' [order == True]')

        for date2 in postLeap24:
            for date1 in preLeapOrLeap20:
                failMessage = f'Dates are: {date1}, {date2}'
                self.assertEqual(calander.countLeapDays(date2, date1, order=True),
                                 -2, failMessage + ' [order == True]')
                
            for date1 in afterLeap20:
                failMessage = f'Dates are: {date1}, {date2}'
                self.assertEqual(calander.countLeapDays(date2, date1, order=True),
                                 -1, failMessage + ' [order == True]')
        
class newYearsDayTest(unittest.TestCase):
    """Test of 'newYearsDay' function."""

    def test_results(self):
        """Test accurate results for the first day of a few years."""
        verifiedNewYearDays = {5: 'SAT', 1701: 'SAT',
                               1899: 'SUN', 2023: 'SUN',
                               2024: 'MON', 3988: 'FRI'} 
        for yr in verifiedNewYearDays:
            failMessage = f'Year is: {yr}'
            self.assertEqual(calander.newYearsDay(yr),
                             verifiedNewYearDays[yr], failMessage)

class weekOneTest(unittest.TestCase):
    """Test of 'weekOne' function."""

    def test_results(self):
        """Verify 'weekOne' functions results via 'newYearsDay' function."""
        
        oneWeek = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        cycWeek = oneWeek + oneWeek
        for yr in range(1999, 2007): #Range includes all unique starting days
            dayOne = calander.newYearsDay(yr)
            failMessage = f'Failure on start day {dayOne}'
            start = calander.orderingOfDays[dayOne]
            end = start + 7
            answer = {i:x for i, x in enumerate(cycWeek[start:end], 1)}
            self.assertEqual(calander.weekOne(yr), answer, failMessage)
            
class elapsedDaysTest(unittest.TestCase):
    """Test of 'elapsedDays' function."""

    def component_DateToStartYear(self, date):
        """Return numbers of days between a date and the start of the year.

        This is the component of 'elapsedDays' that reduces the function
        to one that computes the date after a number of days have elapsed
        from Jan 1 of a given year.
        
        """
        dayCount = 0
        day, month, year = date
        if calander.leapYear(year):
            dayCount += calander.daysElapsedLeap[month-1][0] + day - 1
        else:
            dayCount += calander.daysElapsed[month-1][0] + day - 1

        return dayCount

    def component_YearJumps(self, dayCount, year):
        """Return the number of years elapsed.

        This is the component of 'elapsedDays' that reduces the problem
        to computing the date after a number of days have elapsed
        from Jan 1 of a given year.
        
        """
        deltaYear = 0
        while dayCount >= (365 + calander.leapYear(year)):
            dayCount = dayCount - (365 + calander.leapYear(year))
            year += 1
            deltaYear += 1

        return deltaYear, dayCount

    def test_newYearsSameYear(self):
        """Starting from the new years, test cases the year does not change."""

        testCases = [0] * 366
        for mnth, (start, end) in enumerate(calander.daysElapsedLeap, 1):
            for j in range(start, end+1):
                date = (j-start+1, mnth, 2024)
                testCases[j] = date
                
        for addDays, date in enumerate(testCases):
            failMessage = f'Computing {addDays} after 2024.'
            self.assertEqual(calander.elapsedDays(addDays, 2024),
                             date, failMessage)

    def test_DateToStartYear(self):
        """Test computation of days a date is from the start of the year.

        Note the case this component is run iff 'newYearsSameYear' is not the
        case. The previous test shows 'elapsedDays' can handle the problem of
        returning the date when starting from the new years and when
        'dayCount' does not change the year. This allows this component
        to be independently tested by the 'elapsedDays.'
        
        """
        for ans in range(366):
            date = calander.elapsedDays(ans, 2024)
            failMessage = f'{ans} days after the Jan. 1 2024 is {date}.'
            self.assertEqual(self.component_DateToStartYear(date),
                             ans, failMessage)

    def test_YearJumps(self):
        """Test how function deals when 'dayCount' results in change in year."""

        years = [2020, 2024]
        for year in years:
            for yrJump in range(1,3):
                for daysOver in range(364):
                    dayCount = (365*yrJump
                                + calander.countLeap(year, year+yrJump)
                                + daysOver)
                    failMessage = (f'{dayCount} days from {year} is '
                                  +f'{yrJump} years, {daysOver} days.')
                    self.assertEqual(self.component_YearJumps(dayCount, year),
                                     (yrJump, daysOver), failMessage)
       
    def test_negativeCount(self):
        """Test 'elapsedDays' when 'dayCount' is negative.

        To test when 'dayCount' is negative note: if
        elapsedDays(N, date1) = date2 then elapsedDays(-N, date2) = date1.
        The case when 'dayCount' is non-negative is tested above, allowing
        the case of negative days to be easily tested.
        
        """
        dates = [(1,1,2020), (28,2,2000), (5,5,2023)]
        for date1 in dates:
            for localJump in range(100):
                for globalJump in [368, 700, 1000]:
                    N = (localJump + globalJump)
                    date2 = calander.elapsedDays(N, date1)
                    failMessage = f'Counting {-N} days before {date2}.'
                    self.assertEqual(calander.elapsedDays(-N, date2),
                                     date1, failMessage)

class parseDateTest(unittest.TestCase):
    """Test of 'parseDate' function."""

    def test_DayMonthYear(self):
        """Test parsing of dates given in day, month, then year order."""
        
        days = ['5', '11']
        punc = [' ', ',', '/', '-']
        months = ['Dec', 'DEC', 'december', 'Dec.']
        years = ['04', '2004']

        answers = {'5': (5, 12, 2004), '11': (11, 12, 2004)}
        for day in days:
            for p, q in zip(punc, punc):
                for month in months:
                    for year in years:
                        testInput = day + p + month + q + year
                        failMessage = f'Input is: {testInput}.'
                        self.assertEqual(calander.parseDate(testInput),
                                         answers[day], failMessage)

    def test_MonthDayYear(self):
        """Test parsing of dates given in month, day, then year order."""

        days = ['5', '11']
        punc = [' ', ',', '/', '-']
        months = ['Dec', 'DEC', 'december', 'Dec.', '12']
        years = ['04', '2004']

        answers = {'5': (5, 12, 2004), '11': (11, 12, 2004)}
        for day in days:
            for p, q in zip(punc, punc):
                for month in months:
                    for year in years:
                        testInput = month + p + day + q + year
                        failMessage = f'Input is: {testInput}.'
                        self.assertEqual(calander.parseDate(testInput),
                                         answers[day], failMessage)

class tradingDaysTest(unittest.TestCase):
    """Test of 'tradingDays' function."""

    def test_completeYear(self):
        """Test calculation of trading days for a complete year.

        The following special years are omitted:
            - 2012: Due to the extra closures caused by hurricane Sandy.
            - 2018: Due to extra clousre caused by death of a past president.
        
        """
        ans = {2010: 252, 2011: 252, 2013: 252, 2014: 252, 2015: 252,
               2016: 252, 2017: 251, 2019: 252, 2020: 253, 2021: 252,
               2022: 251, 2023: 250, 2024: 252}
        for year in ans:
            failMessage = f'Number of trading days in year {year}.'
            date1, date2 = (1, 1, year), (1, 1, year+1)
            self.assertEqual(calander.tradingDays(date1, date2),
                             ans[year], failMessage)

    def test_sameYear(self):
        """Test calculation of trading days for dates in the same year."""

        #Trading days by month for 2024
        monthDays = [21, 20, 20, 22, 22, 19, 22, 22, 20, 23, 20, 21]
        for mnth, ans in enumerate(monthDays, 1):

            failMessage = f'{ans} trading days in {calander.intToMonth[mnth]}'
            start = (1, mnth, 2024)
            end = (1, mnth+1, 2024) if mnth != 12 else (1, 1, 2025)
            self.assertEqual(calander.tradingDays(start, end),
                             ans, failMessage)

    def test_differentYears(self):
        """Test calculation of trading days for dates in different years."""
        
        yrDays = {2020: 253, 2021: 252, 2022: 251, 2023: 250, 2024: 252}
        yrJumpDays = sum([yrDays[x] for x in range(2021, 2024)])
        monthDays2020 = [21, 19, 22, 21, 20, 22, 22, 21, 21, 22, 20, 22]
        monthDays2024 = [21, 20, 20, 22, 22, 19, 22, 22, 20, 23, 20, 21]
        for mnth20, trDays20 in enumerate(monthDays2020, 1):
            for mnth24, trDays24 in enumerate(monthDays2024, 1):
                date20 = (1, mnth20, 2020)
                date24 = (1, mnth24, 2024)
                mnthJump20 = sum(monthDays2020[mnth20-1:])
                mnthJump24 = sum(monthDays2024[: mnth24-1])
                ans = yrJumpDays + mnthJump20 + mnthJump24
                failMessage = f'{ans} trading days from {date20} to {date24}'
                self.assertEqual(calander.tradingDays(date20, date24),
                                 ans, failMessage)
    
if __name__ == "__main__":
    unittest.main()
