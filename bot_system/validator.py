from pathlib import Path

SUPPORTED_API_VERSION = "1.0"
SUPPORTED_RUNTIME = "python"

ALLOWED_PERMISSIONS = {
    "market.read",
    "account.read",
    "order.create",
    "order.cancel"
}


class ValidationError(Exception):
    pass


class BotValidator:

    @staticmethod
    def validate(manifest, bot_dir: str | Path):
        bot_dir = Path(bot_dir)

        if not manifest.id:
            raise ValidationError("Bot ID is empty")

        if not manifest.name:
            raise ValidationError("Bot name is empty")

        if manifest.api_version != SUPPORTED_API_VERSION:
            raise ValidationError(
                f"Unsupported API version: {manifest.api_version}"
            )

        if manifest.runtime != SUPPORTED_RUNTIME:
            raise ValidationError(
                f"Unsupported runtime: {manifest.runtime}"
            )

        entrypoint = bot_dir / manifest.entrypoint

        if not entrypoint.exists():
            raise ValidationError(
                f"Entrypoint not found: {entrypoint}"
            )

        for permission in manifest.permissions:
            if permission not in ALLOWED_PERMISSIONS:
                raise ValidationError(
                    f"Unknown permission: {permission}"
                )

        return True