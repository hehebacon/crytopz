from python.crytopz_sdk import BotContext

import sys
from pathlib import Path


BOT_PATH = Path("bots/bot-test")

sys.path.insert(
    0,
    str(BOT_PATH)
)


from bot import create_bot


ctx = BotContext()

bot = create_bot()


bot.on_start(ctx)


for i in range(3):
    bot.on_tick(ctx)


bot.on_stop(ctx)