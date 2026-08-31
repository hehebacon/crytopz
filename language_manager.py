import json
from pathlib import Path


class LanguageManager:

    def __init__(self):

        self.root = Path(__file__).resolve().parent

        self.locale_dir = (
            self.root / "locales"
        )

        self.current = "vi"

        self.data = {}

        self.ensure_folder()

        self.load()



    def ensure_folder(self):

        if not self.locale_dir.exists():

            self.locale_dir.mkdir(
                exist_ok=True
            )



    def load(self):

        file = (
            self.locale_dir /
            f"{self.current}.json"
        )


        # Nếu chưa có file ngôn ngữ

        if not file.exists():

            with open(
                file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {},
                    f,
                    indent=4,
                    ensure_ascii=False
                )


        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                self.data = json.load(f)


        except Exception:

            self.data = {}



    def change(self, language):

        self.current = language

        self.load()



    def t(self, key):

        return self.data.get(
            key,
            key
        )



    def get_language(self):

        return self.current



    def available_languages(self):

        languages = []

        for file in self.locale_dir.glob(
            "*.json"
        ):

            languages.append(
                file.stem
            )

        return languages



# Singleton dùng toàn app

lang = LanguageManager()