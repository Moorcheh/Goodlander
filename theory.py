import math
from datetime import date, datetime
from zoneinfo import ZoneInfo


class Option:
    """
    A universal options contract object.
    Args:
        symbol      (str):   underlying ticker, e.g. "AAPL"
        expiration  (str):   expiration date in format, e.g. "May 21"
        strike      (float): strike price, e.g. 210.0
        option_type (str):   "call" or "put"
        price       (float): market price of the option, e.g. 3.50
        delta       (float): delta greek, e.g. 0.45
        gamma       (float): gamma greek, e.g. 0.08
    """

    # construct the option object
    def __init__(
        self,
        symbol: str,
        expiration: str,
        strike: float,
        option_type: str,
        price: float,
        delta: float,
        gamma: float,
    ):
        self.symbol      = symbol.upper().strip()
        self.expiration  = expiration
        self.strike      = strike
        self.option_type = option_type.lower().strip()
        self.price       = price
        self.delta       = delta
        self.gamma       = gamma

        # check if option type is valid
        if self.option_type not in ("call", "put"):
            raise ValueError(f"option_type must be 'call' or 'put', got '{self.option_type}'")

    # convert expiration date to time to expiration (in years)
    def timeToExpiration(self, expirationDate: str) -> float:
        """
        Converts an expiration date string to precise time in years.
        Assumes expiration is at 1:00 PM California time (Pacific Time).

        Accepted formats:
            "May 21"        — assumes current year
            "Jan 15, 2027"  — uses the specified year
        """
        # Define the California timezone
        pt_zone = ZoneInfo("America/Los_Angeles")
        now = datetime.now(pt_zone)

        # Parse the date
        try:
            expiry_dt = datetime.strptime(expirationDate, "%b %d, %Y")
        except ValueError:
            expiry_dt = datetime.strptime(expirationDate, "%b %d").replace(year=now.year)

        # Attach the timezone and set expiration time to 1:00 PM (13:00:00)
        expiry = expiry_dt.replace(hour=13, minute=0, second=0, microsecond=0, tzinfo=pt_zone)

        # Calculate exact seconds to expiration
        seconds_to_expiry = (expiry - now).total_seconds()

        # Floor at 0 in case the contract has already expired
        seconds_to_expiry = max(0.0, seconds_to_expiry)

        # Return as a fractional year (365 days * 24 hours * 3600 seconds)
        return seconds_to_expiry / (365 * 24 * 3600)

    # define the cumulative distribution function
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

    # calculate new option price at specified underlying price
    def calculatePrice(self, underlyingPrice, vol, rate):
        if self.option_type == "call":
            timeToExpiration = self.timeToExpiration(self.expiration)
            discountFactor = math.exp(-rate * timeToExpiration)
            strikeGrowth = math.log(underlyingPrice / self.strike)
            otherGrowth = (rate - vol**2/2) * timeToExpiration
            standardDeviation = vol * math.sqrt(timeToExpiration)
            d2 = (strikeGrowth + otherGrowth) / standardDeviation
            d1 = d2 + standardDeviation
            Nd2 = self.CDF(d2)
            Nd1 = self.CDF(d1)
            valueAboveStrike = underlyingPrice * Nd1
            costOfStrike = self.strike * Nd2 * discountFactor
            return valueAboveStrike - costOfStrike

    # build the representation of the option object itself
    def __repr__(self):
        return (
            f"Option({self.symbol} {self.expiration} "
            f"${self.strike} {self.option_type.upper()} | "
            f"price={self.price}, delta={self.delta}, gamma={self.gamma})"
        )
