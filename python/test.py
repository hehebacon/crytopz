from crytopz import Crytopz

core = Crytopz(10000.0)

core.update_market(
    "BTCUSDT",
    100000,
    100010,
    100005,
    1
)

print("Price:", core.price("BTCUSDT"))

order = core.buy(
    "BTCUSDT",
    0.01
)

print("Order:", order)
print("Balance:", core.balance())
print("Position:", core.position("BTCUSDT"))

core.close()