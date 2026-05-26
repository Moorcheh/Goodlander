from theory import Option

contract = Option(
    symbol="HOOD",
    expiration="May 29",
    strike=75,
    option_type="call",
    price=1.49,
    delta=.4128,
    gamma=.0749
)

price = contract.calculatePrice(
    underlyingPrice=73.64,
    vol=.75,
    rate=.0365
    )
print(price)