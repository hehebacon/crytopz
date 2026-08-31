import customtkinter as ctk

from language_manager import lang


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.app = app

        self.build_ui()


    def build_ui(self):

        ctk.CTkLabel(
            self,
            text=lang.t("settings"),
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(25,20)
        )


        container = ctk.CTkFrame(
            self,
            corner_radius=14
        )

        container.pack(
            fill="x",
            padx=25
        )


        # Appearance

        ctk.CTkLabel(
            container,
            text=lang.t("appearance"),
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18,10)
        )


        row = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=5
        )


        ctk.CTkLabel(
            row,
            text=lang.t("theme")
        ).pack(
            side="left"
        )


        self.theme = ctk.CTkOptionMenu(
            row,
            values=[
                "Dark",
                "Light",
                "System"
            ],
            command=self.change_theme
        )

        self.theme.set(
            "Dark"
        )

        self.theme.pack(
            side="right"
        )



        # Language

        ctk.CTkLabel(
            container,
            text=lang.t("language"),
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20,10)
        )


        row_lang = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        row_lang.pack(
            fill="x",
            padx=20,
            pady=5
        )


        ctk.CTkLabel(
            row_lang,
            text=lang.t("app_language")
        ).pack(
            side="left"
        )


        self.language = ctk.CTkOptionMenu(
            row_lang,
            values=[
                "Vietnamese",
                "English"
            ],
            command=self.change_language
        )


        if lang.get_language() == "en":

            self.language.set(
                "English"
            )

        else:

            self.language.set(
                "Vietnamese"
            )


        self.language.pack(
            side="right"
        )



        # Trading

        ctk.CTkLabel(
            container,
            text=lang.t("trading"),
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20,10)
        )


        row3 = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )


        row3.pack(
            fill="x",
            padx=20,
            pady=5
        )


        ctk.CTkLabel(
            row3,
            text=lang.t("default_asset")
        ).pack(
            side="left"
        )


        self.asset = ctk.CTkOptionMenu(
            row3,
            values=[
                "BTCUSDT",
                "ETHUSDT",
                "SOLUSDT"
            ]
        )


        self.asset.set(
            "BTCUSDT"
        )


        self.asset.pack(
            side="right"
        )



        # Paper

        ctk.CTkLabel(
            container,
            text=lang.t("paper_account"),
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20,10)
        )


        ctk.CTkLabel(
            container,
            text=lang.t("starting_balance"),
            text_color="gray"
        ).pack(
            anchor="w",
            padx=20
        )


        ctk.CTkButton(
            container,
            text=lang.t("reset_account"),
            height=38,
            command=self.reset_account
        ).pack(
            fill="x",
            padx=20,
            pady=15
        )



        ctk.CTkLabel(
            container,
            text="crytopz v0.1.0  •  Paper Trading",
            text_color="gray"
        ).pack(
            pady=(0,18)
        )



    def change_theme(self, value):

        modes = {

            "Dark":"dark",
            "Light":"light",
            "System":"system"

        }


        ctk.set_appearance_mode(
            modes[value]
        )



    def change_language(self, value):

        languages = {

            "Vietnamese":"vi",
            "English":"en"

        }


        lang.change(
            languages[value]
        )


        print(
            "[LANG]",
            value
        )


        # reload toàn app

        if hasattr(
            self.app,
            "reload_language"
        ):

            self.app.reload_language()



    def reset_account(self):

        self.app.engine.reset()

        self.app.show_page(
            "Settings"
        )