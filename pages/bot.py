import customtkinter as ctk
from datetime import datetime
import json
import os


class LocalBot:
    """
    UI-side bot model.

    This is intentionally only a control/UI layer.
    The real strategy execution will be connected to the
    C++ BotManager/Runtime later.
    """

    def __init__(
        self,
        name,
        version="1.0.0",
        author="Local",
        description=""
    ):
        self.id = name.lower().replace(" ", "-")
        self.name = name
        self.version = version
        self.author = author
        self.description = description

        self.enabled = False
        self.running = False

        self.last_action = "Idle"
        self.trades = 0
        self.pnl = 0.0

        self.logs = []


class BotPage(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(
            parent,
            corner_radius=0
        )

        self.app = app

        self.bots = {}
        self.selected_bot = None

        self._load_bots()

        self.build_ui()
        self.refresh()

    # =====================================================
    # BOT STORAGE
    # =====================================================

    @property
    def storage_path(self):
        base = os.environ.get("LOCALAPPDATA")

        if base:
            root = os.path.join(
                base,
                "Crytopz",
                "bots"
            )
        else:
            root = os.path.join(
                os.path.expanduser("~"),
                ".crytopz",
                "bots"
            )

        os.makedirs(
            root,
            exist_ok=True
        )

        return os.path.join(
            root,
            "bots.json"
        )

    def _load_bots(self):

        path = self.storage_path

        if os.path.exists(path):

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                for item in data:

                    bot = LocalBot(
                        item.get(
                            "name",
                            "Unnamed Bot"
                        ),
                        item.get(
                            "version",
                            "1.0.0"
                        ),
                        item.get(
                            "author",
                            "Local"
                        ),
                        item.get(
                            "description",
                            ""
                        )
                    )

                    bot.id = item.get(
                        "id",
                        bot.id
                    )

                    bot.enabled = bool(
                        item.get(
                            "enabled",
                            False
                        )
                    )

                    bot.running = False

                    bot.last_action = item.get(
                        "last_action",
                        "Idle"
                    )

                    bot.trades = int(
                        item.get(
                            "trades",
                            0
                        )
                    )

                    bot.pnl = float(
                        item.get(
                            "pnl",
                            0.0
                        )
                    )

                    bot.logs = list(
                        item.get(
                            "logs",
                            []
                        )
                    )

                    self.bots[bot.id] = bot

            except (
                OSError,
                ValueError,
                TypeError,
                json.JSONDecodeError
            ):
                pass

        if not self.bots:

            bot = LocalBot(
                "SimpleBot",
                "1.0.0",
                "Crytopz",
                "Built-in paper trading strategy."
            )

            self.bots[bot.id] = bot

            self._save_bots()

    def _save_bots(self):

        data = []

        for bot in self.bots.values():

            data.append(
                {
                    "id": bot.id,
                    "name": bot.name,
                    "version": bot.version,
                    "author": bot.author,
                    "description": bot.description,
                    "enabled": bot.enabled,
                    "last_action": bot.last_action,
                    "trades": bot.trades,
                    "pnl": bot.pnl,
                    "logs": bot.logs[-100:]
                }
            )

        try:

            with open(
                self.storage_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

        except OSError:
            pass

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # HEADER
        # =================================================

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=28,
            pady=(24, 12)
        )

        title_box = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_box.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            title_box,
            text="Bot Control Center",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_box,
            text="Manage, monitor and configure your trading bots",
            text_color="gray"
        ).pack(
            anchor="w"
        )

        ctk.CTkButton(
            header,
            text=lang.t("create_bot"),
            width=125,
            command=self.create_bot
        ).pack(
            side="right",
            padx=5
        )

        ctk.CTkButton(
            header,
            text=lang.t("import_bot"),
            width=110,
            fg_color="transparent",
            border_width=1,
            command=self.import_bot
        ).pack(
            side="right",
            padx=5
        )

        # =================================================
        # MAIN AREA
        # =================================================

        self.main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        # =================================================
        # LEFT - BOT LIST
        # =================================================

        self.bot_list = ctk.CTkFrame(
            self.main,
            width=285,
            corner_radius=14
        )

        self.bot_list.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        self.bot_list.pack_propagate(
            False
        )

        ctk.CTkLabel(
            self.bot_list,
            text="BOT LIBRARY",
            text_color="gray",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 10)
        )

        self.bot_scroll = ctk.CTkScrollableFrame(
            self.bot_list,
            fg_color="transparent"
        )

        self.bot_scroll.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 8)
        )

        # =================================================
        # CENTER - MONITOR
        # =================================================

        self.monitor = ctk.CTkFrame(
            self.main,
            corner_radius=14
        )

        self.monitor.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.monitor_header = ctk.CTkFrame(
            self.monitor,
            fg_color="transparent"
        )

        self.monitor_header.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        self.bot_title = ctk.CTkLabel(
            self.monitor_header,
            text="No bot selected",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        self.bot_title.pack(
            side="left"
        )

        self.bot_status = ctk.CTkLabel(
            self.monitor_header,
            text="● STOPPED",
            text_color="gray",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        self.bot_status.pack(
            side="right"
        )

        # -------------------------------------------------
        # ACTION
        # -------------------------------------------------

        self.action_box = ctk.CTkFrame(
            self.monitor,
            corner_radius=12
        )

        self.action_box.pack(
            fill="x",
            padx=18,
            pady=8
        )

        ctk.CTkLabel(
            self.action_box,
            text="CURRENT ACTION",
            text_color="gray",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 2)
        )

        self.action_label = ctk.CTkLabel(
            self.action_box,
            text="Idle",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        self.action_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 14)
        )

        # -------------------------------------------------
        # STATS
        # -------------------------------------------------

        stats = ctk.CTkFrame(
            self.monitor,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            padx=13,
            pady=4
        )

        self.trade_stat = self.stat(
            stats,
            "Trades",
            "0"
        )

        self.pnl_stat = self.stat(
            stats,
            "Bot PnL",
            "$0.00"
        )

        self.version_stat = self.stat(
            stats,
            "Version",
            "-"
        )

        # -------------------------------------------------
        # LOG
        # -------------------------------------------------

        ctk.CTkLabel(
            self.monitor,
            text="EVENT LOG",
            text_color="gray",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(12, 5)
        )

        self.log_box = ctk.CTkTextbox(
            self.monitor,
            corner_radius=10,
            wrap="word"
        )

        self.log_box.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        self.log_box.configure(
            state="disabled"
        )

        # =================================================
        # RIGHT - SETTINGS
        # =================================================

        self.settings = ctk.CTkFrame(
            self.main,
            width=280,
            corner_radius=14
        )

        self.settings.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        self.settings.pack_propagate(
            False
        )

        ctk.CTkLabel(
            self.settings,
            text="BOT SETTINGS",
            text_color="gray",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 12)
        )

        self.description_label = ctk.CTkLabel(
            self.settings,
            text="Select a bot.",
            justify="left",
            anchor="w",
            wraplength=235
        )

        self.description_label.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.author_label = ctk.CTkLabel(
            self.settings,
            text="Author: -",
            text_color="gray",
            justify="left",
            anchor="w"
        )

        self.author_label.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.enable_button = ctk.CTkButton(
            self.settings,
            text="Enable Bot",
            command=self.toggle_enabled
        )

        self.enable_button.pack(
            fill="x",
            padx=20,
            pady=(25, 6)
        )

        self.run_button = ctk.CTkButton(
            self.settings,
            text="Start Bot",
            command=self.toggle_running
        )

        self.run_button.pack(
            fill="x",
            padx=20,
            pady=6
        )

        self.delete_button = ctk.CTkButton(
            self.settings,
            text="Delete Bot",
            fg_color="transparent",
            border_width=1,
            command=self.delete_bot
        )

        self.delete_button.pack(
            fill="x",
            padx=20,
            pady=6
        )

        self.runtime_label = ctk.CTkLabel(
            self.settings,
            text=(
                "Runtime\n"
                "Paper Trading\n\n"
                "C++ Runtime\n"
                "Not connected"
            ),
            text_color="gray",
            justify="left",
            anchor="w"
        )

        self.runtime_label.pack(
            fill="x",
            padx=20,
            pady=(35, 10)
        )

    # =====================================================
    # STAT CARD
    # =====================================================

    def stat(
        self,
        parent,
        title,
        value
    ):

        box = ctk.CTkFrame(
            parent,
            corner_radius=10
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
            padx=12,
            pady=(10, 0)
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
            padx=12,
            pady=(2, 10)
        )

        return label

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        for child in self.bot_scroll.winfo_children():
            child.destroy()

        if not self.bots:
            self.selected_bot = None
            self.show_empty()
            return

        for bot in self.bots.values():

            self.create_bot_card(
                bot
            )

        if (
            self.selected_bot is None
            or self.selected_bot.id not in self.bots
        ):

            self.selected_bot = next(
                iter(self.bots.values())
            )

        else:

            self.selected_bot = self.bots[
                self.selected_bot.id
            ]

        self.update_details()

    # =====================================================
    # BOT CARD
    # =====================================================

    def create_bot_card(
        self,
        bot
    ):

        card = ctk.CTkFrame(
            self.bot_scroll,
            corner_radius=10
        )

        card.pack(
            fill="x",
            padx=2,
            pady=4
        )

        title = ctk.CTkLabel(
            card,
            text=bot.name,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            padx=12,
            pady=(10, 0)
        )

        if bot.running:

            status_text = "● RUNNING"
            status_color = "#4ade80"

        elif bot.enabled:

            status_text = "● ENABLED"
            status_color = "#facc15"

        else:

            status_text = "○ DISABLED"
            status_color = "gray"

        status = ctk.CTkLabel(
            card,
            text=status_text,
            text_color=status_color,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        status.pack(
            anchor="w",
            padx=12,
            pady=(2, 8)
        )

        card.bind(
            "<Button-1>",
            lambda _event, b=bot:
                self.select_bot(b)
        )

        title.bind(
            "<Button-1>",
            lambda _event, b=bot:
                self.select_bot(b)
        )

        status.bind(
            "<Button-1>",
            lambda _event, b=bot:
                self.select_bot(b)
        )

    # =====================================================
    # SELECT
    # =====================================================

    def select_bot(
        self,
        bot
    ):

        self.selected_bot = bot

        self.update_details()

    # =====================================================
    # DETAILS
    # =====================================================

    def update_details(self):

        bot = self.selected_bot

        if bot is None:
            return

        self.bot_title.configure(
            text=bot.name
        )

        self.bot_status.configure(
            text=(
                "● RUNNING"
                if bot.running
                else "● STOPPED"
            ),
            text_color=(
                "#4ade80"
                if bot.running
                else "gray"
            )
        )

        self.action_label.configure(
            text=bot.last_action
        )

        self.trade_stat.configure(
            text=str(bot.trades)
        )

        self.pnl_stat.configure(
            text=f"${bot.pnl:,.2f}"
        )

        self.version_stat.configure(
            text=bot.version
        )

        self.description_label.configure(
            text=(
                f"{bot.description}\n\n"
                f"Version: {bot.version}"
            )
        )

        self.author_label.configure(
            text=f"Author: {bot.author}"
        )

        self.enable_button.configure(
            text=(
                "Disable Bot"
                if bot.enabled
                else "Enable Bot"
            )
        )

        self.run_button.configure(
            text=(
                "Stop Bot"
                if bot.running
                else "Start Bot"
            ),
            state=(
                "normal"
                if bot.enabled
                else "disabled"
            )
        )

        self.update_logs()

    # =====================================================
    # LOG
    # =====================================================

    def add_log(
        self,
        message
    ):

        bot = self.selected_bot

        if bot is None:
            return

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        line = (
            f"[{timestamp}] "
            f"{message}"
        )

        bot.logs.append(
            line
        )

        bot.logs = bot.logs[-100:]

        self._save_bots()
        self.update_logs()

    def update_logs(self):

        bot = self.selected_bot

        if bot is None:
            return

        self.log_box.configure(
            state="normal"
        )

        self.log_box.delete(
            "1.0",
            "end"
        )

        if bot.logs:

            self.log_box.insert(
                "end",
                "\n".join(
                    bot.logs
                )
            )

        else:

            self.log_box.insert(
                "end",
                "No events yet."
            )

        self.log_box.configure(
            state="disabled"
        )

        self.log_box.see(
            "end"
        )

    # =====================================================
    # ENABLE
    # =====================================================

    def toggle_enabled(self):

        bot = self.selected_bot

        if bot is None:
            return

        bot.enabled = not bot.enabled

        if not bot.enabled:
            bot.running = False

            bot.last_action = "Disabled"

            self.add_log(
                "Bot disabled"
            )

        else:

            bot.last_action = "Enabled"

            self.add_log(
                "Bot enabled"
            )

        self._save_bots()
        self.refresh()

    # =====================================================
    # START / STOP
    # =====================================================

    def toggle_running(self):

        bot = self.selected_bot

        if bot is None:
            return

        if not bot.enabled:
            return

        runtime = getattr(
            self.app,
            "bot_manager",
            None
        )

        if bot.running:

            if runtime is not None and hasattr(
                runtime,
                "stop_bot"
            ):

                try:
                    runtime.stop_bot(
                        bot.name
                    )
                except Exception as error:
                    self.add_log(
                        f"Runtime stop error: {error}"
                    )

            bot.running = False
            bot.last_action = "Stopped"

            self.add_log(
                "Bot stopped"
            )

        else:

            if runtime is not None and hasattr(
                runtime,
                "start_bot"
            ):

                try:
                    runtime.start_bot(
                        bot.name
                    )
                except Exception as error:
                    self.add_log(
                        f"Runtime start error: {error}"
                    )
                    return

            bot.running = True
            bot.last_action = "Waiting for market data"

            self.add_log(
                "Bot started"
            )

        self._save_bots()
        self.refresh()

    # =====================================================
    # CREATE BOT
    # =====================================================

    def create_bot(self):

        from tkinter import messagebox

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Create Bot"
        )

        dialog.geometry(
            "430x430"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.transient(
            self
        )

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Create Bot",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=(25, 20)
        )

        ctk.CTkLabel(
            dialog,
            text="Name"
        ).pack(
            anchor="w",
            padx=35
        )

        name_entry = ctk.CTkEntry(
            dialog,
            width=350,
            placeholder_text="My Trading Bot"
        )

        name_entry.pack(
            padx=35,
            pady=(5, 12)
        )

        ctk.CTkLabel(
            dialog,
            text="Version"
        ).pack(
            anchor="w",
            padx=35
        )

        version_entry = ctk.CTkEntry(
            dialog,
            width=350
        )

        version_entry.insert(
            0,
            "1.0.0"
        )

        version_entry.pack(
            padx=35,
            pady=(5, 12)
        )

        ctk.CTkLabel(
            dialog,
            text="Description"
        ).pack(
            anchor="w",
            padx=35
        )

        description_entry = ctk.CTkEntry(
            dialog,
            width=350,
            placeholder_text="Bot description"
        )

        description_entry.pack(
            padx=35,
            pady=(5, 20)
        )

        def save():

            name = name_entry.get().strip()

            version = (
                version_entry.get().strip()
                or "1.0.0"
            )

            description = (
                description_entry.get().strip()
            )

            if not name:

                messagebox.showerror(
                    "Create Bot",
                    "Bot name không được để trống.",
                    parent=dialog
                )

                return

            bot_id = (
                name.lower()
                .replace(" ", "-")
            )

            if bot_id in self.bots:

                messagebox.showerror(
                    "Create Bot",
                    "Bot này đã tồn tại.",
                    parent=dialog
                )

                return

            bot = LocalBot(
                name,
                version,
                "Local",
                description
            )

            bot.id = bot_id

            self.bots[
                bot.id
            ] = bot

            self.selected_bot = bot

            self._save_bots()

            dialog.destroy()

            self.refresh()

        ctk.CTkButton(
            dialog,
            text="Create",
            width=350,
            height=40,
            command=save
        ).pack(
            padx=35
        )

    # =====================================================
    # IMPORT
    # =====================================================

    def import_bot(self):

        from tkinter import filedialog, messagebox

        path = filedialog.askopenfilename(
            title="Import Crytopz Bot",
            filetypes=[
                (
                    "Crytopz Bot",
                    "*.cpbot"
                ),
                (
                    "JSON Bot",
                    "*.json"
                ),
                (
                    "All files",
                    "*.*"
                )
            ]
        )

        if not path:
            return

        try:

            if path.lower().endswith(
                ".json"
            ):

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

            else:

                messagebox.showinfo(
                    "Import Bot",
                    "`.cpbot` package import sẽ được nối vào Bot Package Manager ở bước tiếp theo.\n\nHiện tại chưa chạy code bên trong package."
                )

                return

            name = str(
                data.get(
                    "name",
                    ""
                )
            ).strip()

            if not name:

                raise ValueError(
                    "Bot package thiếu tên."
                )

            bot_id = (
                name.lower()
                .replace(" ", "-")
            )

            if bot_id in self.bots:

                raise ValueError(
                    "Bot đã tồn tại."
                )

            bot = LocalBot(
                name,
                str(
                    data.get(
                        "version",
                        "1.0.0"
                    )
                ),
                str(
                    data.get(
                        "author",
                        "Imported"
                    )
                ),
                str(
                    data.get(
                        "description",
                        ""
                    )
                )
            )

            bot.id = bot_id

            self.bots[
                bot.id
            ] = bot

            self.selected_bot = bot

            self._save_bots()

            self.refresh()

            messagebox.showinfo(
                "Import Bot",
                f"Đã import {name}."
            )

        except (
            OSError,
            ValueError,
            TypeError,
            json.JSONDecodeError
        ) as error:

            messagebox.showerror(
                "Import Bot",
                str(error)
            )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_bot(self):

        from tkinter import messagebox

        bot = self.selected_bot

        if bot is None:
            return

        if bot.name == "SimpleBot":

            messagebox.showinfo(
                "Delete Bot",
                "Không xóa bot built-in SimpleBot."
            )

            return

        if not messagebox.askyesno(
            "Delete Bot",
            f"Xóa bot '{bot.name}'?"
        ):

            return

        self.bots.pop(
            bot.id,
            None
        )

        self.selected_bot = None

        self._save_bots()

        self.refresh()

    # =====================================================
    # EMPTY STATE
    # =====================================================

    def show_empty(self):

        self.bot_title.configure(
            text="No bot selected"
        )

        self.bot_status.configure(
            text="● STOPPED",
            text_color="gray"
        )

        self.action_label.configure(
            text="Idle"
        )

        self.trade_stat.configure(
            text="0"
        )

        self.pnl_stat.configure(
            text="$0.00"
        )

        self.version_stat.configure(
            text="-"
        )

        self.description_label.configure(
            text="Select or create a bot."
        )

        self.author_label.configure(
            text="Author: -"
        )

        self.enable_button.configure(
            state="disabled"
        )

        self.run_button.configure(
            state="disabled"
        )

        self.delete_button.configure(
            state="disabled"
        )

        self.update_logs()


