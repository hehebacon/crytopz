class BotTest:

    def __init__(self, sdk):

        self.sdk = sdk

        self.has_traded = False

    # =====================================================
    # START
    # =====================================================

    def on_start(self):

        self.sdk.log(
            "Bot Test started"
        )

        self.has_traded = False

    # =====================================================
    # TICK
    # =====================================================

    def on_tick(self):

        symbol = "BTCUSDT"

        price = self.sdk.price(
            symbol
        )

        self.sdk.log(
            f"{symbol} price = ${price:,.2f}"
        )

        # BUY ONLY ONCE
        if not self.has_traded:

            quantity = 0.01

            order_id = self.sdk.buy(
                symbol,
                quantity
            )

            self.has_traded = True

            self.sdk.log(
                f"BUY {quantity} {symbol} "
                f"| Order #{order_id}"
            )

            return {
                "action": "BUY",
                "order_id": order_id,
            }

        return {
            "action": "HOLD"
        }

    # =====================================================
    # STOP
    # =====================================================

    def on_stop(self):

        self.sdk.log(
            "Bot Test stopped"
        )


def create_bot(sdk):

    return BotTest(
        sdk
    )