
import importlib.util
from pathlib import Path

from .api import BotAPI


class BotLoader:

    def __init__(self, core=None):
        self.core = core

    def load(self, bot_dir, manifest):

        bot_dir = Path(bot_dir)

        entrypoint = (
            bot_dir /
            manifest.entrypoint
        )

        if not entrypoint.exists():
            raise FileNotFoundError(
                f"Entrypoint not found: {entrypoint}"
            )

        module_name = (
            f"crytopz_bot_{manifest.id}"
        )

        spec = importlib.util.spec_from_file_location(
            module_name,
            entrypoint
        )

        if spec is None or spec.loader is None:
            raise RuntimeError(
                f"Cannot load bot: {manifest.id}"
            )

        module = importlib.util.module_from_spec(
            spec
        )

        spec.loader.exec_module(module)

        api = BotAPI(
            core=self.core,
            permissions=manifest.permissions
        )

        # -------------------------------------------------
        # NEW STANDARD
        # -------------------------------------------------

        bot_class = getattr(
            module,
            "CrytopzBot",
            None
        )

        if bot_class is not None:

            try:
                return bot_class(api)
            except TypeError:
                return bot_class(
                    sdk=api,
                    strategy=None
                )

        # -------------------------------------------------
        # FACTORY
        # -------------------------------------------------

        create_bot = getattr(
            module,
            "create_bot",
            None
        )

        if create_bot is not None:

            try:
                return create_bot(
                    api
                )
            except TypeError:

                return create_bot(
                    sdk=api,
                    strategy=None
                )

        raise RuntimeError(
            f"Bot {manifest.id} must contain "
            f"'CrytopzBot' or 'create_bot()'."
        )

