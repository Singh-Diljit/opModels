class American(Option):
    def __init__(self, stock, K, r, T, payOff, startDate=()):
        super().__init__(stock, K, r, T, payOff, startDate)
        self.optionType = f'American {payOff.__name__}'

class Bermuda(Option):
    def __init__(self, stock, K, r, T, exerciseDates, payOff, startDate=()):
        super().__init__(stock, K, r, T, payOff, startDate)
        self.exDates = timeList(exerciseDates)
        self.optionType = f'Bermuda {payOff.__name__}'

    def __repr__(self):
        return super().__repr__() + f'exerciseTimes: {self.exDates}'

    def __str__(self):
        return super().__str__() + '\n' + f'exerciseDates: {self.exDates}'

from hestonDirect import heston as heston_
from blackScholesMerton import BSM

class European(Option):
    def __init__(self, stock, K, r, T, payOff, startDate=()):
        super().__init__(stock, K, r, T, payOff, startDate)
        self.optionType = f'European {payOff.__name__}'

    @property
    def hes(self):
        S, q, vol, var, rateVar, longVar, volVol, cor = self.stock.unload('heston')
        K, r, T, payOffType, now = self.unload
        return heston_(S, K, var, r, q.rate, T, rateVar, longVar, volVol, cor, self.call)

    @property
    def BSM(self):
        S, q, vol = self.stock.unload('BSM')
        K, r, T, payOffType, now = self.unload
        return BSM(S, K, r, T, vol, q.rate, self.call)

st = Stock(S=100, q=.2, vol=.2, kappa=1, theta=.22, xi=.3)
A = European(st, 105, .1, 1, put)
print(A.BSM)
