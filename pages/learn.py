import customtkinter as ctk


class LearnPage(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.app = app

        self.lessons = [

            {
                "title": "Crypto Basics",
                "content":
                    "Blockchain, coins, tokens, wallets and how crypto networks work."
            },

            {
                "title": "Trading Basics",
                "content":
                    "Markets, orders, bid/ask, volume, liquidity and price movement."
            },

            {
                "title": "Technical Analysis",
                "content":
                    "Candles, OHLCV, indicators, support and resistance."
            },

            {
                "title": "Risk Management",
                "content":
                    "Position sizing, stop loss, risk/reward and protecting capital."
            },

            {
                "title": "Paper Trading",
                "content":
                    "Practice strategies safely using Crytopz Paper Trading Engine."
            },

            {
                "title": "Trading Glossary",
                "content":
                    "BTC, ETH, PnL, spread, liquidity, leverage and common terms."
            }

        ]


        self.build_ui()



    def build_ui(self):


        ctk.CTkLabel(
            self,
            text="Learn",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(25,5)
        )


        ctk.CTkLabel(
            self,
            text=
            "Learn crypto, trading and how Crytopz works.",
            text_color="gray"
        ).pack(
            anchor="w",
            padx=30
        )



        self.container = ctk.CTkScrollableFrame(
            self,
            corner_radius=12
        )


        self.container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )


        self.create_lessons()



    def create_lessons(self):


        for lesson in self.lessons:


            card = ctk.CTkFrame(
                self.container,
                corner_radius=14
            )


            card.pack(
                fill="x",
                pady=6
            )


            ctk.CTkLabel(
                card,
                text=lesson["title"],
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=18,
                pady=(12,4)
            )


            ctk.CTkLabel(
                card,
                text=lesson["content"],
                text_color="gray",
                wraplength=800,
                justify="left"
            ).pack(
                anchor="w",
                padx=18,
                pady=(0,12)
            )