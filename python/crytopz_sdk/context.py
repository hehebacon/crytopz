class MarketAPI:


    def price(self, symbol):

        print(
            "[SDK] request price:",
            symbol
        )

        return 99950



class TradeAPI:


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




class BotContext:


    def __init__(self):

        self.market = MarketAPI()

        self.trade = TradeAPI()