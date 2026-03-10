import random
import math
import matplotlib.pyplot as plt

class GBM:
    def __init__(self, interval = 365, drift = 0, vol = 100 / 100, initialPrice = 100):
        self.interval = interval
        self.drift = drift
        self.vol = vol
        self.initialPrice = initialPrice

        self.driftConverted = drift / interval
        self.volConverted = vol / math.sqrt(interval)

        self.brownianMotion = [0]
        self.prices = [initialPrice]

    def createBrownianMotion(self):
        self.brownianMotion = [0]
        for t in range(self.interval):
            currentLocation = self.brownianMotion[-1]
            step = random.normalvariate(0, 1)
            nextLocation = currentLocation + step
            self.brownianMotion.append(nextLocation)

    def price(self, t):
        driftGrowth = math.exp(self.driftConverted * t)
        volDecay = math.exp(-self.volConverted**2/2 * t)
        brownianShock = math.exp(self.volConverted * self.brownianMotion[t])
        return self.initialPrice * driftGrowth * volDecay * brownianShock

    def simulate(self):
        self.createBrownianMotion()
        self.prices = [self.price(t) for t, brownianMotion in enumerate(self.brownianMotion)]

    def plot(self):
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(self.brownianMotion, color='blue')
        plt.title("Standard Brownian Motion")
        
        plt.subplot(1, 2, 2)
        plt.plot(self.prices, color='green')
        plt.title(f"GBM (Interval: {self.interval})")
        plt.show()