import customtkinter as ctk


class HomePage(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(
            parent,
            corner_radius=0
        )

        self.app = app

        self.build_ui()
        self.refresh()


    # =========================================================
    # BUILD UI
    # =========================================================

    def build_ui(self):

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        self.paper_status = ctk.CTkLabel(
            header,
            text="  ● PAPER",
            text_color="#4ade80",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        self.paper_status.pack(
            side="left"
        )


        # -----------------------------------------------------
        # STATS
        # -----------------------------------------------------

        stats = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.equity = self.stat(
            stats,
            "Total Equity",
            "$0.00"
        )

        self.balance = self.stat(
            stats,
            "Cash Balance",
            "$0.00"
        )

        self.pnl = self.stat(
            stats,
            "PnL",
            "$0.00"
        )

        self.position = self.stat(
            stats,
            "Position",
            "0 BTC"
        )


        # -----------------------------------------------------
        # BOT STATUS
        # -----------------------------------------------------

        ctk.CTkLabel(
            self,
            text="Bot Status",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 8)
        )

        bot_card = ctk.CTkFrame(
            self,
            corner_radius=14
        )

        bot_card.pack(
            fill="x",
            padx=25
        )

        bot_left = ctk.CTkFrame(
            bot_card,
            fg_color="transparent"
        )

        bot_left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=18,
            pady=14
        )

        self.bot_name = ctk.CTkLabel(
            bot_left,
            text="No bot",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        self.bot_name.pack(
            anchor="w"
        )

        self.bot_action = ctk.CTkLabel(
            bot_left,
            text="No action",
            text_color="gray"
        )

        self.bot_action.pack(
            anchor="w",
            pady=(3, 0)
        )

        bot_right = ctk.CTkFrame(
            bot_card,
            fg_color="transparent"
        )

        bot_right.pack(
            side="right",
            padx=18
        )

        self.bot_status = ctk.CTkLabel(
            bot_right,
            text="● OFFLINE",
            text_color="#f87171",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        self.bot_status.pack(
            pady=(0, 4)
        )

        self.bot_trades = ctk.CTkLabel(
            bot_right,
            text="0 trades",
            text_color="gray"
        )

        self.bot_trades.pack()

        ctk.CTkButton(
            bot_right,
            text="Open Bot",
            width=110,
            height=30,
            command=lambda:
                self.app.show_page("Bots")
        ).pack(
            pady=(8, 0)
        )


        # -----------------------------------------------------
        # MARKET OVERVIEW
        # -----------------------------------------------------

        ctk.CTkLabel(
            self,
            text="Market Overview",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 8)
        )

        market = ctk.CTkFrame(
            self,
            corner_radius=14
        )

        market.pack(
            fill="x",
            padx=25
        )

        self.market_labels = {}

        for symbol in [
            "BTCUSDT",
            "ETHUSDT",
            "SOLUSDT",
            "BNBUSDT"
        ]:

            row = ctk.CTkFrame(
                market,
                height=52,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=12,
                pady=2
            )

            row.pack_propagate(False)

            ctk.CTkLabel(
                row,
                text=f"{symbol[:3]} / {symbol[3:]}",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=10
            )

            price = ctk.CTkLabel(
                row,
                text="$0.00"
            )

            price.pack(
                side="right",
                padx=20
            )

            self.market_labels[symbol] = price


        # -----------------------------------------------------
        # QUICK ACTIONS
        # -----------------------------------------------------

        actions = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        actions.pack(
            fill="x",
            padx=25,
            pady=25
        )

        ctk.CTkButton(
            actions,
            text="Open Trade",
            width=150,
            height=40,
            command=lambda:
                self.app.show_page("Trade")
        ).pack(
            side="left"
        )

        ctk.CTkButton(
            actions,
            text="View Markets",
            width=150,
            height=40,
            fg_color="transparent",
            border_width=1,
            command=lambda:
                self.app.show_page("Markets")
        ).pack(
            side="left",
            padx=8
        )

        ctk.CTkButton(
            actions,
            text="Bot Dashboard",
            width=150,
            height=40,
            fg_color="transparent",
            border_width=1,
            command=lambda:
                self.app.show_page("Bots")
        ).pack(
            side="left"
        )


    # =========================================================
    # STAT
    # =========================================================

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
                size=19,
                weight="bold"
            )
        )

        label.pack(
            anchor="w",
            padx=15,
            pady=(2, 12)
        )

        return label


    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):

        engine = self.app.engine

        # -----------------------------------------------------
        # ACCOUNT
        # -----------------------------------------------------

        try:

            equity = engine.total_equity()

            self.equity.configure(
                text=f"${equity:,.2f}"
            )

        except Exception:

            self.equity.configure(
                text="$0.00"
            )


        try:

            self.balance.configure(
                text=f"${engine.cash:,.2f}"
            )

        except Exception:

            self.balance.configure(
                text="$0.00"
            )


        try:

            pnl = engine.pnl()

            self.pnl.configure(
                text=f"${pnl:,.2f}",
                text_color=(
                    "#4ade80"
                    if pnl >= 0
                    else "#f87171"
                )
            )

        except Exception:

            self.pnl.configure(
                text="$0.00"
            )


        # -----------------------------------------------------
        # POSITION
        # -----------------------------------------------------

        try:

            position = engine.positions.get(
                "BTCUSDT"
            )

            if position:

                self.position.configure(
                    text=f"{position.quantity:g} BTC"
                )

            else:

                self.position.configure(
                    text="0 BTC"
                )

        except Exception:

            self.position.configure(
                text="0 BTC"
            )


        # -----------------------------------------------------
        # MARKET
        # -----------------------------------------------------

        for symbol, label in self.market_labels.items():

            try:

                price = engine.get_price(
                    symbol
                )

                label.configure(
                    text=f"${price:,.2f}"
                )

            except Exception:

                label.configure(
                    text="--"
                )


        # -----------------------------------------------------
        # BOT
        # -----------------------------------------------------

        self.refresh_bot()


    # =========================================================
    # BOT SUMMARY
    # =========================================================

    def refresh_bot(self):

        manager = self.app.bot_manager

        if manager is None:

            self.bot_name.configure(
                text="Bot System unavailable"
            )

            self.bot_status.configure(
                text="● OFFLINE",
                text_color="#f87171"
            )

            self.bot_trades.configure(
                text="0 trades"
            )

            self.bot_action.configure(
                text="Bot Manager unavailable"
            )

            return


        try:

            bots = manager.list_bots()

        except Exception:

            bots = []


        if not bots:

            self.bot_name.configure(
                text="No bots installed"
            )

            self.bot_status.configure(
                text="● OFFLINE",
                text_color="#f87171"
            )

            self.bot_trades.configure(
                text="0 trades"
            )

            self.bot_action.configure(
                text="Install or create a bot."
            )

            return


        # Find first running bot.
        selected = None

        for bot in bots:

            if manager.is_running(
                bot["id"]
            ):

                selected = bot
                break


        if selected is None:

            selected = bots[0]


        bot_id = selected["id"]

        bot_name = selected["name"]


        self.bot_name.configure(
            text=bot_name
        )


        running = manager.is_running(
            bot_id
        )


        if running:

            self.bot_status.configure(
                text="● RUNNING",
                text_color="#4ade80"
            )

        else:

            self.bot_status.configure(
                text="● STOPPED",
                text_color="#f87171"
            )


        # -----------------------------------------------------
        # BOT INSTANCE STATE
        # -----------------------------------------------------

        instance = manager.get_instance(
            bot_id
        )


        trades = 0
        action = "No action"


        if instance is not None:

            try:

                state = instance.state()

                if isinstance(state, dict):

                    trades = state.get(
                        "trades",
                        0
                    )

                    action = state.get(
                        "last_action",
                        "No action"
                    )

                else:

                    trades = getattr(
                        state,
                        "trades",
                        0
                    )

                    action = getattr(
                        state,
                        "last_action",
                        "No action"
                    )

            except Exception:

                trades = getattr(
                    instance,
                    "trades",
                    0
                )

                action = getattr(
                    instance,
                    "last_action",
                    "No action"
                )


        self.bot_trades.configure(
            text=f"{trades} trades"
        )

        self.bot_action.configure(
            text=action or "No action"
        )