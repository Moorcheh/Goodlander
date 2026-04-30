from Strategies import Strategies
from GBM import GBM
import matplotlib.pyplot as plt

priceModel = GBM(drift = 10 / 100)

# test strategies 
buyAndhold = []
follower = []
contrarian = []

iterations = 100000
for i in range(iterations):
    priceModel.simulate()
    stratego = Strategies(priceModel.prices)
    buyAndholdResults = stratego.buyAndhold()
    followerResults = stratego.follower()
    contrarianResults = stratego.contrarian()
    buyAndhold.append(buyAndholdResults[-1] - buyAndholdResults[0])
    follower.append(followerResults[-1] - followerResults[0])
    contrarian.append(contrarianResults[-1] - contrarianResults[0])

# statistics
buy_avg = sum(buyAndhold) / len(buyAndhold)
buyAndHoldStats = {
    'avg': buy_avg,
    'std': (sum([(x - buy_avg)**2 for x in buyAndhold]) / len(buyAndhold))**0.5,
}

fol_avg = sum(follower) / len(follower)
followerStats = {
    'avg': fol_avg,
    'std': (sum([(x - fol_avg)**2 for x in follower]) / len(follower))**0.5,
}

con_avg = sum(contrarian) / len(contrarian)
contrarianStats = {
    'avg': con_avg,
    'std': (sum([(x - con_avg)**2 for x in contrarian]) / len(contrarian))**0.5,
}

print("=" * 55)
print(f" 📈 MONTE CARLO SIMULATION RESULTS ({iterations} Iterations) ")
print("=" * 55)
print(f"{'Strategy':<15} | {'Average PnL':>15} | {'Std Dev (Risk)':>15}")
print("-" * 55)
print(f"{'Buy & Hold':<15} | {buyAndHoldStats['avg']:>15.2f} | {buyAndHoldStats['std']:>15.2f}")
print(f"{'Follower':<15} | {followerStats['avg']:>15.2f} | {followerStats['std']:>15.2f}")
print(f"{'Contrarian':<15} | {contrarianStats['avg']:>15.2f} | {contrarianStats['std']:>15.2f}")
print("=" * 55)

# plt.hist(buyAndhold, bins = 500)
# plt.show()