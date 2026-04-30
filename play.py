from GBM import GBM
from Options import Option
import matplotlib.pyplot as plt
from math import exp

priceModel = GBM(interval = 365, drift = .1, vol = 16 / 100, initialPrice = 711)
paths = priceModel.simulate(N = 1000, plot = False)

contractPaths = []
for _, prices in enumerate(paths):
    contractPrices = []
    for i, price in enumerate(prices):
        contract = Option(strike = 711, vol = 16 / 100)
        contract.set_daysToExpiration( (len(prices) - (i + 1)) / 365)
        contract.set_underlyingPrice(price)
        contractPrice = contract.call()
        contractPrices.append(contractPrice)
    contractPaths.append(contractPrices)

plt.figure(figsize=(16, 7))
for i in range(len(paths)):
    plt.subplot(1, 2, 1)
    plt.plot(paths[i])
    plt.title("Underlying Price")

    plt.subplot(1, 2, 2)
    plt.plot(contractPaths[i])
    plt.title(f"Call Contract")
# plt.show()

theoreticalFinalPrice = 711 * exp(.1)
averageFinalPrice = sum([prices[-1] / len(paths) for prices in paths])
error = (theoreticalFinalPrice - averageFinalPrice) / theoreticalFinalPrice
print("price statistics:", theoreticalFinalPrice, averageFinalPrice, error)

# theoreticalFinalCall = theoreticalFinalPrice - 711
theoreticalFinalCall = Option(
    daysToExpiration=365,
    strike=711,
    rate=.1,
    vol=.16,
    underlyingPrice=711
).call() * exp(.1)
averageFinalCall = sum([contractPrices[-1] / len(contractPaths) for contractPrices in contractPaths])
errorCall = (theoreticalFinalCall - averageFinalCall) / theoreticalFinalCall
print("contract statistics:", theoreticalFinalCall, averageFinalCall, errorCall)

marketPrice = Option(
    daysToExpiration=365,
    strike=711,
    rate=.1,
    vol=.16,
    underlyingPrice=711
).call()
print(marketPrice)