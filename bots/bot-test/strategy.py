from bot_system.strategy import Signal


class SimpleStrategy:


    def on_price(
        self,
        symbol,
        price
    ):

        print(
            "[STRATEGY] checking:",
            symbol,
            price
        )


        if price < 100000:
            return Signal.BUY


        return Signal.SELL