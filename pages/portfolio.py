import customtkinter as ctk


class PortfolioPage(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.app = app

        self.build_ui()

        self.refresh()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Portfolio",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 15)
        )

        stats = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            padx=25
        )

        self.equity = self.stat(
            stats,
            "Total Equity",
            "$0.00"
        )

        self.cash = self.stat(
            stats,
            "Cash",
            "$0.00"
        )

        self.assets = self.stat(
            stats,
            "Assets",
            "$0.00"
        )

        self.pnl = self.stat(
            stats,
            "Total PnL",
            "$0.00"
        )

        self.realized = self.stat(
            stats,
            "Realized",
            "$0.00"
        )

        ctk.CTkLabel(
            self,
            text="Open Positions",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 8)
        )

        self.position_box = ctk.CTkScrollableFrame(
            self,
            corner_radius=14
        )

        self.position_box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

    # =====================================================
    # STAT
    # =====================================================

    def stat(
        self,
        parent,
        title,
        value
    ):

        box = ctk.CTkFrame(
            parent,
            corner_radius=12
        )

        box.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            box,
            text=title,
            text_color="gray"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 0)
        )

        label = ctk.CTkLabel(
            box,
            text=value,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        label.pack(
            anchor="w",
            padx=15,
            pady=(3, 12)
        )

        return label

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        engine = getattr(
            self.app,
            "engine",
            None
        )

        if engine is None:
            return

        account = engine.account()

        # -------------------------------------------------
        # STATS
        # -------------------------------------------------

        self.equity.configure(
            text=f"${account['equity']:,.2f}"
        )

        self.cash.configure(
            text=f"${account['cash']:,.2f}"
        )

        self.assets.configure(
            text=f"${account['position_value']:,.2f}"
        )

        pnl = account["pnl"]

        self.pnl.configure(
            text=f"${pnl:,.2f}",
            text_color=(
                "#4ade80"
                if pnl >= 0
                else "#f87171"
            )
        )

        realized = account[
            "realized_pnl"
        ]

        self.realized.configure(
            text=f"${realized:,.2f}",
            text_color=(
                "#4ade80"
                if realized >= 0
                else "#f87171"
            )
        )

        # -------------------------------------------------
        # CLEAR
        # -------------------------------------------------

        for widget in (
            self.position_box.winfo_children()
        ):

            widget.destroy()

        # -------------------------------------------------
        # POSITIONS
        # -------------------------------------------------

        positions = engine.positions()

        if not positions:

            ctk.CTkLabel(
                self.position_box,
                text="No open positions",
                text_color="gray"
            ).pack(
                pady=25
            )

            return

        # -------------------------------------------------
        # POSITION CARDS
        # -------------------------------------------------

        for position in positions:

            symbol = position[
                "symbol"
            ]

            quantity = position[
                "quantity"
            ]

            average_price = position[
                "average_price"
            ]

            current_price = (
                engine.get_price(
                    symbol
                )
            )

            value = (
                quantity
                * current_price
            )

            unrealized = (
                current_price
                - average_price
            ) * quantity

            card = ctk.CTkFrame(
                self.position_box,
                corner_radius=12
            )

            card.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=symbol,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=(10, 2)
            )

            ctk.CTkLabel(
                card,
                text=(
                    f"Quantity: "
                    f"{quantity:g}\n"
                    f"Average: "
                    f"${average_price:,.2f}\n"
                    f"Current: "
                    f"${current_price:,.2f}\n"
                    f"Value: "
                    f"${value:,.2f}"
                ),
                text_color="gray"
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 10)
            )

            ctk.CTkLabel(
                card,
                text=(
                    f"Unrealized PnL: "
                    f"${unrealized:,.2f}"
                ),
                text_color=(
                    "#4ade80"
                    if unrealized >= 0
                    else "#f87171"
                )
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 10)
            )