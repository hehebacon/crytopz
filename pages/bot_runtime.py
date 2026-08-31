from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
import time


# =========================================================
# BOT STATE
# =========================================================

@dataclass
class BotState:

    trades: int = 0

    profit: float = 0.0

    last_action: str = ""

    logs: List[dict] = field(
        default_factory=list
    )


# =========================================================
# BOT INSTANCE
# =========================================================

class BotInstance:

    def __init__(
        self,
        name: str,
        path: Path,
        manifest: dict
    ):

        self.name = name

        self.path = path

        self.manifest = manifest

        self.running = False

        self._state = BotState()


    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.running:
            return True

        self.running = True

        self.log("Bot started")

        return True


    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        if not self.running:
            return True

        self.running = False

        self.log("Bot stopped")

        return True


    # =====================================================
    # TOGGLE
    # =====================================================

    def toggle(self):

        if self.running:
            return self.stop()

        return self.start()


    # =====================================================
    # STATUS
    # =====================================================

    def is_running(self):

        return self.running


    # =====================================================
    # STATE
    # =====================================================

    def state(self):

        return self._state


    # =====================================================
    # LOG
    # =====================================================

    def log(self, message):

        self._state.logs.append({

            "timestamp": time.time(),

            "message": str(message)

        })

        if len(self._state.logs) > 100:

            self._state.logs = (
                self._state.logs[-100:]
            )

        self._state.last_action = str(
            message
        )


    # =====================================================
    # TRADE
    # =====================================================

    def record_trade(
        self,
        profit: float = 0.0
    ):

        self._state.trades += 1

        self._state.profit += float(
            profit
        )

        self.log(
            f"Trade #{self._state.trades}"
        )


    # =====================================================
    # RESET STATE
    # =====================================================

    def reset_state(self):

        self._state = BotState()


# =========================================================
# BOT RUNTIME / MANAGER
# =========================================================

class BotRuntime:

    def __init__(self, bots_dir):

        self.bots_dir = Path(
            bots_dir
        )

        self.bots: Dict[
            str,
            BotInstance
        ] = {}

        self.load_bots()


    # =====================================================
    # LOAD
    # =====================================================

    def load_bots(self):

        self.bots.clear()

        self.bots_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        for bot_dir in self.bots_dir.iterdir():

            if not bot_dir.is_dir():
                continue

            manifest = self.load_manifest(
                bot_dir
            )

            name = manifest.get(
                "name",
                bot_dir.name
            )

            self.bots[name] = BotInstance(

                name=name,

                path=bot_dir,

                manifest=manifest

            )


    # =====================================================
    # MANIFEST
    # =====================================================

    def load_manifest(
        self,
        bot_dir: Path
    ):

        manifest_file = (
            bot_dir / "manifest.json"
        )

        if not manifest_file.exists():

            return {

                "name": bot_dir.name,

                "version": "unknown",

                "description": "No manifest",

                "author": "unknown",

                "type": "strategy",

                "api_version": "1",

                "entry": "main.py"

            }


        try:

            with open(
                manifest_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if not isinstance(
                    data,
                    dict
                ):

                    raise ValueError(
                        "Manifest must be an object"
                    )

                return data


        except Exception as e:

            return {

                "name": bot_dir.name,

                "version": "invalid",

                "description":
                    f"Invalid manifest.json: {e}",

                "author": "unknown",

                "type": "strategy",

                "api_version": "1",

                "entry": "main.py"

            }


    # =====================================================
    # LIST
    # =====================================================

    def list_bots(self):

        return list(
            self.bots.values()
        )


    # =====================================================
    # GET
    # =====================================================

    def get_bot(
        self,
        name: str
    ) -> Optional[BotInstance]:

        return self.bots.get(
            name
        )


    # =====================================================
    # START
    # =====================================================

    def start_bot(
        self,
        name: str
    ):

        bot = self.get_bot(
            name
        )

        if bot is None:

            return False

        return bot.start()


    # =====================================================
    # STOP
    # =====================================================

    def stop_bot(
        self,
        name: str
    ):

        bot = self.get_bot(
            name
        )

        if bot is None:

            return False

        return bot.stop()


    # =====================================================
    # TOGGLE
    # =====================================================

    def toggle_bot(
        self,
        name: str
    ):

        bot = self.get_bot(
            name
        )

        if bot is None:

            return False

        return bot.toggle()


    # =====================================================
    # LOG
    # =====================================================

    def log(
        self,
        name: str,
        message: str
    ):

        bot = self.get_bot(
            name
        )

        if bot is None:
            return

        bot.log(
            message
        )


    # =====================================================
    # RELOAD
    # =====================================================

    def reload(self):

        old_states = {}

        for name, bot in self.bots.items():

            old_states[name] = {

                "running":
                    bot.running,

                "trades":
                    bot.state().trades,

                "profit":
                    bot.state().profit,

                "last_action":
                    bot.state().last_action,

                "logs":
                    list(
                        bot.state().logs
                    )

            }


        self.load_bots()


        for name, state in old_states.items():

            bot = self.bots.get(
                name
            )

            if bot is None:
                continue


            bot.running = (
                state["running"]
            )


            bot.state().trades = (
                state["trades"]
            )


            bot.state().profit = (
                state["profit"]
            )


            bot.state().last_action = (
                state["last_action"]
            )


            bot.state().logs = (
                state["logs"]
            )


    # =====================================================
    # STOP ALL
    # =====================================================

    def stop_all(self):

        for bot in self.bots.values():

            bot.stop()


    # =====================================================
    # RESET ALL STATES
    # =====================================================

    def reset_states(self):

        for bot in self.bots.values():

            bot.reset_state()


    # =====================================================
    # BOT COUNT
    # =====================================================

    def count(self):

        return len(
            self.bots
        )


    # =====================================================
    # RUNNING COUNT
    # =====================================================

    def running_count(self):

        return sum(

            1

            for bot in self.bots.values()

            if bot.is_running()

        )