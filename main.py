import customtkinter as ctk

from language_manager import LanguageManager

lang = LanguageManager()

import sys
import os


# ============================================================
# PYTHON DIRECTORY
# ============================================================

PYTHON_DIR = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "python"
)

if PYTHON_DIR not in sys.path:
    sys.path.insert(
        0,
        PYTHON_DIR
    )


# ============================================================
# FRONTEND / PAGES
# ============================================================

from python.frontend_api import CrytopzAPI

from pages.home import HomePage
from pages.markets import MarketsPage
from pages.trade import TradePage
from pages.bots import BotLibraryPage
from pages.order_history import OrderHistoryPage
from pages.learn import LearnPage
from pages.portfolio import PortfolioPage
from pages.settings import SettingsPage

from theme import ThemeManager


# ============================================================
# CRYTOPZ APPLICATION
# ============================================================

class Crytopz(ctk.CTk):

    def __init__(self):

        super().__init__()

        # ====================================================
        # WINDOW
        # ====================================================

        self.title(
            "crytopz"
        )

        self.geometry(
            "1400x850"
        )

        self.minsize(
            1100,
            700
        )


        # ====================================================
        # THEME
        # ====================================================

        self.theme = ThemeManager()


        # ====================================================
        # NATIVE CRYTOPZ CORE
        # ====================================================

        self.engine = CrytopzAPI(
            initial_balance=10_000.0
        )


        # ====================================================
        # LIVE MARKET
        # ====================================================

        self.live_market_enabled = False
        self._live_market_after_id = None

        self.start_live_market()


        # ====================================================
        # BOT SYSTEM
        # ====================================================

        self.bot_manager = None


        # ====================================================
        # PAGE STORAGE
        # ====================================================

        self.pages = {}


        # ====================================================
        # BUILD UI
        # ====================================================

        self.build_navbar()

        self.build_content()


        # ====================================================
        # WINDOW CLOSE
        # ====================================================

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )


        # ====================================================
        # DEFAULT PAGE
        # ====================================================

        self.show_page(
            "Home"
        )


    # ========================================================
    # LIVE MARKET
    # ========================================================

    def start_live_market(self):

        try:

            if self.engine.live_market_running():
                self.live_market_enabled = True

                self.schedule_live_market_refresh()

                print(
                    "[LIVE MARKET] Already running."
                )

                return


            started = self.engine.start_live_market()

            if started:

                self.live_market_enabled = True

                print(
                    "[LIVE MARKET] Started."
                )

                print(
                    "[LIVE MARKET] Interval:",
                    self.engine.live_market_interval_ms(),
                    "ms"
                )

                self.schedule_live_market_refresh()

            else:

                self.live_market_enabled = False

                print(
                    "[LIVE MARKET] Failed to start."
                )

        except Exception as error:

            self.live_market_enabled = False

            print(
                f"[LIVE MARKET START ERROR] {error}"
            )


    def schedule_live_market_refresh(self):

        if self._live_market_after_id is not None:

            try:
                self.after_cancel(
                    self._live_market_after_id
                )
            except Exception:
                pass

            self._live_market_after_id = None


        self._live_market_after_id = self.after(
            500,
            self._live_market_tick
        )


    def _live_market_tick(self):

        self._live_market_after_id = None

        if not self.live_market_enabled:
            return


        try:

            running = self.engine.live_market_running()

            if not running:

                print(
                    "[LIVE MARKET] Scheduler stopped unexpectedly."
                )

                self.live_market_enabled = False

                return


            # ------------------------------------------------
            # Refresh currently visible page.
            #
            # Pages that implement refresh() can read the
            # latest prices directly from app.engine.
            # ------------------------------------------------

            for page in self.pages.values():

                refresh = getattr(
                    page,
                    "refresh",
                    None
                )

                if callable(refresh):

                    try:
                        refresh()
                    except Exception as error:

                        print(
                            "[LIVE MARKET PAGE REFRESH ERROR]",
                            error
                        )


        except Exception as error:

            print(
                f"[LIVE MARKET TICK ERROR] {error}"
            )


        finally:

            if self.live_market_enabled:

                self._live_market_after_id = self.after(
                    500,
                    self._live_market_tick
                )


    def stop_live_market(self):

        self.live_market_enabled = False


        if self._live_market_after_id is not None:

            try:

                self.after_cancel(
                    self._live_market_after_id
                )

            except Exception:
                pass

            self._live_market_after_id = None


        engine = getattr(
            self,
            "engine",
            None
        )

        if engine is None:
            return


        try:

            if engine.live_market_running():

                engine.stop_live_market()

                print(
                    "[LIVE MARKET] Stopped."
                )

        except Exception as error:

            print(
                f"[LIVE MARKET STOP ERROR] {error}"
            )


    # ========================================================
    # NAVBAR
    # ========================================================

    def build_navbar(self):

        self.navbar = ctk.CTkFrame(
            self,
            height=68,
            corner_radius=0
        )

        self.navbar.pack(
            side="top",
            fill="x"
        )

        self.navbar.pack_propagate(
            False
        )


        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        ctk.CTkLabel(
            self.navbar,
            text="crytopz",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=(25, 30)
        )


        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        navigation = [

            "Home",

            "Markets",

            "Trade",

            "Bots",

            "Order History",

            "Learn",

            "Portfolio",

            "Settings"

        ]


        for name in navigation:

            button = ctk.CTkButton(

                self.navbar,

                text=name,

                width=105,

                height=38,

                fg_color="transparent",

                hover_color="#202020",

                command=lambda page=name:
                    self.show_page(page)
            )

            button.pack(
                side="left",
                padx=2
            )


        # ----------------------------------------------------
        # AI BUTTON
        # ----------------------------------------------------

        self.ai_button = ctk.CTkButton(
            self.navbar,

            text="AI",

            width=70,

            height=38,

            command=self.open_ai
        )

        self.ai_button.pack(
            side="right",
            padx=15
        )


        # ----------------------------------------------------
        # LIVE STATUS
        # ----------------------------------------------------

        self.status = ctk.CTkLabel(
            self.navbar,

            text="LIVE",

            text_color="#4ade80",

            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        self.status.pack(
            side="right",
            padx=10
        )


    # ========================================================
    # CONTENT
    # ========================================================

    def build_content(self):

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.pack(
            fill="both",
            expand=True
        )


    # ========================================================
    # PAGE MANAGER
    # ========================================================

    def show_page(
        self,
        name
    ):

        # ----------------------------------------------------
        # HIDE ALL PAGES
        # ----------------------------------------------------

        for page in self.pages.values():

            try:

                page.pack_forget()

            except Exception:

                pass


        # ----------------------------------------------------
        # CREATE PAGE WHEN NEEDED
        # ----------------------------------------------------

        if name not in self.pages:

            try:

                self.pages[name] = (
                    self.create_page(
                        name
                    )
                )

            except Exception as error:

                print(
                    f"[PAGE CREATE ERROR] "
                    f"{name}: {error}"
                )

                self.pages[name] = (
                    self.create_error_page(
                        name,
                        error
                    )
                )


        # ----------------------------------------------------
        # SHOW PAGE
        # ----------------------------------------------------

        page = self.pages[name]

        page.pack(
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # REFRESH PAGE
        # ----------------------------------------------------

        refresh = getattr(
            page,
            "refresh",
            None
        )

        if callable(refresh):

            try:

                refresh()

            except Exception as error:

                print(
                    f"[PAGE REFRESH ERROR] "
                    f"{name}: {error}"
                )


    # ========================================================
    # CREATE PAGE
    # ========================================================

    def create_page(
        self,
        name
    ):

        pages = {

            "Home":
                HomePage,

            "Markets":
                MarketsPage,

            "Trade":
                TradePage,

            "Bots":
                BotLibraryPage,

            "Order History":
                OrderHistoryPage,

            "Learn":
                LearnPage,

            "Portfolio":
                PortfolioPage,

            "Settings":
                SettingsPage

        }


        page_class = pages.get(
            name
        )


        if page_class is None:

            return self.create_error_page(
                name,
                "Unknown page"
            )


        return page_class(
            self.content,
            self
        )


    # ========================================================
    # ERROR PAGE
    # ========================================================

    def create_error_page(
        self,
        name,
        error
    ):

        frame = ctk.CTkFrame(
            self.content,
            corner_radius=0
        )


        ctk.CTkLabel(
            frame,

            text=name,

            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        ).pack(
            pady=(100, 10)
        )


        ctk.CTkLabel(
            frame,

            text=(
                f"Unable to load page\n"
                f"{error}"
            ),

            text_color="#f87171",

            justify="center"
        ).pack(
            pady=10
        )


        return frame


    # ========================================================
    # AI
    # ========================================================

    def open_ai(self):

        try:

            if not hasattr(
                self,
                "ai"
            ):

                from widgets.ai_chat import AIChat

                self.ai = AIChat(
                    self
                )


            self.ai.deiconify()

            self.ai.lift()

            self.ai.focus_force()


        except Exception as error:

            print(
                f"[AI ERROR] {error}"
            )


    # ========================================================
    # LANGUAGE RELOAD
    # ========================================================

    def reload_language(self):

        for name, page in self.pages.items():

            reload_page = getattr(
                page,
                "reload_language",
                None
            )

            if callable(
                reload_page
            ):

                try:

                    reload_page()

                except Exception as error:

                    print(
                        f"[LANG RELOAD ERROR] "
                        f"{name}: {error}"
                    )


    # ========================================================
    # CLOSE
    # ========================================================

    def on_close(self):

        print(
            "[CRYTOPZ] Shutting down..."
        )


        # ----------------------------------------------------
        # STOP LIVE MARKET FIRST
        # ----------------------------------------------------

        self.stop_live_market()


        # ----------------------------------------------------
        # STOP BOT RUNTIME
        # ----------------------------------------------------

        bots_page = self.pages.get(
            "Bots"
        )


        if bots_page is not None:

            runtime = getattr(
                bots_page,
                "runtime",
                None
            )


            if runtime is not None:

                stop_all = getattr(
                    runtime,
                    "stop_all",
                    None
                )


                if callable(
                    stop_all
                ):

                    try:

                        stop_all()

                    except Exception as error:

                        print(
                            f"[BOT STOP ERROR] "
                            f"{error}"
                        )


            stop_all = getattr(
                bots_page,
                "stop_all",
                None
            )


            if callable(
                stop_all
            ):

                try:

                    stop_all()

                except Exception as error:

                    print(
                        f"[BOT PAGE STOP ERROR] "
                        f"{error}"
                    )


        # ----------------------------------------------------
        # CLOSE AI
        # ----------------------------------------------------

        ai = getattr(
            self,
            "ai",
            None
        )


        if ai is not None:

            try:

                ai.destroy()

            except Exception:

                pass


        # ----------------------------------------------------
        # CLOSE ENGINE
        # ----------------------------------------------------

        engine = getattr(
            self,
            "engine",
            None
        )


        if engine is not None:

            close = getattr(
                engine,
                "close",
                None
            )


            if callable(
                close
            ):

                try:

                    close()

                except Exception as error:

                    print(
                        f"[ENGINE CLOSE ERROR] "
                        f"{error}"
                    )


        # ----------------------------------------------------
        # DESTROY APPLICATION
        # ----------------------------------------------------

        self.destroy()


# ============================================================
# START APPLICATION
# ============================================================

def main():

    ctk.set_appearance_mode(
        "dark"
    )

    ctk.set_default_color_theme(
        "blue"
    )


    app = Crytopz()

    app.mainloop()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()

