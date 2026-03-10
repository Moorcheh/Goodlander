class Strategies:
    def __init__(self, prices):
        self.prices = prices

    # trading strategy: buy & hold
    def buyAndhold(self):
        buyAndhold = [0]
        position = 0
        for t, price in enumerate(self.prices):
            if t == 0:
                position = 1
            elif t == len(self.prices) - 1:
                pnl = price - self.prices[0]
                buyAndhold.append(pnl)
            else: buyAndhold.append(0)
        return buyAndhold

    # trading strategy: follower
    def follower(self):
        follower = [0]
        position = 0
        for t, price in enumerate(self.prices):
            currentBalance = follower[-1]
            if t == 0: continue
            yesterday = self.prices[t - 1]
            change = price - yesterday
            if position != 0: 
                pnl = change * position
                follower.append(currentBalance + pnl)
            else: follower.append(currentBalance)
            if change > 0: position = 1
            elif change < 0: position = -1
            else: continue
        return follower

    # trading strategy: contrarian
    def contrarian(self):
        contrarian = [0]
        position = 0
        for t, price in enumerate(self.prices):
            currentBalance = contrarian[-1]
            if t == 0: continue
            yesterday = self.prices[t - 1]
            change = price - yesterday
            if position != 0: 
                pnl = change * position
                contrarian.append(currentBalance + pnl)
            else: contrarian.append(currentBalance)
            if change > 0: position = -1
            elif change < 0: position = 1
            else: continue
        return contrarian