
from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass
class BotManifest:
    id: str
    name: str
    version: str
    api_version: str
    runtime: str
    entrypoint: str

    permissions: list[str] = field(default_factory=list)

    description: str = ""
    author: str = "Unknown"

    @classmethod
    def load(cls, path: str | Path):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"manifest.json not found: {path}"
            )

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError(
                "manifest.json must contain an object"
            )

        required = [
            "id",
            "name",
            "version",
            "api_version",
            "runtime",
            "entrypoint",
        ]

        for key in required:
            if key not in data:
                raise ValueError(
                    f"Missing manifest field: {key}"
                )

        permissions = data.get("permissions", [])

        if not isinstance(permissions, list):
            raise ValueError(
                "Manifest permissions must be a list"
            )

        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            version=str(data["version"]),
            api_version=str(data["api_version"]),
            runtime=str(data["runtime"]),
            entrypoint=str(data["entrypoint"]),
            permissions=permissions,
            description=str(data.get("description", "")),
            author=str(data.get("author", "Unknown")),
        )

    def save(self, path: str | Path):

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "api_version": self.api_version,
            "runtime": self.runtime,
            "entrypoint": self.entrypoint,
            "permissions": self.permissions,
            "description": self.description,
            "author": self.author,
        }

        with path.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

