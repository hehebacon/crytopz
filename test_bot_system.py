from pathlib import Path
import sys
import random


ROOT = Path(__file__).resolve().parent


BOT_PATH = ROOT / "bots" / "bot-test"


sys.path.insert(
    0,
    str(BOT_PATH)
)


from bot import create_bot

from bot_system.sdk import BotSDK
from strategy import SimpleStrategy



# =========================
# Mock Bridge
# =========================

class Bridge:


    def __init__(self):

        self.next_order_id = 1

        self.orders = []



    def get_price(
        self,
        symbol
    ):

        print(
            "[BRIDGE] get price:",
            symbol
        )


        return random.randint(
            99800,
            100100
        )



    def buy(
        self,
        symbol,
        quantity
    ):

        order_id = self.next_order_id

        self.next_order_id += 1


        order = {
            "id": order_id,
            "symbol": symbol,
            "side": "BUY",
            "quantity": quantity
        }


        self.orders.append(order)


        print(
            "[BRIDGE] BUY:",
            symbol,
            quantity,
            "ID:",
            order_id
        )


        return order_id



    def sell(
        self,
        symbol,
        quantity
    ):

        order_id = self.next_order_id

        self.next_order_id += 1


        order = {
            "id": order_id,
            "symbol": symbol,
            "side": "SELL",
            "quantity": quantity
        }


        self.orders.append(order)


        print(
            "[BRIDGE] SELL:",
            symbol,
            quantity,
            "ID:",
            order_id
        )


        return order_id



    def history(self):

        return self.orders




# =========================
# Runtime
# =========================

class BotRuntime:


    def __init__(
        self,
        bot,
        ticks=3
    ):

        self.bot = bot
        self.ticks = ticks



    def start(self):

        print(
            "[Runtime] Starting bot..."
        )


        self.bot.on_start()



        for i in range(self.ticks):

            print(
                f"[Runtime] Tick {i+1}"
            )

            self.bot.on_tick()



    def stop(self):

        print(
            "[Runtime] Stopping bot..."
        )


        self.bot.on_stop()




# =========================
# Main
# =========================

print(
    "=== crytopz Bot System ==="
)


bridge = Bridge()


sdk = BotSDK(
    bridge
)


strategy = SimpleStrategy()



bot = create_bot(
    sdk,
    strategy
)



runtime = BotRuntime(
    bot,
    ticks=3
)



runtime.start()

runtime.stop()



print()


print(
    "=== Order History ==="
)


for order in bridge.history():

    print(
        f"#{order['id']} "
        f"{order['side']} "
        f"{order['symbol']} "
        f"qty={order['quantity']}"
    )



print()


print(
    "=== Done ==="
)