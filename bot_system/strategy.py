from enum import Enum


class Signal(Enum):
    HOLD = 0
    BUY = 1
    SELL = 2



class Strategy:

    def on_price(
        self,
        symbol,
        price
    ):
        return Signal.HOLD