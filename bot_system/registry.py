from pathlib import Path

from .manifest import BotManifest
from .validator import BotValidator


class BotRegistry:

    def __init__(self, bots_directory):

        self.bots_directory = Path(
            bots_directory
        )

        self.bots = {}

    def scan(self):

        self.bots.clear()

        self.bots_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        for bot_dir in sorted(
            self.bots_directory.iterdir()
        ):

            if not bot_dir.is_dir():
                continue

            manifest_path = (
                bot_dir / "manifest.json"
            )

            if not manifest_path.exists():

                print(
                    f"[BotRegistry] Skipping "
                    f"{bot_dir.name}: "
                    f"manifest.json missing"
                )

                continue

            try:

                manifest = BotManifest.load(
                    manifest_path
                )

                BotValidator.validate(
                    manifest,
                    bot_dir
                )

                if manifest.id in self.bots:

                    raise ValueError(
                        f"Duplicate bot id: "
                        f"{manifest.id}"
                    )

                self.bots[
                    manifest.id
                ] = {
                    "manifest": manifest,
                    "path": bot_dir,
                }

                print(
                    f"[BotRegistry] Valid: "
                    f"{manifest.id} "
                    f"v{manifest.version}"
                )

            except Exception as error:

                print(
                    f"[BotRegistry] Invalid bot "
                    f"{bot_dir.name}: "
                    f"{type(error).__name__}: "
                    f"{error}"
                )

    def get(self, bot_id):
        return self.bots.get(
            bot_id
        )

    def list(self):
        return list(
            self.bots.values()
        )