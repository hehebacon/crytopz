class BotSDK:


    def __init__(
        self,
        bridge
    ):
        self.bridge = bridge



    def price(
        self,
        symbol
    ):

        print(
            "[SDK] request price:",
            symbol
        )


        return self.bridge.get_price(
            symbol
        )



    def buy(
        self,
        symbol,
        quantity
    ):

        print(
            "[SDK] BUY",
            symbol,
            quantity
        )


        return self.bridge.buy(
            symbol,
            quantity
        )



    def sell(
        self,
        symbol,
        quantity
    ):

        print(
            "[SDK] SELL",
            symbol,
            quantity
        )


        return self.bridge.sell(
            symbol,
            quantity
        )