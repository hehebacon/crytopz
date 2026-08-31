
from dataclasses import dataclass, field
import time


@dataclass
class BotState:

    running: bool = False

    trades: int = 0

    profit: float = 0.0

    last_action: str = ""

    logs: list = field(
        default_factory=list
    )


class BotRuntime:

    def __init__(self, bot, name="Bot"):

        self.bot = bot
        self.name = name

        self.state_data = BotState()

    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.state_data.running:
            return True

        try:

            if hasattr(self.bot, "on_start"):
                self.bot.on_start()

            self.state_data.running = True

            self.log(
                "Bot started"
            )

            return True

        except Exception as error:

            self.log(
                f"Start error: {type(error).__name__}: {error}"
            )

            self.state_data.running = False

            return False

    # =====================================================
    # TICK
    # =====================================================

    def tick(self):

        if not self.state_data.running:
            return None

        try:

            if not hasattr(
                self.bot,
                "on_tick"
            ):
                raise RuntimeError(
                    "Bot has no on_tick() method."
                )

            result = self.bot.on_tick()

            if isinstance(result, dict):

                action = result.get(
                    "action"
                )

                if action:

                    action = str(
                        action
                    ).upper()

                    self.state_data.last_action = action

                    if action in (
                        "BUY",
                        "SELL"
                    ):
                        self.state_data.trades += 1

            return result

        except Exception as error:

            self.log(
                f"Bot error: "
                f"{type(error).__name__}: {error}"
            )

            return None

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        if not self.state_data.running:
            return True

        try:

            if hasattr(
                self.bot,
                "on_stop"
            ):
                self.bot.on_stop()

        except Exception as error:

            self.log(
                f"Stop error: "
                f"{type(error).__name__}: {error}"
            )

        finally:

            self.state_data.running = False

            self.log(
                "Bot stopped"
            )

        return True

    # =====================================================
    # LOG
    # =====================================================

    def log(self, message):

        message = str(message)

        self.state_data.logs.append({
            "timestamp": time.time(),
            "message": message
        })

        if len(
            self.state_data.logs
        ) > 100:

            self.state_data.logs = (
                self.state_data.logs[-100:]
            )

        self.state_data.last_action = message

        print(
            f"[BotRuntime:{self.name}] "
            f"{message}"
        )

    # =====================================================
    # STATE
    # =====================================================

    def state(self):
        return self.state_data

    def is_running(self):
        return self.state_data.running

