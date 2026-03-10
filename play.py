from GBM import GBM
from Options import Option
import matplotlib.pyplot as plt

priceModel = GBM(interval = 390, vol = 1 / 100, initialPrice = 680)
priceModel.simulate()
prices = priceModel.prices

contractPrices = []
for i, price in enumerate(prices):
    contract = Option(strike = 684, vol = 1 / 100)
    contract.set_daysToExpiration( (len(prices) - (i + 1)) / 60 / 24)
    contract.set_underlyingPrice(price)
    contractPrice = contract.call()
    contractPrices.append(contractPrice)

plt.plot(prices)
plt.show()

plt.plot(contractPrices)
plt.show()