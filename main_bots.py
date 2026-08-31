import os
import sys
from pathlib import Path

# =========================================================
# PROJECT ROOT
# =========================================================

ROOT = Path(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# =========================================================
# UI
# =========================================================

import customtkinter as ctk

from theme import ThemeManager

from pages.paper_engine import PaperTradingEngine
from pages.trade import TradePage
from pages.home import HomePage
from pages.markets import MarketsPage
from pages.learn import LearnPage
from pages.portfolio import PortfolioPage
from pages.settings import SettingsPage
from pages.bots import BotLibraryPage


# =========================================================
# BOT SYSTEM
# =========================================================

from bot_system.manager import BotManager


# =========================================================
# APPLICATION
# =========================================================

class Crytopz(ctk.CTk):

    def __init__(self):
        super().__init__()

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        self.title("crytopz")

        self.geometry(
            "1400x850"
        )

        self.minsize(
            1100,
            700
        )

        # -------------------------------------------------
        # THEME
        # -------------------------------------------------

        self.theme = ThemeManager()

        # -------------------------------------------------
        # PAPER ENGINE
        # -------------------------------------------------

        self.engine = PaperTradingEngine(
            initial_balance=10_000.0
        )

        # -------------------------------------------------
        # BOT SYSTEM
        # -------------------------------------------------

        self.bot_manager = BotManager(
            bots_directory=ROOT / "bots",
            core=self.engine
        )

        # -------------------------------------------------
        # PAGES
        # -------------------------------------------------

        self.pages = {}

        # -------------------------------------------------
        # UI
        # -------------------------------------------------

        self.build_navbar()

        self.build_content()

        self.show_page(
            "Home"
        )

        # -------------------------------------------------
        # CLOSE
        # -------------------------------------------------

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )


    # =====================================================
    # NAVBAR
    # =====================================================

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


        # -------------------------------------------------
        # LOGO
        # -------------------------------------------------

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


        # -------------------------------------------------
        # NAVIGATION
        # -------------------------------------------------

        pages = [
            "Home",
            "Markets",
            "Trade",
            "Bots",
            "Learn",
            "Portfolio",
            "Settings"
        ]

        for name in pages:

            ctk.CTkButton(
                self.navbar,
                text=name,
                width=82 if name == "Bots" else 90,
                height=38,
                fg_color="transparent",
                hover_color="#202020",
                command=lambda n=name:
                    self.show_page(n)
            ).pack(
                side="left",
                padx=2
            )


        # -------------------------------------------------
        # AI
        # -------------------------------------------------

        ctk.CTkButton(
            self.navbar,
            text="✦ AI",
            width=70,
            height=38,
            command=self.open_ai
        ).pack(
            side="right",
            padx=15
        )


        # -------------------------------------------------
        # PAPER STATUS
        # -------------------------------------------------

        ctk.CTkLabel(
            self.navbar,
            text="● PAPER",
            text_color="#4ade80",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            side="right",
            padx=10
        )


    # =====================================================
    # CONTENT
    # =====================================================

    def build_content(self):

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.pack(
            fill="both",
            expand=True
        )


    # =====================================================
    # SHOW PAGE
    # =====================================================

    def show_page(self, name):

        # Hide current pages

        for page in self.pages.values():

            page.pack_forget()


        # Create page if necessary

        if name not in self.pages:

            self.pages[name] = (
                self.create_page(name)
            )


        # Get page

        page = self.pages[name]


        # Show page

        page.pack(
            fill="both",
            expand=True
        )


        # Refresh

        if hasattr(
            page,
            "refresh"
        ):

            try:

                page.refresh()

            except Exception as error:

                print(
                    f"[UI] Page refresh error: "
                    f"{error}"
                )


    # =====================================================
    # CREATE PAGE
    # =====================================================

    def create_page(self, name):

        page_class = {

            "Home":
                HomePage,

            "Markets":
                MarketsPage,

            "Trade":
                TradePage,

            "Bots":
                BotLibraryPage,

            "Learn":
                LearnPage,

            "Portfolio":
                PortfolioPage,

            "Settings":
                SettingsPage

        }.get(
            name
        )


        # Unknown page

        if page_class is None:

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
                pady=100
            )

            return frame


        return page_class(
            self.content,
            self
        )


    # =====================================================
    # AI
    # =====================================================

    def open_ai(self):

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


    # =====================================================
    # CLOSE
    # =====================================================

    def on_close(self):

        # Stop all bots first

        try:

            if self.bot_manager:

                self.bot_manager.stop_all()

        except Exception as error:

            print(
                f"[Crytopz] Bot shutdown error: "
                f"{error}"
            )


        self.destroy()


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    ctk.set_appearance_mode(
        "dark"
    )

    ctk.set_default_color_theme(
        "blue"
    )

    app = Crytopz()

    app.mainloop()