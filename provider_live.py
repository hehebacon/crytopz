from __future__ import annotations

import json
import threading
import time
from typing import Any, Optional
from urllib.parse import quote
from urllib.request import Request, urlopen


class MarketDataProvider:
    # Read-only external market-data layer.
    # Crypto: Binance public ticker.
    # Stocks/ETFs/FX/indices: Yahoo Finance chart endpoint.
    # Paper execution remains inside the local Crytopz engine.

    CACHE_TTL = 5.0
    REQUEST_TIMEOUT = 5.0

    BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
    YAHOO_URL = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        "{symbol}?range=1d&interval=1m"
    )

    def __init__(self, engine: Any = None):
        self.engine = engine
        self._prices: dict[str, float] = {}
        self._changes: dict[str, float] = {}
        self._timestamps: dict[str, float] = {}
        self._lock = threading.RLock()
        self._refreshing: set[str] = set()

    def set_engine(self, engine: Any) -> None:
        self.engine = engine

    @staticmethod
    def _is_crypto(symbol: str) -> bool:
        return symbol.upper().endswith("USDT")

    @staticmethod
    def _provider_symbol(symbol: str) -> str:
        mapping = {
            "7203": "7203.T",
            "0700": "0700.HK",
            "SHEL": "SHEL.L",
            "EURUSD": "EURUSD=X",
            "GBPUSD": "GBPUSD=X",
            "USDJPY": "JPY=X",
            "AUDUSD": "AUDUSD=X",
            "USDCAD": "CAD=X",
            "USDCHF": "CHF=X",
            "NZDUSD": "NZDUSD=X",
            "SPX": "^GSPC",
            "NDX": "^NDX",
            "DJI": "^DJI",
            "RUT": "^RUT",
        }
        return mapping.get(
            symbol.strip().upper(),
            symbol.strip().upper(),
        )

    def get_price(self, symbol: str) -> Optional[float]:
        symbol = symbol.strip().upper()
        if not symbol:
            return None

        now = time.time()

        with self._lock:
            cached = self._prices.get(symbol)
            updated = self._timestamps.get(symbol, 0.0)

        if cached is not None and now - updated <= self.CACHE_TTL:
            return cached

        if cached is not None:
            self._start_refresh(symbol)
            return cached

        value = self._fetch_external(symbol)
        if value is not None:
            return value

        return self._engine_price(symbol)

    def set_price(self, symbol: str, price: float) -> None:
        symbol = symbol.strip().upper()
        with self._lock:
            self._prices[symbol] = float(price)
            self._timestamps[symbol] = time.time()

    def prefetch(self, symbols: list[str]) -> None:
        for symbol in symbols:
            self._start_refresh(
                str(symbol).strip().upper()
            )

    def _fetch_external(self, symbol: str) -> Optional[float]:
        try:
            if self._is_crypto(symbol):
                return self._fetch_binance(symbol)
            return self._fetch_yahoo(symbol)
        except Exception:
            return None

    def _fetch_binance(self, symbol: str) -> Optional[float]:
        url = f"{self.BINANCE_URL}?symbol={quote(symbol)}"

        request = Request(
            url,
            headers={
                "User-Agent": "Crytopz/1.0",
                "Accept": "application/json",
            },
        )

        with urlopen(
            request,
            timeout=self.REQUEST_TIMEOUT,
        ) as response:
            payload = json.loads(
                response.read().decode("utf-8")
            )

        value = float(payload["price"])
        self.set_price(symbol, value)
        return value

    def _fetch_yahoo(self, symbol: str) -> Optional[float]:
        provider_symbol = self._provider_symbol(symbol)

        url = self.YAHOO_URL.format(
            symbol=quote(
                provider_symbol,
                safe="",
            )
        )

        request = Request(
            url,
            headers={
                "User-Agent": "Crytopz/1.0",
                "Accept": "application/json",
            },
        )

        with urlopen(
            request,
            timeout=self.REQUEST_TIMEOUT,
        ) as response:
            payload = json.loads(
                response.read().decode("utf-8")
            )

        result = (
            payload.get("chart", {})
            .get("result")
        )

        if not result:
            return None

        meta = result[0].get("meta", {})

        value = (
            meta.get("regularMarketPrice")
            or meta.get("previousClose")
        )

        if value is None:
            return None

        value = float(value)
        self.set_price(symbol, value)

        previous_close = meta.get("previousClose")
        if previous_close:
            self.set_change_24h(
                symbol,
                (
                    (value - float(previous_close))
                    / float(previous_close)
                    * 100.0
                ),
            )

        return value

    def _start_refresh(self, symbol: str) -> None:
        with self._lock:
            if symbol in self._refreshing:
                return
            self._refreshing.add(symbol)

        threading.Thread(
            target=self._refresh_worker,
            args=(symbol,),
            daemon=True,
        ).start()

    def _refresh_worker(self, symbol: str) -> None:
        try:
            self._fetch_external(symbol)
        finally:
            with self._lock:
                self._refreshing.discard(symbol)

    def _engine_price(self, symbol: str) -> Optional[float]:
        if self.engine is None:
            return None

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
                    with self._lock:
                        self._prices[symbol] = value
                        self._timestamps[symbol] = time.time()
                    return value
        except Exception:
            pass

        return None

    def get_change_24h(
        self,
        symbol: str,
    ) -> Optional[float]:
        with self._lock:
            return self._changes.get(
                symbol.strip().upper()
            )

    def set_change_24h(
        self,
        symbol: str,
        change: float,
    ) -> None:
        with self._lock:
            self._changes[
                symbol.strip().upper()
            ] = float(change)

    def get_snapshot(self, symbol: str) -> dict:
        symbol = symbol.strip().upper()
        return {
            "symbol": symbol,
            "price": self.get_price(symbol),
            "change_24h": self.get_change_24h(symbol),
            "source": (
                "external"
                if symbol in self._timestamps
                else "engine"
            ),
        }

    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, Optional[float]]:
        return {
            symbol: self.get_price(symbol)
            for symbol in symbols
        }
