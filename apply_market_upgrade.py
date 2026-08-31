from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
MD = ROOT / "python" / "market_data"

TRADE = PAGES / "trade.py"
MARKETS = PAGES / "markets.py"
REGISTRY = MD / "registry.py"
PROVIDER = MD / "provider.py"

LIVE_PROVIDER = ROOT / "provider_live.py"
EXTRA_FILE = ROOT / "registry_extra.txt"

for path in (TRADE, MARKETS, REGISTRY, PROVIDER, LIVE_PROVIDER, EXTRA_FILE):
    if not path.exists():
        raise FileNotFoundError(path)

# Backups
for path in (TRADE, MARKETS, REGISTRY, PROVIDER):
    backup = path.with_suffix(path.suffix + ".market_backup")
    if not backup.exists():
        shutil.copy2(path, backup)

# Provider
shutil.copy2(LIVE_PROVIDER, PROVIDER)

# Registry
registry = REGISTRY.read_text(encoding="utf-8")
extra = EXTRA_FILE.read_text(encoding="utf-8")
marker = "        self.register_many(instruments)\n"

if extra.strip() not in registry:
    if marker not in registry:
        raise RuntimeError("Registry insertion point not found.")
    registry = registry.replace(
        marker,
        marker + extra,
        1,
    )
REGISTRY.write_text(registry, encoding="utf-8")

# Trade
trade = TRADE.read_text(encoding="utf-8")

if "from market_data import (" not in trade:
    trade = trade.replace(
        "import customtkinter as ctk\n",
        """import customtkinter as ctk

from market_data import (
    InstrumentRegistry,
    MarketDataProvider,
)
""",
        1,
    )

if "self.instrument_registry = InstrumentRegistry()" not in trade:
    trade = trade.replace(
        "        self.destroyed = False\n",
        """        self.destroyed = False

        # ========================================================
        # MARKET DATA
        # ========================================================
        self.instrument_registry = InstrumentRegistry()
        self.market_data = MarketDataProvider(
            getattr(self.app, "engine", None)
        )
""",
        1,
    )

old_symbols = """        symbols = getattr(
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
"""

new_symbols = """        # Shared asset universe used by Trade and Markets.
        symbols = [
            instrument.symbol
            for instrument in self.instrument_registry.search(
                query="",
                asset_type=None,
            )
        ]

        if self.symbol not in symbols:
            symbols.insert(
                0,
                self.symbol,
            )

        self.symbol_menu = ctk.CTkOptionMenu(
"""

if old_symbols in trade:
    trade = trade.replace(old_symbols, new_symbols, 1)

old_current = """    def current_price(self):
        try:
            return float(
                self.engine().get_price(
                    self.symbol
                )
            )
        except Exception:
            return 0.0
"""

new_current = """    def current_price(self):
        try:
            price = self.market_data.get_price(
                self.symbol
            )
            if price is not None:
                return float(price)
        except Exception:
            pass

        try:
            return float(
                self.engine().get_price(
                    self.symbol
                )
            )
        except Exception:
            return 0.0
"""

if old_current in trade:
    trade = trade.replace(old_current, new_current, 1)

old_refresh = """            price = float(
                engine.get_price(
                    self.symbol
                )
            )
"""

new_refresh = """            price = self.market_data.get_price(
                self.symbol
            )

            if price is None:
                price = float(
                    engine.get_price(
                        self.symbol
                    )
                )

            price = float(price)
"""

if old_refresh in trade:
    trade = trade.replace(old_refresh, new_refresh, 1)

TRADE.write_text(trade, encoding="utf-8")

# Markets: warm the external cache without blocking the UI.
markets = MARKETS.read_text(encoding="utf-8")

old_load = """            self.all_instruments = list(
                instruments
            )

        except Exception as exc:
"""

new_load = """            self.all_instruments = list(
                instruments
            )

            self.provider.prefetch(
                [
                    instrument.symbol
                    for instrument in self.all_instruments
                ]
            )

        except Exception as exc:
"""

if old_load in markets and "self.provider.prefetch(" not in markets:
    markets = markets.replace(old_load, new_load, 1)

MARKETS.write_text(markets, encoding="utf-8")

print("CRYTOPZ MARKET UPGRADE COMPLETE")
print("Updated Trade + Markets + Registry + Provider.")
print("Backups created as *.market_backup")
