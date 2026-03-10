import math

class Option:
    def __init__(self, daysToExpiration = 5, strike = 100, rate = 4 / 100, vol = 100 / 100, underlyingPrice = 100):
        self.daysToExpiration = daysToExpiration
        self.strike = strike
        self.rate = rate
        self.vol = vol
        self.underlyingPrice = underlyingPrice
        
    def CDF(self, x):
        # return 1/2 + (x - x**3/6 + x**5/40 - x**7/336 + x**9/3456 - x**11/42240) / math.sqrt(2*math.pi)
        steps = 100
        dx = x / steps
        I = 0
        for n in range(steps):
            loc = n * dx
            I += math.exp(-loc**2/2) * dx
        N = 1/2 + I / math.sqrt(2*math.pi)
        if N > 1: return 1
        elif N < 0: return 0
        else: return N 

    def call(self):
        if self.daysToExpiration == 0: return max(0, self.underlyingPrice - self.strike)

        timeToExpiration = self.daysToExpiration / 365
        discountFactor = math.exp(-self.rate * timeToExpiration)

        strikeGrowth = math.log(self.underlyingPrice / self.strike)
        otherGrowth = (self.rate - self.vol**2/2) * timeToExpiration
        standardDeviation = self.vol * math.sqrt(timeToExpiration)

        d2 = (strikeGrowth + otherGrowth) / standardDeviation
        d1 = d2 + standardDeviation
        Nd2 = self.CDF(d2)
        Nd1 = self.CDF(d1)

        valueAboveStrike = self.underlyingPrice * Nd1
        costOfStrike = self.strike * Nd2 * discountFactor
        return valueAboveStrike - costOfStrike

    def set_daysToExpiration(self, dte): self.daysToExpiration = dte

    def set_underlyingPrice(self, price): self.underlyingPrice = price