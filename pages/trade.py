from __future__ import annotations

import json
import math
import time
from pathlib import Path

import tkinter as tk
import customtkinter as ctk


class TradePage(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color="transparent",
        )

        self.app = app
        self.symbol = "BTCUSDT"
        self.side = "BUY"

        self.refresh_interval = 33
        self.refresh_job = None
        self.clock_job = None
        self.destroyed = False

        # ============================================================
        # CANDLE DATA
        # ============================================================

        self.candles = []
        self.candle_ticks = 0
        self.candle_interval = 8
        self.max_candles = 300
        self.visible_candles = 80
        self.last_price = None

        # ============================================================
        # CANDLE ANIMATION
        # ============================================================

        self.candle_animation_job = None
        self.candle_animation_progress = 1.0
        self.candle_animation_from = None
        self.candle_animation_to = None

        # ============================================================
        # HISTORY / PAN
        # ============================================================

        self.history_position = 1.0
        self.history_target = 1.0

        self.history_animation_job = None
        self.history_animation_start = 1.0
        self.history_animation_target = 1.0
        self.history_animation_clock = 0.0
        self.history_animation_duration = 240

        self.chart_pan_active = False
        self.chart_pan_start_x = None
        self.chart_pan_start_position = 1.0

        # ============================================================
        # HOVER
        # ============================================================

        self.chart_hover = False
        self.hover_x = None
        self.hover_y = None

        # ============================================================
        # DRAWING
        # ============================================================

        self.drawing_mode = "cursor"
        self.drawings = []
        self.active_drawing = None

        self.drag_start_x = None
        self.drag_start_y = None

        # ============================================================
        # ANALYSIS
        # ============================================================

        self.analysis_period = "1H"

        # ============================================================
        # CACHE
        # ============================================================

        self.chart_cache_dir = (
            Path.home()
            / ".crytopz"
            / "chart_cache"
        )

        try:
            self.chart_cache_dir.mkdir(
                parents=True,
                exist_ok=True,
            )
        except Exception:
            pass

        # ============================================================
        # STATE
        # ============================================================

        self.last_order_count = -1
        self.theme_mode = None

        self.chart_width = 0
        self.chart_height = 0
        self.chart_dirty = True

        self.update_theme_colors()
        self.build_ui()

        self.update_idletasks()

        self.load_chart_cache()

        self.refresh()
        self.start_auto_refresh()
        self.start_clock()

    # ================================================================
    # THEME
    # ================================================================

    def update_theme_colors(self):
        mode = ctk.get_appearance_mode().lower()
        self.theme_mode = mode

        if mode == "light":
            self.bg = "#f4f5f7"
            self.card = "#ffffff"
            self.card_2 = "#f8f9fb"
            self.chart_bg = "#ffffff"
            self.border = "#dfe2e7"
            self.grid_color = "#eceef2"
            self.text = "#17181c"
            self.muted = "#747780"

            self.green = "#16a34a"
            self.green_hover = "#15803d"

            self.red = "#dc2626"
            self.red_hover = "#b91c1c"

            self.blue = "#2563eb"
            self.blue_hover = "#1d4ed8"

        else:
            self.bg = "#0b0b0d"
            self.card = "#111114"
            self.card_2 = "#151519"
            self.chart_bg = "#0d0d10"
            self.border = "#202027"
            self.grid_color = "#1b1b21"
            self.text = "#f4f4f5"
            self.muted = "#77777f"

            self.green = "#22c55e"
            self.green_hover = "#16a34a"

            self.red = "#ef4444"
            self.red_hover = "#dc2626"

            self.blue = "#2563eb"
            self.blue_hover = "#1d4ed8"

    def theme_changed(self):
        self.update_theme_colors()

        try:
            self.configure(
                fg_color=self.bg
            )
        except Exception:
            pass

        self.chart_dirty = True

        try:
            self.refresh()
        except Exception:
            pass

    # ================================================================
    # UI
    # ================================================================

    def build_ui(self):
        self.configure(
            fg_color=self.bg
        )

        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
            height=38,
        )
        header.pack(
            fill="x",
            padx=12,
            pady=(6, 2),
        )
        header.pack_propagate(False)

        title_row = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )
        title_row.pack(
            side="left",
            fill="y",
        )

        ctk.CTkLabel(
            title_row,
            text="Trade",
            text_color=self.text,
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        ).pack(side="left")

        self.live_label = ctk.CTkLabel(
            title_row,
            text="● LIVE",
            text_color=self.green,
            font=ctk.CTkFont(
                size=9,
                weight="bold",
            ),
        )
        self.live_label.pack(
            side="left",
            padx=(10, 5),
        )

        self.market_interval_label = ctk.CTkLabel(
            title_row,
            text="Core: --",
            text_color=self.muted,
            font=ctk.CTkFont(size=9),
        )
        self.market_interval_label.pack(
            side="left"
        )

        main = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        main.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 8),
        )

        main.grid_columnconfigure(
            0,
            weight=1,
        )
        main.grid_columnconfigure(
            1,
            weight=0,
            minsize=285,
        )
        main.grid_rowconfigure(
            0,
            weight=1,
        )

        market_container = ctk.CTkFrame(
            main,
            fg_color="transparent",
        )
        market_container.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5),
        )

        order_container = ctk.CTkFrame(
            main,
            fg_color="transparent",
            width=285,
        )
        order_container.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(5, 0),
        )
        order_container.grid_propagate(False)

        self.build_market(
            market_container
        )

        self.build_order_panel(
            order_container
        )

    def create_accent_card(
        self,
        parent,
        accent=True,
        corner_radius=10,
    ):
        outer = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        card = ctk.CTkFrame(
            outer,
            fg_color=self.card,
            corner_radius=corner_radius,
            border_width=1,
            border_color=self.border,
        )

        card.pack(
            fill="both",
            expand=True,
            padx=(4 if accent else 0, 0),
        )

        if accent:
            bar = ctk.CTkFrame(
                outer,
                width=4,
                fg_color=self.blue,
                corner_radius=3,
            )

            bar.place(
                relx=0,
                rely=0.18,
                relheight=0.64,
                anchor="nw",
            )

        return outer, card

    # ================================================================
    # MARKET
    # ================================================================

    def build_market(self, parent):
        parent.grid_rowconfigure(
            0,
            weight=1,
        )
        parent.grid_columnconfigure(
            0,
            weight=1,
        )

        market_outer, market = self.create_accent_card(
            parent,
            accent=True,
            corner_radius=11,
        )

        market_outer.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self._market_card_reference = market

        for row in range(7):
            market.grid_rowconfigure(
                row,
                weight=0,
            )

        market.grid_rowconfigure(
            2,
            weight=1,
        )

        market.grid_columnconfigure(
            0,
            weight=1,
        )

        # ------------------------------------------------------------
        # TOP
        # ------------------------------------------------------------

        top = ctk.CTkFrame(
            market,
            fg_color="transparent",
            height=38,
        )
        top.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=12,
            pady=(6, 0),
        )
        top.grid_propagate(False)

        self.symbol_label = ctk.CTkLabel(
            top,
            text="BTC / USDT",
            text_color=self.text,
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
        )
        self.symbol_label.pack(
            side="left"
        )

        self.price_label = ctk.CTkLabel(
            top,
            text="$0.00",
            text_color=self.text,
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
        )
        self.price_label.pack(
            side="left",
            padx=(13, 7),
        )

        self.price_change_label = ctk.CTkLabel(
            top,
            text="0.000%",
            text_color=self.muted,
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
        )
        self.price_change_label.pack(
            side="left"
        )

        self.chart_clock_label = ctk.CTkLabel(
            top,
            text="00:00:00",
            text_color=self.muted,
            font=ctk.CTkFont(
                size=8,
            ),
        )
        self.chart_clock_label.pack(
            side="right",
            padx=(8, 0),
        )

        ctk.CTkLabel(
            top,
            text="PAPER",
            text_color=self.green,
            font=ctk.CTkFont(
                size=8,
                weight="bold",
            ),
        ).pack(
            side="right"
        )

        # ------------------------------------------------------------
        # TOOLBAR
        # ------------------------------------------------------------

        toolbar = ctk.CTkFrame(
            market,
            fg_color="transparent",
            height=31,
        )

        toolbar.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 2),
        )
        toolbar.grid_propagate(False)

        self.selected_timeframe = "1m"
        self.timeframe_buttons = {}

        for tf in (
            "1m",
            "5m",
            "15m",
            "1H",
            "4H",
            "1D",
        ):
            button = ctk.CTkButton(
                toolbar,
                text=tf,
                width=39,
                height=23,
                corner_radius=5,
                fg_color=(
                    self.blue
                    if tf == "1m"
                    else "transparent"
                ),
                hover_color=self.blue_hover,
                text_color=self.text,
                font=ctk.CTkFont(
                    size=9,
                    weight="bold",
                ),
                command=lambda value=tf:
                    self.change_timeframe(value),
            )

            button.pack(
                side="left",
                padx=1,
            )

            self.timeframe_buttons[tf] = button

        ctk.CTkFrame(
            toolbar,
            width=1,
            height=17,
            fg_color=self.border,
        ).pack(
            side="left",
            padx=7,
        )

        self.draw_buttons = {}

        for tool, icon in (
            ("cursor", "↖"),
            ("line", "╱"),
            ("horizontal", "━"),
            ("rectangle", "□"),
        ):
            button = ctk.CTkButton(
                toolbar,
                text=icon,
                width=27,
                height=23,
                corner_radius=5,
                fg_color=(
                    self.blue
                    if tool == "cursor"
                    else "transparent"
                ),
                hover_color=self.blue_hover,
                text_color=self.text,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold",
                ),
                command=lambda value=tool:
                    self.set_drawing_mode(value),
            )

            button.pack(
                side="left",
                padx=1,
            )

            self.draw_buttons[tool] = button

        ctk.CTkButton(
            toolbar,
            text="×",
            width=27,
            height=23,
            corner_radius=5,
            fg_color="transparent",
            hover_color=self.red_hover,
            text_color=self.text,
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
            command=self.clear_drawings,
        ).pack(
            side="left",
            padx=(5, 1),
        )

        # ------------------------------------------------------------
        # CHART
        # ------------------------------------------------------------

        chart_outer = ctk.CTkFrame(
            market,
            fg_color="transparent",
        )

        chart_outer.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(0, 3),
        )

        chart_outer.grid_rowconfigure(
            0,
            weight=1,
        )

        chart_outer.grid_columnconfigure(
            0,
            weight=1,
        )

        chart_card = ctk.CTkFrame(
            chart_outer,
            fg_color=self.chart_bg,
            corner_radius=9,
            border_width=1,
            border_color=self.border,
        )

        chart_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(3, 0),
        )

        self.chart = tk.Canvas(
            chart_card,
            background=self.chart_bg,
            highlightthickness=0,
            bd=0,
        )

        self.chart.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1,
        )

        self.chart.bind(
            "<Configure>",
            self.on_chart_resize,
        )

        self.chart.bind(
            "<ButtonPress-1>",
            self.on_chart_mouse_down,
        )

        self.chart.bind(
            "<B1-Motion>",
            self.on_chart_mouse_drag,
        )

        self.chart.bind(
            "<ButtonRelease-1>",
            self.on_chart_mouse_up,
        )

        self.chart.bind(
            "<Motion>",
            self.on_chart_motion,
        )

        self.chart.bind(
            "<Leave>",
            self.on_chart_leave,
        )

        ctk.CTkFrame(
            chart_outer,
            width=3,
            fg_color=self.blue,
            corner_radius=3,
        ).place(
            relx=0,
            rely=0.12,
            relheight=0.76,
            anchor="nw",
        )

        # ------------------------------------------------------------
        # ANALYSIS
        # ------------------------------------------------------------

        analysis = ctk.CTkFrame(
            market,
            fg_color=self.card_2,
            corner_radius=8,
            height=39,
        )

        analysis.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 4),
        )

        analysis.grid_propagate(False)

        ctk.CTkLabel(
            analysis,
            text="Analysis",
            text_color=self.text,
            font=ctk.CTkFont(
                size=9,
                weight="bold",
            ),
        ).pack(
            side="left",
            padx=(8, 5),
        )

        self.analysis_buttons = {}

        for period in (
            "15m",
            "1H",
            "4H",
            "1D",
            "7D",
        ):
            button = ctk.CTkButton(
                analysis,
                text=period,
                width=38,
                height=23,
                corner_radius=6,
                fg_color=(
                    self.blue
                    if period == self.analysis_period
                    else "transparent"
                ),
                hover_color=self.blue_hover,
                text_color=self.text,
                font=ctk.CTkFont(size=8),
                command=lambda p=period:
                    self.set_analysis_period(p),
            )

            button.pack(
                side="left",
                padx=1,
            )

            self.analysis_buttons[
                period
            ] = button

        self.analysis_label = ctk.CTkLabel(
            analysis,
            text="Analysis ready",
            text_color=self.muted,
            font=ctk.CTkFont(size=8),
        )

        self.analysis_label.pack(
            side="right",
            padx=8,
        )

        # ------------------------------------------------------------
        # HISTORY SLIDER
        # ------------------------------------------------------------

        history_slider_frame = ctk.CTkFrame(
            market,
            fg_color="transparent",
            height=25,
        )

        history_slider_frame.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 2),
        )

        history_slider_frame.grid_propagate(False)

        ctk.CTkLabel(
            history_slider_frame,
            text="History",
            text_color=self.muted,
            font=ctk.CTkFont(size=8),
        ).pack(
            side="left",
            padx=(0, 6),
        )

        self.history_slider = ctk.CTkSlider(
            history_slider_frame,
            from_=0,
            to=1,
            number_of_steps=1000,
            height=14,
            command=self.on_history_slider,
        )

        self.history_slider.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.history_slider.set(1)

        self.history_label = ctk.CTkLabel(
            history_slider_frame,
            text="LIVE",
            text_color=self.green,
            width=48,
            font=ctk.CTkFont(
                size=8,
                weight="bold",
            ),
        )

        self.history_label.pack(
            side="right",
            padx=(6, 0),
        )

        # ------------------------------------------------------------
        # RECENT ORDERS
        # ------------------------------------------------------------

        history_outer, history = self.create_accent_card(
            market,
            accent=True,
            corner_radius=9,
        )

        history_outer.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 5),
        )

        history.configure(
            height=88
        )

        history.grid_rowconfigure(
            1,
            weight=1,
        )

        history.grid_columnconfigure(
            0,
            weight=1,
        )

        history_header = ctk.CTkFrame(
            history,
            fg_color="transparent",
            height=23,
        )

        history_header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=(3, 0),
        )

        history_header.grid_propagate(False)

        ctk.CTkLabel(
            history_header,
            text="Recent Orders",
            text_color=self.text,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        ).pack(
            side="left"
        )

        self.order_count_label = ctk.CTkLabel(
            history_header,
            text="0 orders",
            text_color=self.muted,
            font=ctk.CTkFont(size=9),
        )

        self.order_count_label.pack(
            side="right"
        )

        self.orders_text = ctk.CTkTextbox(
            history,
            height=55,
            activate_scrollbars=False,
            font=ctk.CTkFont(size=9),
            fg_color=self.chart_bg,
            border_width=0,
            text_color=self.text,
        )

        self.orders_text.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=6,
            pady=(0, 5),
        )

        self.orders_text.configure(
            state="disabled"
        )

        # ------------------------------------------------------------
        # ACCOUNT
        # ------------------------------------------------------------

        self.build_account_section(
            market
        )

    # ================================================================
    # ORDER PANEL
    # ================================================================

    def build_order_panel(self, parent):
        outer, panel = self.create_accent_card(
            parent,
            accent=True,
            corner_radius=11,
        )

        outer.pack(
            fill="both",
            expand=True,
        )

        title = ctk.CTkFrame(
            panel,
            fg_color="transparent",
            height=35,
        )

        title.pack(
            fill="x",
            padx=14,
            pady=(6, 0),
        )

        title.pack_propagate(False)

        ctk.CTkLabel(
            title,
            text="Order",
            text_color=self.text,
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
        ).pack(
            side="left"
        )

        side_frame = ctk.CTkFrame(
            panel,
            fg_color="transparent",
        )

        side_frame.pack(
            fill="x",
            padx=13,
            pady=(0, 4),
        )

        self.buy_button = ctk.CTkButton(
            side_frame,
            text="BUY",
            height=32,
            corner_radius=6,
            command=lambda:
                self.set_side("BUY"),
        )

        self.buy_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 2),
        )

        self.sell_button = ctk.CTkButton(
            side_frame,
            text="SELL",
            height=32,
            corner_radius=6,
            command=lambda:
                self.set_side("SELL"),
        )

        self.sell_button.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(2, 0),
        )

        self.add_label(
            panel,
            "Asset",
        )

        symbols = getattr(
            self.app.engine,
            "supported_symbols",
            [
                "BTCUSDT",
                "ETHUSDT",
                "SOLUSDT",
                "BNBUSDT",
                "XRPUSDT",
                "ADAUSDT",
            ],
        )

        self.symbol_menu = ctk.CTkOptionMenu(
            panel,
            values=symbols,
            height=30,
            corner_radius=6,
            command=self.change_symbol,
        )

        self.symbol_menu.set(
            self.symbol
        )

        self.symbol_menu.pack(
            fill="x",
            padx=14,
        )

        self.add_label(
            panel,
            "Order Type",
        )

        self.order_type = ctk.CTkOptionMenu(
            panel,
            values=[
                "Market",
                "Limit",
            ],
            height=30,
            corner_radius=6,
            command=self.change_order_type,
        )

        self.order_type.set(
            "Market"
        )

        self.order_type.pack(
            fill="x",
            padx=14,
        )

        self.add_label(
            panel,
            "Quantity",
        )

        self.quantity = ctk.CTkEntry(
            panel,
            height=30,
            corner_radius=6,
            placeholder_text="0.001",
        )

        self.quantity.pack(
            fill="x",
            padx=14,
        )

        self.quantity.bind(
            "<KeyRelease>",
            lambda _event:
                self.update_cost(),
        )

        quick = ctk.CTkFrame(
            panel,
            fg_color="transparent",
        )

        quick.pack(
            fill="x",
            padx=12,
            pady=(4, 0),
        )

        for amount in (
            10,
            50,
            100,
            500,
        ):
            ctk.CTkButton(
                quick,
                text=f"${amount}",
                width=43,
                height=24,
                corner_radius=5,
                font=ctk.CTkFont(size=8),
                command=lambda value=amount:
                    self.set_quick_amount(value),
            ).pack(
                side="left",
                padx=1,
            )

        ctk.CTkButton(
            quick,
            text="MAX",
            width=43,
            height=24,
            corner_radius=5,
            font=ctk.CTkFont(
                size=8,
                weight="bold",
            ),
            command=self.set_max_amount,
        ).pack(
            side="left",
            padx=1,
        )

        self.limit_label = ctk.CTkLabel(
            panel,
            text="Limit Price",
            text_color=self.muted,
            font=ctk.CTkFont(size=9),
        )

        self.limit_label.pack(
            anchor="w",
            padx=14,
            pady=(5, 2),
        )

        self.limit_price = ctk.CTkEntry(
            panel,
            height=30,
            corner_radius=6,
            placeholder_text="Only for Limit",
        )

        self.limit_price.pack(
            fill="x",
            padx=14,
        )

        self.limit_price.configure(
            state="disabled"
        )

        self.cost_label = ctk.CTkLabel(
            panel,
            text="Estimated: $0.00",
            text_color=self.muted,
            wraplength=230,
            justify="left",
            font=ctk.CTkFont(size=9),
        )

        self.cost_label.pack(
            anchor="w",
            padx=14,
            pady=(5, 4),
        )

        self.execute_button = ctk.CTkButton(
            panel,
            text="BUY BTC",
            height=37,
            corner_radius=6,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            command=self.execute,
        )

        self.execute_button.pack(
            fill="x",
            padx=14,
        )

        self.status = ctk.CTkLabel(
            panel,
            text="Ready",
            text_color=self.muted,
            wraplength=230,
            justify="left",
            font=ctk.CTkFont(size=9),
        )

        self.status.pack(
            padx=14,
            pady=5,
        )

        ctk.CTkButton(
            panel,
            text="Reset Paper Account",
            height=25,
            corner_radius=5,
            fg_color="transparent",
            border_width=1,
            border_color=self.border,
            font=ctk.CTkFont(size=8),
            command=self.reset_account,
        ).pack(
            fill="x",
            padx=14,
            pady=(0, 7),
        )

        self.set_side(
            "BUY"
        )

    # ================================================================
    # HELPERS
    # ================================================================

    def engine(self):
        return self.app.engine

    def add_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            text_color=self.muted,
            font=ctk.CTkFont(size=9),
        ).pack(
            anchor="w",
            padx=14,
            pady=(4, 2),
        )

    def show_error(self, message):
        self.status.configure(
            text=str(message),
            text_color=self.red,
        )

    # ================================================================
    # SIDE / SYMBOL / TIMEFRAME
    # ================================================================

    def set_side(self, side):
        side = str(side).upper()

        if side not in (
            "BUY",
            "SELL",
        ):
            return

        self.side = side

        if side == "BUY":
            self.buy_button.configure(
                fg_color=self.green_hover,
                hover_color="#15803d",
            )

            self.sell_button.configure(
                fg_color=self.border,
                hover_color=self.card_2,
            )

        else:
            self.sell_button.configure(
                fg_color=self.red_hover,
                hover_color="#b91c1c",
            )

            self.buy_button.configure(
                fg_color=self.border,
                hover_color=self.card_2,
            )

        self.update_execute_button()
        self.update_cost()

    def change_symbol(self, symbol):
        self.symbol = str(
            symbol
        ).strip().upper()

        if self.symbol.endswith(
            "USDT"
        ):
            self.symbol_label.configure(
                text=(
                    f"{self.symbol[:-4]} / USDT"
                )
            )
        else:
            self.symbol_label.configure(
                text=self.symbol
            )

        self.reset_chart_state()
        self.load_chart_cache()
        self.refresh()

    def change_timeframe(self, timeframe):
        self.selected_timeframe = timeframe

        intervals = {
            "1m": 8,
            "5m": 15,
            "15m": 25,
            "1H": 40,
            "4H": 55,
            "1D": 70,
        }

        self.candle_interval = intervals.get(
            timeframe,
            8,
        )

        for name, button in (
            self.timeframe_buttons.items()
        ):
            button.configure(
                fg_color=(
                    self.blue
                    if name == timeframe
                    else "transparent"
                )
            )

        self.reset_chart_state()
        self.load_chart_cache()

        self.status.configure(
            text=f"Timeframe: {timeframe}",
            text_color=self.muted,
        )

        self.refresh()

    def change_order_type(self, order_type):
        if order_type == "Limit":
            self.limit_price.configure(
                state="normal"
            )

            self.execute_button.configure(
                state="disabled"
            )

            self.status.configure(
                text=(
                    "Limit orders are not "
                    "available yet."
                ),
                text_color="#fbbf24",
            )

        else:
            self.limit_price.delete(
                0,
                "end",
            )

            self.limit_price.configure(
                state="disabled"
            )

            self.execute_button.configure(
                state="normal"
            )

            self.status.configure(
                text="Ready",
                text_color=self.muted,
            )

        self.update_cost()

    # ================================================================
    # ORDER HELPERS
    # ================================================================

    def current_price(self):
        try:
            return float(
                self.engine().get_price(
                    self.symbol
                )
            )
        except Exception:
            return 0.0

    def set_quick_amount(self, amount):
        price = self.current_price()

        if price <= 0:
            self.show_error(
                "Invalid market price."
            )
            return

        engine = self.engine()

        if self.side == "BUY":
            fee_rate = float(
                getattr(
                    engine,
                    "fee_rate",
                    0.0,
                )
            )

            quantity = (
                float(amount)
                / (
                    price
                    * (
                        1.0
                        + fee_rate
                    )
                )
            )

        else:
            position = engine.position(
                self.symbol
            )

            available = max(
                0.0,
                float(
                    position.get(
                        "quantity",
                        0.0,
                    )
                ),
            )

            if available <= 0:
                self.show_error(
                    "No position to sell."
                )
                return

            quantity = min(
                float(amount) / price,
                available,
            )

        self.set_quantity(
            quantity
        )

    def set_max_amount(self):
        price = self.current_price()

        if price <= 0:
            self.show_error(
                "Invalid market price."
            )
            return

        engine = self.engine()

        if self.side == "BUY":
            fee_rate = float(
                getattr(
                    engine,
                    "fee_rate",
                    0.0,
                )
            )

            cash = max(
                0.0,
                float(
                    getattr(
                        engine,
                        "cash",
                        0.0,
                    )
                ),
            )

            quantity = (
                cash
                / (
                    price
                    * (
                        1.0
                        + fee_rate
                    )
                )
            )

        else:
            position = engine.position(
                self.symbol
            )

            quantity = max(
                0.0,
                float(
                    position.get(
                        "quantity",
                        0.0,
                    )
                ),
            )

        self.set_quantity(
            quantity
        )

    def set_quantity(self, quantity):
        self.quantity.delete(
            0,
            "end",
        )

        self.quantity.insert(
            0,
            f"{quantity:.8f}",
        )

        self.update_cost()

    def update_cost(self):
        try:
            quantity = float(
                self.quantity.get()
            )
        except (
            ValueError,
            TypeError,
        ):
            quantity = 0.0

        price = self.current_price()

        if quantity <= 0 or price <= 0:
            self.cost_label.configure(
                text="Estimated: $0.00"
            )
            return

        value = quantity * price

        fee_rate = float(
            getattr(
                self.engine(),
                "fee_rate",
                0.0,
            )
        )

        fee = value * fee_rate

        if self.side == "BUY":
            self.cost_label.configure(
                text=(
                    f"Value  ${value:,.2f}\n"
                    f"Fee    ${fee:,.2f}   |   "
                    f"Total  ${value + fee:,.2f}"
                )
            )

        else:
            self.cost_label.configure(
                text=(
                    f"Value  ${value:,.2f}\n"
                    f"Fee    ${fee:,.2f}   |   "
                    f"Receive  ${value - fee:,.2f}"
                )
            )

    def execute(self):
        if self.order_type.get() != "Market":
            self.show_error(
                "Limit orders are not available yet."
            )
            return

        try:
            quantity = float(
                self.quantity.get()
            )
        except (
            ValueError,
            TypeError,
        ):
            self.show_error(
                "Invalid quantity."
            )
            return

        if quantity <= 0:
            self.show_error(
                "Quantity must be greater than 0."
            )
            return

        engine = self.engine()

        try:
            if self.side == "BUY":
                order_id = engine.buy(
                    self.symbol,
                    quantity,
                )
            else:
                order_id = engine.sell(
                    self.symbol,
                    quantity,
                )

        except Exception as error:
            self.show_error(
                str(error)
            )
            return

        self.status.configure(
            text=(
                f"{self.side} FILLED  |  "
                f"{quantity:g} {self.symbol}  |  "
                f"Order #{order_id}"
            ),
            text_color=self.green,
        )

        self.quantity.delete(
            0,
            "end",
        )

        self.refresh()
        self.refresh_other_pages()

    def reset_account(self):
        try:
            self.engine().reset()

        except Exception as error:
            self.show_error(
                f"Reset failed: {error}"
            )
            return

        self.reset_chart_state()

        self.last_order_count = -1

        self.status.configure(
            text="Paper account reset.",
            text_color=self.green,
        )

        self.quantity.delete(
            0,
            "end",
        )

        self.refresh()
        self.refresh_other_pages()

    def refresh_other_pages(self):
        pages = getattr(
            self.app,
            "pages",
            {},
        )

        for name in (
            "Home",
            "Portfolio",
            "Markets",
            "Order History",
        ):
            page = pages.get(name)

            if page is None:
                continue

            refresh = getattr(
                page,
                "refresh",
                None,
            )

            if callable(refresh):
                try:
                    refresh()
                except Exception:
                    pass

    # ================================================================
    # CHART STATE
    # ================================================================

    def reset_chart_state(self):
        self.candles.clear()

        self.candle_ticks = 0
        self.last_price = None

        self.history_position = 1.0
        self.history_target = 1.0

        if self.history_animation_job:
            try:
                self.after_cancel(
                    self.history_animation_job
                )
            except Exception:
                pass

        self.history_animation_job = None

        if self.candle_animation_job:
            try:
                self.after_cancel(
                    self.candle_animation_job
                )
            except Exception:
                pass

        self.candle_animation_job = None

        self.candle_animation_progress = 1.0
        self.candle_animation_from = None
        self.candle_animation_to = None

        self.chart_pan_active = False
        self.chart_pan_start_x = None

        self.drawings.clear()
        self.active_drawing = None

        self.chart_dirty = True

        try:
            self.history_slider.set(
                1
            )

            self.history_label.configure(
                text="LIVE",
                text_color=self.green,
            )

        except Exception:
            pass

    # ================================================================
    # CANDLES
    # ================================================================

    def update_candles(self, price):
        if price <= 0:
            return

        if self.last_price is None:
            self.last_price = price

            self.candles.append(
                {
                    "open": price,
                    "high": price,
                    "low": price,
                    "close": price,
                    "timestamp": time.time(),
                }
            )

            self.chart_dirty = True
            return

        if not self.candles:
            self.candles.append(
                {
                    "open": self.last_price,
                    "high": price,
                    "low": price,
                    "close": price,
                    "timestamp": time.time(),
                }
            )

            self.candle_ticks = 1
            self.last_price = price
            self.chart_dirty = True
            return

        candle = self.candles[-1]

        old_close = float(
            candle["close"]
        )

        candle["high"] = max(
            float(candle["high"]),
            price,
        )

        candle["low"] = min(
            float(candle["low"]),
            price,
        )

        candle["close"] = price

        self.start_candle_animation(
            old_close,
            price,
        )

        self.candle_ticks += 1
        self.last_price = price

        if self.candle_ticks >= self.candle_interval:
            self.candles.append(
                {
                    "open": price,
                    "high": price,
                    "low": price,
                    "close": price,
                    "timestamp": time.time(),
                }
            )

            self.candle_ticks = 0

        if len(self.candles) > self.max_candles:
            self.candles = self.candles[
                -self.max_candles:
            ]

        if old_close != price:
            self.chart_dirty = True

    # ================================================================
    # CANDLE ANIMATION
    # ================================================================

    def start_candle_animation(
        self,
        old_price,
        new_price,
    ):
        if old_price is None:
            return

        if abs(
            old_price - new_price
        ) < 0.000001:
            return

        if self.candle_animation_job:
            try:
                self.after_cancel(
                    self.candle_animation_job
                )
            except Exception:
                pass

        self.candle_animation_from = old_price
        self.candle_animation_to = new_price
        self.candle_animation_progress = 0.0

        self.candle_animation_job = self.after(
            12,
            self._animate_candle,
        )

    def get_animated_close(
        self,
        actual_close,
    ):
        if (
            self.candle_animation_from is None
            or self.candle_animation_to is None
            or self.candle_animation_progress >= 1.0
        ):
            return actual_close

        p = self.candle_animation_progress

        eased = (
            1.0
            - (1.0 - p) ** 3
        )

        return (
            self.candle_animation_from
            + (
                self.candle_animation_to
                - self.candle_animation_from
            )
            * eased
        )

    def _animate_candle(self):
        if self.destroyed:
            self.candle_animation_job = None
            return

        self.candle_animation_progress += 0.08

        if self.candle_animation_progress >= 1.0:
            self.candle_animation_progress = 1.0

            self.candle_animation_job = None
            self.chart_dirty = True
            self.draw_chart()
            return

        self.chart_dirty = True
        self.draw_chart()

        self.candle_animation_job = self.after(
            12,
            self._animate_candle,
        )

    # ================================================================
    # HISTORY
    # ================================================================

    def on_history_slider(self, value):
        try:
            target = float(value)
        except (
            ValueError,
            TypeError,
        ):
            return

        target = max(
            0.0,
            min(
                1.0,
                target,
            ),
        )

        if target >= 0.995:
            target = 1.0

            self.history_label.configure(
                text="LIVE",
                text_color=self.green,
            )

        else:
            self.history_label.configure(
                text="HISTORY",
                text_color=self.muted,
            )

        self.history_target = target

        self.start_history_animation(
            target
        )

    def start_history_animation(
        self,
        target,
    ):
        target = max(
            0.0,
            min(
                1.0,
                float(target),
            ),
        )

        if self.history_animation_job:
            try:
                self.after_cancel(
                    self.history_animation_job
                )
            except Exception:
                pass

        self.history_animation_start = (
            self.history_position
        )

        self.history_animation_target = target

        self.history_animation_clock = (
            time.perf_counter()
        )

        if abs(
            target
            - self.history_position
        ) < 0.0005:
            self.history_position = target
            self.chart_dirty = True
            self.draw_chart()
            return

        self.history_animation_job = self.after(
            8,
            self._animate_history,
        )

    def _animate_history(self):
        if self.destroyed:
            self.history_animation_job = None
            return

        elapsed = (
            time.perf_counter()
            - self.history_animation_clock
        )

        duration = (
            self.history_animation_duration
            / 1000.0
        )

        progress = max(
            0.0,
            min(
                1.0,
                elapsed / duration,
            ),
        )

        if progress >= 1.0:
            self.history_position = (
                self.history_animation_target
            )

            self.history_animation_job = None
            self.chart_dirty = True
            self.draw_chart()
            return

        eased = (
            1.0
            - (1.0 - progress) ** 3
        )

        self.history_position = (
            self.history_animation_start
            + (
                self.history_animation_target
                - self.history_animation_start
            )
            * eased
        )

        self.chart_dirty = True
        self.draw_chart()

        self.history_animation_job = self.after(
            8,
            self._animate_history,
        )

    def get_visible_candles(self):
        if not self.candles:
            return [], 0

        total = len(
            self.candles
        )

        visible_count = min(
            self.visible_candles,
            total,
        )

        if total <= visible_count:
            return (
                self.candles,
                0,
            )

        max_start = (
            total
            - visible_count
        )

        start = int(
            max_start
            * self.history_position
        )

        return (
            self.candles[
                start:start + visible_count
            ],
            start,
        )

    # ================================================================
    # CHART MOUSE
    # ================================================================

    def on_chart_mouse_down(self, event):
        if self.drawing_mode != "cursor":
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            self.active_drawing = None
            return

        self.chart_pan_start_x = event.x

        self.chart_pan_start_position = (
            self.history_position
        )

        self.chart_pan_active = True

    def on_chart_mouse_drag(self, event):
        if self.drawing_mode != "cursor":
            if self.drag_start_x is None:
                return

            self.active_drawing = {
                "type": self.drawing_mode,
                "x1": self.drag_start_x,
                "y1": self.drag_start_y,
                "x2": event.x,
                "y2": event.y,
            }

            self.chart_dirty = True
            self.draw_chart()
            return

        if not self.chart_pan_active:
            return

        if self.chart_pan_start_x is None:
            return

        dx = (
            event.x
            - self.chart_pan_start_x
        )

        chart_width = max(
            1,
            self.chart.winfo_width()
            - 76,
        )

        delta = (
            -dx
            / chart_width
        )

        target = (
            self.chart_pan_start_position
            + delta
        )

        target = max(
            0.0,
            min(
                1.0,
                target,
            ),
        )

        self.history_position = target
        self.history_target = target

        try:
            self.history_slider.set(
                target
            )
        except Exception:
            pass

        if target >= 0.995:
            self.history_label.configure(
                text="LIVE",
                text_color=self.green,
            )
        else:
            self.history_label.configure(
                text="HISTORY",
                text_color=self.muted,
            )

        self.chart_dirty = True
        self.draw_chart()

    def on_chart_mouse_up(self, event):
        if self.drawing_mode != "cursor":
            if self.drag_start_x is None:
                return

            drawing = {
                "type": self.drawing_mode,
                "x1": self.drag_start_x,
                "y1": self.drag_start_y,
                "x2": event.x,
                "y2": event.y,
            }

            if (
                abs(
                    drawing["x2"]
                    - drawing["x1"]
                ) >= 3
                or abs(
                    drawing["y2"]
                    - drawing["y1"]
                ) >= 3
            ):
                self.drawings.append(
                    drawing
                )

            self.drag_start_x = None
            self.drag_start_y = None
            self.active_drawing = None

            self.chart_dirty = True
            self.draw_chart()
            return

        self.chart_pan_active = False
        self.chart_pan_start_x = None

    # ================================================================
    # HOVER
    # ================================================================

    def on_chart_motion(self, event):
        self.chart_hover = True
        self.hover_x = event.x
        self.hover_y = event.y

        self.chart_dirty = True
        self.draw_chart()

    def on_chart_leave(self, _event):
        self.chart_hover = False
        self.hover_x = None
        self.hover_y = None

        self.chart_dirty = True
        self.draw_chart()

    # ================================================================
    # DRAWING TOOLS
    # ================================================================

    def set_drawing_mode(self, mode):
        self.drawing_mode = mode

        for name, button in (
            self.draw_buttons.items()
        ):
            button.configure(
                fg_color=(
                    self.blue
                    if name == mode
                    else "transparent"
                )
            )

        self.chart.configure(
            cursor=(
                ""
                if mode == "cursor"
                else "crosshair"
            )
        )

    def clear_drawings(self):
        self.drawings.clear()
        self.active_drawing = None

        self.chart_dirty = True
        self.draw_chart()

    def render_drawing(
        self,
        drawing,
        active=False,
    ):
        dtype = drawing.get(
            "type"
        )

        x1 = drawing.get(
            "x1",
            0,
        )

        y1 = drawing.get(
            "y1",
            0,
        )

        x2 = drawing.get(
            "x2",
            0,
        )

        y2 = drawing.get(
            "y2",
            0,
        )

        color = (
            "#60a5fa"
            if active
            else self.blue
        )

        if dtype == "line":
            self.chart.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                width=2,
            )

        elif dtype == "horizontal":
            self.chart.create_line(
                8,
                y1,
                self.chart.winfo_width() - 64,
                y1,
                fill=color,
                width=2,
                dash=(6, 4),
            )

        elif dtype == "rectangle":
            self.chart.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                outline=color,
                width=2,
            )

    # ================================================================
    # CHART HELPERS
    # ================================================================

    def y_to_price(
        self,
        y,
        candles,
    ):
        if not candles:
            return 0.0

        width = self.chart.winfo_width()
        height = self.chart.winfo_height()

        left = 12
        right = width - 64
        top = 12
        bottom = height - 30

        highest = max(
            c["high"]
            for c in candles
        )

        lowest = min(
            c["low"]
            for c in candles
        )

        if highest == lowest:
            padding = max(
                abs(highest)
                * 0.002,
                1.0,
            )
        else:
            padding = (
                highest
                - lowest
            ) * 0.08

        chart_high = (
            highest
            + padding
        )

        chart_low = (
            lowest
            - padding
        )

        chart_height = max(
            1,
            bottom - top,
        )

        ratio = (
            bottom - y
        ) / chart_height

        return (
            chart_low
            + ratio
            * (
                chart_high
                - chart_low
            )
        )

    def get_candle_at_x(
        self,
        x,
        candles,
    ):
        if not candles:
            return (
                None,
                -1,
            )

        width = self.chart.winfo_width()

        left = 12
        right = width - 64

        chart_width = max(
            1,
            right - left,
        )

        spacing = (
            chart_width
            / max(
                len(candles),
                1,
            )
        )

        index = int(
            (x - left)
            / spacing
        )

        if (
            index < 0
            or index >= len(candles)
        ):
            return (
                None,
                -1,
            )

        return (
            candles[index],
            index,
        )

    def draw_crosshair(
        self,
        candles,
        left,
        right,
        top,
        bottom,
    ):
        if not self.chart_hover:
            return

        if (
            self.hover_x is None
            or self.hover_y is None
        ):
            return

        x = self.hover_x
        y = self.hover_y

        if not (
            left <= x <= right
            and top <= y <= bottom
        ):
            return

        self.chart.create_line(
            x,
            top,
            x,
            bottom,
            fill=self.muted,
            dash=(3, 4),
            width=1,
        )

        self.chart.create_line(
            left,
            y,
            right,
            y,
            fill=self.muted,
            dash=(3, 4),
            width=1,
        )

        candle, index = (
            self.get_candle_at_x(
                x,
                candles,
            )
        )

        if candle is None:
            return

        tooltip_width = 160
        tooltip_height = 88

        tx = x + 14
        ty = y + 14

        if (
            tx + tooltip_width
            > self.chart.winfo_width()
        ):
            tx = (
                x
                - tooltip_width
                - 14
            )

        if (
            ty + tooltip_height
            > self.chart.winfo_height()
        ):
            ty = (
                y
                - tooltip_height
                - 14
            )

        self.chart.create_rectangle(
            tx,
            ty,
            tx + tooltip_width,
            ty + tooltip_height,
            fill=self.card,
            outline=self.border,
            width=1,
        )

        timestamp = candle.get(
            "timestamp"
        )

        if timestamp:
            try:
                candle_time = time.strftime(
                    "%H:%M:%S",
                    time.localtime(
                        timestamp
                    ),
                )
            except Exception:
                candle_time = "--:--:--"
        else:
            candle_time = "--:--:--"

        text = (
            f"{self.symbol}  {candle_time}\n"
            f"O  {candle['open']:,.2f}\n"
            f"H  {candle['high']:,.2f}\n"
            f"L  {candle['low']:,.2f}\n"
            f"C  {candle['close']:,.2f}"
        )

        self.chart.create_text(
            tx + 8,
            ty + 7,
            text=text,
            anchor="nw",
            fill=self.text,
            font=("Arial", 8),
        )

        price = self.y_to_price(
            y,
            candles,
        )

        self.chart.create_rectangle(
            right,
            y - 9,
            self.chart.winfo_width(),
            y + 9,
            fill=self.blue,
            outline="",
        )

        self.chart.create_text(
            self.chart.winfo_width() - 4,
            y,
            text=f"{price:,.2f}",
            anchor="e",
            fill="#ffffff",
            font=("Arial", 8, "bold"),
        )

    # ================================================================
    # ROUNDED CANDLE
    # ================================================================

    def draw_rounded_candle(
        self,
        x1,
        y1,
        x2,
        y2,
        radius,
        color,
    ):
        r = max(
            1,
            min(
                radius,
                (x2 - x1) / 2,
                (y2 - y1) / 2,
            ),
        )

        self.chart.create_rectangle(
            x1 + r,
            y1,
            x2 - r,
            y2,
            fill=color,
            outline=color,
        )

        self.chart.create_rectangle(
            x1,
            y1 + r,
            x2,
            y2 - r,
            fill=color,
            outline=color,
        )

        self.chart.create_arc(
            x1,
            y1,
            x1 + 2 * r,
            y1 + 2 * r,
            start=90,
            extent=90,
            fill=color,
            outline=color,
        )

        self.chart.create_arc(
            x2 - 2 * r,
            y1,
            x2,
            y1 + 2 * r,
            start=0,
            extent=90,
            fill=color,
            outline=color,
        )

        self.chart.create_arc(
            x1,
            y2 - 2 * r,
            x1 + 2 * r,
            y2,
            start=180,
            extent=90,
            fill=color,
            outline=color,
        )

        self.chart.create_arc(
            x2 - 2 * r,
            y2 - 2 * r,
            x2,
            y2,
            start=270,
            extent=90,
            fill=color,
            outline=color,
        )

    # ================================================================
    # CHART RENDER
    # ================================================================

    def draw_chart(self):
        if not hasattr(
            self,
            "chart",
        ):
            return

        try:
            width = self.chart.winfo_width()
            height = self.chart.winfo_height()
        except Exception:
            return

        if (
            width < 100
            or height < 80
        ):
            return

        self.chart.delete(
            "all"
        )

        self.chart.configure(
            background=self.chart_bg
        )

        candles, start_index = (
            self.get_visible_candles()
        )

        if not candles:
            self.chart.create_text(
                width / 2,
                height / 2,
                text=(
                    "Waiting for "
                    "market data..."
                ),
                fill=self.muted,
                font=("Arial", 10),
            )

            self.chart_dirty = False
            return

        left = 12
        right = width - 64
        top = 12
        bottom = height - 30

        chart_width = max(
            1,
            right - left,
        )

        chart_height = max(
            1,
            bottom - top,
        )

        # ------------------------------------------------------------
        # GRID
        # ------------------------------------------------------------

        for i in range(1, 5):
            y = (
                top
                + chart_height
                * i
                / 5
            )

            self.chart.create_line(
                left,
                y,
                right,
                y,
                fill=self.grid_color,
                width=1,
            )

        for i in range(1, 9):
            x = (
                left
                + chart_width
                * i
                / 9
            )

            self.chart.create_line(
                x,
                top,
                x,
                bottom,
                fill=self.grid_color,
                width=1,
            )

        # ------------------------------------------------------------
        # SCALE
        # ------------------------------------------------------------

        highest = max(
            c["high"]
            for c in candles
        )

        lowest = min(
            c["low"]
            for c in candles
        )

        if highest == lowest:
            padding = max(
                abs(highest)
                * 0.002,
                1.0,
            )
        else:
            padding = (
                highest
                - lowest
            ) * 0.08

        chart_high = (
            highest
            + padding
        )

        chart_low = (
            lowest
            - padding
        )

        value_range = max(
            chart_high
            - chart_low,
            0.000001,
        )

        def price_to_y(value):
            ratio = (
                value
                - chart_low
            ) / value_range

            return (
                bottom
                - ratio
                * chart_height
            )

        # ------------------------------------------------------------
        # CANDLES
        # ------------------------------------------------------------

        count = len(candles)

        spacing = (
            chart_width
            / max(
                count,
                1,
            )
        )

        candle_width = max(
            4,
            min(
                14,
                spacing * 0.68,
            ),
        )

        last_x = left
        last_y = bottom

        for index, candle in enumerate(
            candles
        ):
            x = (
                left
                + (
                    index
                    + 0.5
                )
                * spacing
            )

            animated_close = (
                candle["close"]
            )

            if (
                index
                == count - 1
            ):
                animated_close = (
                    self.get_animated_close(
                        candle["close"]
                    )
                )

            open_y = price_to_y(
                candle["open"]
            )

            close_y = price_to_y(
                animated_close
            )

            high_y = price_to_y(
                candle["high"]
            )

            low_y = price_to_y(
                candle["low"]
            )

            bullish = (
                candle["close"]
                >= candle["open"]
            )

            candle_color = (
                self.green
                if bullish
                else self.red
            )

            # Wick
            self.chart.create_line(
                x,
                high_y,
                x,
                low_y,
                fill=candle_color,
                width=1,
            )

            body_top = min(
                open_y,
                close_y,
            )

            body_bottom = max(
                open_y,
                close_y,
            )

            if (
                body_bottom
                - body_top
                < 2
            ):
                body_bottom = (
                    body_top + 2
                )

            self.draw_rounded_candle(
                x
                - candle_width / 2,
                body_top,
                x
                + candle_width / 2,
                body_bottom,
                min(
                    3,
                    candle_width / 2,
                ),
                candle_color,
            )

            if index == count - 1:
                last_x = x
                last_y = close_y

        # ------------------------------------------------------------
        # CURRENT PRICE
        # ------------------------------------------------------------

        current_price = (
            candles[-1]["close"]
        )

        current_color = (
            self.green
            if candles[-1]["close"]
            >= candles[-1]["open"]
            else self.red
        )

        self.chart.create_line(
            left,
            last_y,
            right,
            last_y,
            fill=self.muted,
            dash=(4, 3),
            width=1,
        )

        self.chart.create_oval(
            last_x - 3,
            last_y - 3,
            last_x + 3,
            last_y + 3,
            fill=current_color,
            outline="",
        )

        tag_height = 19

        tag_top = max(
            0,
            last_y
            - tag_height / 2,
        )

        tag_bottom = min(
            height,
            last_y
            + tag_height / 2,
        )

        self.chart.create_rectangle(
            right,
            tag_top,
            width,
            tag_bottom,
            fill=current_color,
            outline="",
        )

        self.chart.create_text(
            width - 4,
            last_y,
            text=(
                f"${current_price:,.2f}"
            ),
            fill="#ffffff",
            anchor="e",
            font=(
                "Arial",
                8,
                "bold",
            ),
        )

        # ------------------------------------------------------------
        # PRICE AXIS
        # ------------------------------------------------------------

        for value in (
            chart_high,
            chart_high
            - value_range * 0.25,
            chart_high
            - value_range * 0.50,
            chart_high
            - value_range * 0.75,
            chart_low,
        ):
            self.chart.create_text(
                width - 3,
                price_to_y(
                    value
                ),
                text=(
                    f"{value:,.2f}"
                ),
                fill=self.muted,
                anchor="e",
                font=(
                    "Arial",
                    7,
                ),
            )

        # ------------------------------------------------------------
        # TIME AXIS
        # ------------------------------------------------------------

        label_count = min(
            6,
            len(candles),
        )

        if label_count > 1:
            for i in range(
                label_count
            ):
                idx = int(
                    i
                    * (
                        len(candles)
                        - 1
                    )
                    / (
                        label_count
                        - 1
                    )
                )

                candle = candles[idx]

                timestamp = candle.get(
                    "timestamp"
                )

                if timestamp:
                    try:
                        label = time.strftime(
                            "%H:%M",
                            time.localtime(
                                timestamp
                            ),
                        )
                    except Exception:
                        label = "--:--"
                else:
                    label = "--:--"

                x = (
                    left
                    + (
                        idx
                        + 0.5
                    )
                    * spacing
                )

                self.chart.create_text(
                    x,
                    height - 8,
                    text=label,
                    fill=self.muted,
                    anchor="s",
                    font=(
                        "Arial",
                        7,
                    ),
                )

        # ------------------------------------------------------------
        # OHLC
        # ------------------------------------------------------------

        current = candles[-1]

        info = (
            f"O {current['open']:,.2f}   "
            f"H {current['high']:,.2f}   "
            f"L {current['low']:,.2f}   "
            f"C {current['close']:,.2f}"
        )

        self.chart.create_text(
            left,
            height - 8,
            text=info,
            fill=self.muted,
            anchor="sw",
            font=(
                "Arial",
                7,
            ),
        )

        # ------------------------------------------------------------
        # HISTORY STATUS
        # ------------------------------------------------------------

        if self.history_position < 0.995:
            self.chart.create_text(
                left,
                top,
                text=(
                    f"HISTORY  •  "
                    f"{start_index + 1}"
                ),
                fill=self.muted,
                anchor="nw",
                font=(
                    "Arial",
                    8,
                    "bold",
                ),
            )

        # ------------------------------------------------------------
        # DRAWINGS
        # ------------------------------------------------------------

        for drawing in self.drawings:
            self.render_drawing(
                drawing,
                active=False,
            )

        if self.active_drawing:
            self.render_drawing(
                self.active_drawing,
                active=True,
            )

        # ------------------------------------------------------------
        # CROSSHAIR / TOOLTIP
        # ------------------------------------------------------------

        self.draw_crosshair(
            candles,
            left,
            right,
            top,
            bottom,
        )

        self.chart_dirty = False

    # ================================================================
    # RESIZE
    # ================================================================

    def on_chart_resize(self, event):
        self.chart_width = event.width
        self.chart_height = event.height

        self.chart_dirty = True

        try:
            self.after_idle(
                self.draw_chart
            )
        except Exception:
            pass

    # ================================================================
    # ANALYSIS
    # ================================================================

    def set_analysis_period(
        self,
        period,
    ):
        self.analysis_period = period

        for name, button in (
            self.analysis_buttons.items()
        ):
            button.configure(
                fg_color=(
                    self.blue
                    if name == period
                    else "transparent"
                )
            )

        self.calculate_analysis()

    def calculate_analysis(self):
        candles = self.candles

        if len(candles) < 2:
            self.analysis_label.configure(
                text="Not enough data",
                text_color=self.muted,
            )
            return

        limits = {
            "15m": 15,
            "1H": 60,
            "4H": 120,
            "1D": 240,
            "7D": 300,
        }

        selected = min(
            limits.get(
                self.analysis_period,
                60,
            ),
            len(candles),
        )

        data = candles[
            -selected:
        ]

        start = float(
            data[0]["open"]
        )

        end = float(
            data[-1]["close"]
        )

        high = max(
            c["high"]
            for c in data
        )

        low = min(
            c["low"]
            for c in data
        )

        change = (
            (
                end - start
            )
            / start
            * 100
            if start
            else 0
        )

        direction = (
            "UP"
            if change > 0
            else "DOWN"
            if change < 0
            else "FLAT"
        )

        self.analysis_label.configure(
            text=(
                f"{direction}  "
                f"{change:+.2f}%   "
                f"Range "
                f"${low:,.0f}"
                f" - "
                f"${high:,.0f}"
            ),
            text_color=(
                self.green
                if change > 0
                else self.red
                if change < 0
                else self.muted
            ),
        )

    # ================================================================
    # ACCOUNT
    # ================================================================

    def build_account_section(
        self,
        market,
    ):
        self.account_outer, account = (
            self.create_accent_card(
                market,
                accent=True,
                corner_radius=9,
            )
        )

        self.account_outer.grid(
            row=6,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 7),
        )

        account.configure(
            height=52
        )

        self.balance_label = (
            self.account_stat(
                account,
                "Balance",
                "$0.00",
            )
        )

        self.equity_label = (
            self.account_stat(
                account,
                "Equity",
                "$0.00",
            )
        )

        self.position_label = (
            self.account_stat(
                account,
                "Position",
                "0 BTC",
            )
        )

        self.pnl_label = (
            self.account_stat(
                account,
                "PnL",
                "$0.00",
            )
        )

    def account_stat(
        self,
        parent,
        title,
        value,
    ):
        box = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        box.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7,
        )

        ctk.CTkLabel(
            box,
            text=title,
            text_color=self.muted,
            font=ctk.CTkFont(size=8),
        ).pack(
            anchor="w",
            pady=(3, 0),
        )

        label = ctk.CTkLabel(
            box,
            text=value,
            text_color=self.text,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        )

        label.pack(
            anchor="w"
        )

        return label

    # ================================================================
    # ORDER HISTORY
    # ================================================================

    def update_order_history(self):
        try:
            orders = self.engine().orders()
        except Exception:
            return

        count = len(
            orders
        )

        self.order_count_label.configure(
            text=f"{count} orders"
        )

        if count == self.last_order_count:
            return

        self.last_order_count = count

        self.orders_text.configure(
            state="normal"
        )

        self.orders_text.delete(
            "1.0",
            "end",
        )

        if not orders:
            self.orders_text.insert(
                "end",
                "No orders yet.",
            )

        else:
            for order in reversed(
                orders[-6:]
            ):
                side_value = order.get(
                    "side",
                    0,
                )

                status_value = order.get(
                    "status",
                    0,
                )

                side = (
                    "BUY"
                    if side_value == 0
                    else "SELL"
                )

                status = str(
                    status_value
                )

                symbol = order.get(
                    "symbol",
                    "",
                )

                quantity = float(
                    order.get(
                        "quantity",
                        0.0,
                    )
                )

                price = float(
                    order.get(
                        "price",
                        0.0,
                    )
                )

                order_id = order.get(
                    "id",
                    0,
                )

                timestamp = order.get(
                    "timestamp",
                    order.get(
                        "time",
                        None,
                    ),
                )

                if timestamp:
                    try:
                        if (
                            timestamp
                            > 10_000_000_000
                        ):
                            timestamp /= 1000

                        order_time = time.strftime(
                            "%H:%M:%S",
                            time.localtime(
                                timestamp
                            ),
                        )
                    except Exception:
                        order_time = "--:--:--"
                else:
                    order_time = "--:--:--"

                self.orders_text.insert(
                    "end",
                    (
                        f"{order_time}  "
                        f"#{order_id:<4} "
                        f"{side:<4} "
                        f"{symbol:<9} "
                        f"{quantity:g} "
                        f"@ ${price:,.2f} "
                        f"[{status}]\n"
                    ),
                )

        self.orders_text.configure(
            state="disabled"
        )

    # ================================================================
    # EXECUTE BUTTON
    # ================================================================

    def update_execute_button(self):
        enabled = (
            self.order_type.get()
            == "Market"
        )

        base = (
            self.symbol[:-4]
            if self.symbol.endswith(
                "USDT"
            )
            else self.symbol
        )

        self.execute_button.configure(
            text=(
                f"{self.side} {base}"
            ),
            fg_color=(
                self.green_hover
                if self.side == "BUY"
                else self.red_hover
            ),
            hover_color=(
                "#15803d"
                if self.side == "BUY"
                else "#b91c1c"
            ),
            state=(
                "normal"
                if enabled
                else "disabled"
            ),
        )

    # ================================================================
    # CHART CACHE
    # ================================================================

    def chart_cache_file(self):
        safe_symbol = (
            self.symbol
            .replace("/", "_")
            .replace("\\", "_")
        )

        safe_tf = (
            self.selected_timeframe
            .replace("/", "_")
        )

        return (
            self.chart_cache_dir
            / f"{safe_symbol}_{safe_tf}.json"
        )

    def save_chart_cache(self):
        try:
            data = {
                "symbol": self.symbol,
                "timeframe": (
                    self.selected_timeframe
                ),
                "candles": self.candles[
                    -self.max_candles:
                ],
                "saved_at": time.time(),
            }

            with open(
                self.chart_cache_file(),
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                )

        except Exception:
            pass

    def load_chart_cache(self):
        try:
            path = (
                self.chart_cache_file()
            )

            if not path.exists():
                return

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(
                    file
                )

            cached = data.get(
                "candles",
                [],
            )

            if not cached:
                return

            normalized = []

            for candle in cached:
                try:
                    normalized.append(
                        {
                            "open": float(
                                candle["open"]
                            ),
                            "high": float(
                                candle["high"]
                            ),
                            "low": float(
                                candle["low"]
                            ),
                            "close": float(
                                candle["close"]
                            ),
                            "timestamp": float(
                                candle.get(
                                    "timestamp",
                                    time.time(),
                                )
                            ),
                        }
                    )
                except Exception:
                    continue

            if not normalized:
                return

            self.candles = normalized[
                -self.max_candles:
            ]

            self.last_price = float(
                self.candles[-1]["close"]
            )

            self.chart_dirty = True

        except Exception:
            pass

    # ================================================================
    # REFRESH
    # ================================================================

    def refresh(self):
        if self.destroyed:
            return

        try:
            engine = self.engine()

            price = float(
                engine.get_price(
                    self.symbol
                )
            )

            previous_price = (
                self.last_price
            )

            self.update_candles(
                price
            )

            self.price_label.configure(
                text=f"${price:,.2f}"
            )

            if (
                previous_price is not None
                and previous_price > 0
            ):
                change = (
                    (
                        price
                        - previous_price
                    )
                    / previous_price
                    * 100.0
                )

                if change > 0:
                    self.price_change_label.configure(
                        text=f"+{change:.3f}%",
                        text_color=self.green,
                    )

                elif change < 0:
                    self.price_change_label.configure(
                        text=f"{change:.3f}%",
                        text_color=self.red,
                    )

                else:
                    self.price_change_label.configure(
                        text="0.000%",
                        text_color=self.muted,
                    )

            try:
                running = (
                    engine.live_market_running()
                )

                interval = (
                    engine.live_market_interval_ms()
                )

                self.live_label.configure(
                    text=(
                        "● LIVE"
                        if running
                        else "● OFFLINE"
                    ),
                    text_color=(
                        self.green
                        if running
                        else self.red
                    ),
                )

                self.market_interval_label.configure(
                    text=(
                        f"Core: {interval} ms"
                    )
                )

            except Exception:
                pass

            account = engine.account()

            cash = float(
                account.get(
                    "cash",
                    0.0,
                )
            )

            equity = float(
                account.get(
                    "equity",
                    account.get(
                        "total_equity",
                        0.0,
                    ),
                )
            )

            pnl = float(
                account.get(
                    "pnl",
                    account.get(
                        "total_pnl",
                        0.0,
                    ),
                )
            )

            position = engine.position(
                self.symbol
            )

            quantity = float(
                position.get(
                    "quantity",
                    0.0,
                )
            )

            self.balance_label.configure(
                text=f"${cash:,.2f}"
            )

            self.equity_label.configure(
                text=f"${equity:,.2f}"
            )

            base = (
                self.symbol[:-4]
                if self.symbol.endswith(
                    "USDT"
                )
                else self.symbol
            )

            self.position_label.configure(
                text=f"{quantity:g} {base}"
            )

            self.pnl_label.configure(
                text=f"${pnl:,.2f}",
                text_color=(
                    self.green
                    if pnl >= 0
                    else self.red
                ),
            )

            self.update_cost()
            self.update_execute_button()
            self.update_order_history()

            self.calculate_analysis()

            # Keep chart history.
            self.save_chart_cache()

            if self.chart_dirty:
                self.draw_chart()

        except Exception as error:
            try:
                self.price_label.configure(
                    text="$0.00"
                )

                self.status.configure(
                    text=(
                        f"Core error: "
                        f"{error}"
                    ),
                    text_color=self.red,
                )

            except Exception:
                pass

    # ================================================================
    # CLOCK
    # ================================================================

    def start_clock(self):
        if self.destroyed:
            return

        self.update_clock()

    def update_clock(self):
        if self.destroyed:
            self.clock_job = None
            return

        try:
            self.chart_clock_label.configure(
                text=time.strftime(
                    "%H:%M:%S"
                )
            )
        except Exception:
            pass

        self.clock_job = self.after(
            1000,
            self.update_clock,
        )

    # ================================================================
    # AUTO REFRESH
    # ================================================================

    def start_auto_refresh(self):
        if (
            self.destroyed
            or self.refresh_job is not None
        ):
            return

        self.refresh_job = self.after(
            self.refresh_interval,
            self._auto_refresh,
        )

    def _auto_refresh(self):
        self.refresh_job = None

        if self.destroyed:
            return

        try:
            self.refresh()
        except Exception as error:
            print(
                f"[TRADE REFRESH ERROR] "
                f"{error}"
            )

        self.start_auto_refresh()

    def stop_auto_refresh(self):
        if self.refresh_job is not None:
            try:
                self.after_cancel(
                    self.refresh_job
                )
            except Exception:
                pass

        self.refresh_job = None

        if self.clock_job is not None:
            try:
                self.after_cancel(
                    self.clock_job
                )
            except Exception:
                pass

        self.clock_job = None

        if self.history_animation_job is not None:
            try:
                self.after_cancel(
                    self.history_animation_job
                )
            except Exception:
                pass

        self.history_animation_job = None

        if self.candle_animation_job is not None:
            try:
                self.after_cancel(
                    self.candle_animation_job
                )
            except Exception:
                pass

        self.candle_animation_job = None

    # ================================================================
    # DESTROY
    # ================================================================

    def destroy(self):
        self.destroyed = True

        try:
            self.save_chart_cache()
        except Exception:
            pass

        self.stop_auto_refresh()

        try:
            super().destroy()
        except Exception:
            pass