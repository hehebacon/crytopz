from bot_system.strategy import Signal


class CrytopzBot:

    def __init__(self, api):
        self.api = api

    def on_start(self):
        self.api.log("Bot Test started")

    def on_tick(self):
        symbol = "BTCUSDT"

        price = self.api.market.get_price(symbol)

        if price is None:
            self.api.log("BTCUSDT price unavailable")
            return

        self.api.log(f"BTCUSDT price: {price}")

        # Test strategy:
        # BUY when tick is received.
        signal = Signal.BUY

        self.api.log(f"Signal: {signal.name}")

        if signal == Signal.BUY:
            order_id = self.api.order.buy(symbol, 0.01)
            self.api.log(f"BUY order: {order_id}")
        elif signal == Signal.SELL:
            order_id = self.api.order.sell(symbol, 0.01)
            self.api.log(f"SELL order: {order_id}")
        else:
            self.api.log("No trading action")

    def on_stop(self):
        self.api.log("Bot Test stopped")