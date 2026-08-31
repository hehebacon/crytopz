from __future__ import annotations

from typing import Any, Optional


class MarketDataProvider:
    """
    Market data abstraction.

    Current mode:
        Crytopz Engine / Paper Trading

    Future modes:
        WebSocket provider
        REST provider
        Exchange feed
        Licensed market-data provider
    """

    def __init__(self, engine: Any = None):
        self.engine = engine

        # Optional local cache.
        self._prices: dict[str, float] = {}

        # Optional 24h change cache.
        self._changes: dict[str, float] = {}

    # ============================================================
    # ENGINE
    # ============================================================

    def set_engine(self, engine: Any) -> None:
        self.engine = engine

    # ============================================================
    # PRICE
    # ============================================================

    def get_price(
        self,
        symbol: str,
    ) -> Optional[float]:

        symbol = symbol.strip().upper()

        # --------------------------------------------------------
        # 1. Engine
        # --------------------------------------------------------

        if self.engine is not None:

            try:
                getter = getattr(
                    self.engine,
                    "get_price",
                    None,
                )

                if callable(getter):

                    value = getter(symbol)

                    if value is not None:
                        value = float(value)

                        self._prices[symbol] = value

                        return value

            except Exception:
                pass

        # --------------------------------------------------------
        # 2. Cached value
        # --------------------------------------------------------

        if symbol in self._prices:
            return self._prices[symbol]

        return None

    def set_price(
        self,
        symbol: str,
        price: float,
    ) -> None:

        symbol = symbol.strip().upper()

        self._prices[symbol] = float(price)

    # ============================================================
    # 24H CHANGE
    # ============================================================

    def get_change_24h(
        self,
        symbol: str,
    ) -> Optional[float]:

        symbol = symbol.strip().upper()

        if symbol in self._changes:
            return self._changes[symbol]

        return None

    def set_change_24h(
        self,
        symbol: str,
        change: float,
    ) -> None:

        symbol = symbol.strip().upper()

        self._changes[symbol] = float(change)

    # ============================================================
    # SNAPSHOT
    # ============================================================

    def get_snapshot(
        self,
        symbol: str,
    ) -> dict:

        price = self.get_price(symbol)
        change = self.get_change_24h(symbol)

        return {
            "symbol": symbol,
            "price": price,
            "change_24h": change,
        }

    # ============================================================
    # BATCH
    # ============================================================

    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, Optional[float]]:

        result = {}

        for symbol in symbols:
            result[symbol] = self.get_price(symbol)

        return result