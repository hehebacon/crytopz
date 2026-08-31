from pathlib import Path

from .loader import BotLoader
from .runtime import BotRuntime
from .registry import BotRegistry


class BotManager:

    def __init__(
        self,
        bots_directory=None,
        bots_dir=None,
        core=None
    ):
        if bots_directory is None:
            bots_directory = bots_dir

        if bots_directory is None:
            raise ValueError("Bot directory is required.")

        self.bots_dir = Path(bots_directory)
        self.core = core
        self.registry = BotRegistry(self.bots_dir)
        self.loader = BotLoader(core=self.core)
        self.bots = {}
        self.runtimes = {}
        self.reload()

    def reload(self):
        self.stop_all()
        self.bots.clear()
        self.runtimes.clear()

        self.bots_dir.mkdir(parents=True, exist_ok=True)
        self.registry.scan()

        for bot_id, entry in self.registry.bots.items():
            manifest = entry["manifest"]
            bot_path = entry["path"]

            self.bots[bot_id] = {
                "id": manifest.id,
                "name": manifest.name,
                "version": manifest.version,
                "manifest": manifest,
                "path": bot_path,
                "instance": None,
                "runtime": None,
            }

    def list_bots(self):
        return list(self.bots.values())

    def get_bot(self, bot_id):
        bot = self.bots.get(bot_id)
        if bot is not None:
            return bot

        for bot in self.bots.values():
            if bot["name"] == bot_id:
                return bot

        return None

    def load_bot(self, bot_id):
        bot = self.get_bot(bot_id)

        if bot is None:
            return None

        if bot["instance"] is not None:
            return bot["instance"]

        try:
            instance = self.loader.load(bot["path"], bot["manifest"])
            bot["instance"] = instance
            return instance
        except Exception as error:
            print(f"[BotManager] Failed to load {bot['name']}: {error}")
            return None

    def start_bot(self, bot_id):
        bot = self.get_bot(bot_id)

        if bot is None:
            print(f"[BotManager] Bot not found: {bot_id}")
            return False

        instance = self.load_bot(bot_id)
        if instance is None:
            return False

        runtime = bot.get("runtime")
        if runtime is None:
            runtime = BotRuntime(instance, name=bot["name"])
            bot["runtime"] = runtime
            self.runtimes[bot["id"]] = runtime

        runtime.start()
        return True

    def stop_bot(self, bot_id):
        bot = self.get_bot(bot_id)

        if bot is None:
            return False

        runtime = bot.get("runtime")
        if runtime is None:
            return True

        runtime.stop()
        return True

    def toggle_bot(self, bot_id):
        if self.is_running(bot_id):
            return self.stop_bot(bot_id)
        return self.start_bot(bot_id)

    def tick(self):
        for runtime in list(self.runtimes.values()):
            if not runtime.is_running():
                continue

            try:
                runtime.tick()
            except Exception as error:
                print(f"[BotManager] Runtime error: {error}")

    def is_running(self, bot_id):
        bot = self.get_bot(bot_id)

        if bot is None:
            return False

        runtime = bot.get("runtime")
        if runtime is None:
            return False

        return runtime.is_running()

    def get_instance(self, bot_id):
        bot = self.get_bot(bot_id)

        if bot is None:
            return None

        return bot.get("instance")

    def get_runtime(self, bot_id):
        bot = self.get_bot(bot_id)

        if bot is None:
            return None

        return bot.get("runtime")

    def stop_all(self):
        for bot_id in list(self.bots.keys()):
            try:
                self.stop_bot(bot_id)
            except Exception as error:
                print(f"[BotManager] Stop error: {error}")

    def unload_bot(self, bot_id):
        bot = self.get_bot(bot_id)

        if bot is None:
            return False

        runtime = bot.get("runtime")
        if runtime is not None:
            try:
                runtime.stop()
            except Exception as error:
                print(f"[BotManager] Unload error: {error}")

        self.runtimes.pop(bot["id"], None)
        bot["runtime"] = None
        bot["instance"] = None

        return True

    def reload_bot(self, bot_id):
        was_running = self.is_running(bot_id)

        self.unload_bot(bot_id)
        self.reload()

        if was_running:
            return self.start_bot(bot_id)

        return self.get_bot(bot_id) is not None