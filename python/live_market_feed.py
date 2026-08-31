
from __future__ import annotations

import json
import os
import threading
import time
from typing import Callable, Iterable
from urllib.parse import quote

try:
    import websocket
except ImportError:
    websocket = None


class LiveMarketFeed:
    """
    Live market-data feed.

    Architecture:

        WebSocket
            ↓
        LiveMarketFeed
            ↓
        engine.update_market()
            ↓
        C++ Core
            ↓
        Markets / Trade

    The WebSocket runs in a background thread so it does NOT
    block the CustomTkinter UI thread.
    """

    WS_BASE_URL = (
        "wss://ws.twelvedata.com/"
        "v1/quotes/price"
    )

    def __init__(
        self,
        engine,
        symbols: Iterable[str] | None = None,
        api_key: str | None = None,
        on_price: Callable | None = None,
    ):
        self.engine = engine

        self.api_key = (
            api_key
            or os.getenv("CRYPTOPZ_MARKET_API_KEY")
            or ""
        ).strip()

        self.symbols = self._normalize_symbols(
            symbols
        )

        self.on_price = on_price

        self.running = False

        self._ws = None
        self._thread = None

        # --------------------------------------------------------
        # Thread-safe latest-price cache.
        # --------------------------------------------------------

        self._lock = threading.RLock()

        self.prices: dict[str, float] = {}

        self.timestamps: dict[str, int] = {}

        self.bids: dict[str, float] = {}

        self.asks: dict[str, float] = {}

    # ============================================================
    # SYMBOLS
    # ============================================================

    @staticmethod
    def _normalize_symbol(
        symbol: str,
    ) -> str:

        symbol = str(
            symbol
        ).strip().upper()

        # Twelve Data commonly represents crypto as BTC/USD.
        #
        # Keep normal stock symbols untouched.

        if symbol.endswith("USDT"):

            return (
                f"{symbol[:-4]}/USD"
            )

        return symbol

    # ============================================================

    @classmethod
    def _normalize_symbols(
        cls,
        symbols: Iterable[str] | None,
    ) -> list[str]:

        if symbols is None:
            return []

        result = []

        seen = set()

        for symbol in symbols:

            normalized = cls._normalize_symbol(
                symbol
            )

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(
                normalized
            )

            result.append(
                normalized
            )

        return result

    # ============================================================
    # START
    # ============================================================

    def start(self):

        if self.running:
            return

        if not self.api_key:

            print(
                "[LIVE MARKET FEED] "
                "Missing API key."
            )

            return

        if not self.symbols:

            print(
                "[LIVE MARKET FEED] "
                "No symbols subscribed."
            )

            return

        if websocket is None:

            print(
                "[LIVE MARKET FEED] "
                "Missing websocket-client package."
            )

            return

        self.running = True

        self._thread = threading.Thread(
            target=self._run,
            name="Crytopz-LiveMarketFeed",
            daemon=True,
        )

        self._thread.start()

        print(
            "[LIVE MARKET FEED] Starting..."
        )

    # ============================================================
    # STOP
    # ============================================================

    def stop(self):

        self.running = False

        ws = self._ws

        if ws is not None:

            try:
                ws.close()
            except Exception:
                pass

        self._ws = None

        print(
            "[LIVE MARKET FEED] Stopped"
        )

    # ============================================================
    # ADD SYMBOLS
    # ============================================================

    def set_symbols(
        self,
        symbols: Iterable[str],
    ):

        new_symbols = (
            self._normalize_symbols(
                symbols
            )
        )

        self.symbols = new_symbols

        # If already running, reconnect so the
        # new subscription takes effect.

        if self.running:

            self._restart_connection()

    # ============================================================
    # RESTART CONNECTION
    # ============================================================

    def _restart_connection(self):

        ws = self._ws

        if ws is not None:

            try:
                ws.close()
            except Exception:
                pass

    # ============================================================
    # RUN
    # ============================================================

    def _run(self):

        while self.running:

            try:

                url = (
                    f"{self.WS_BASE_URL}"
                    f"?apikey={quote(self.api_key)}"
                )

                print(
                    "[LIVE MARKET FEED] "
                    "Connecting..."
                )

                ws_app = websocket.WebSocketApp(
                    url,
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close,
                )

                self._ws = ws_app

                # ping_interval keeps the connection alive.
                ws_app.run_forever(
                    ping_interval=20,
                    ping_timeout=10,
                )

            except Exception as error:

                print(
                    "[LIVE MARKET FEED] "
                    f"Connection error: {error}"
                )

            finally:

                self._ws = None

            if not self.running:
                break

            # ----------------------------------------------------
            # Reconnect delay.
            # ----------------------------------------------------

            print(
                "[LIVE MARKET FEED] "
                "Reconnecting in 3 seconds..."
            )

            time.sleep(3)

    # ============================================================
    # OPEN
    # ============================================================

    def _on_open(
        self,
        ws,
    ):

        print(
            "[LIVE MARKET FEED] "
            "Connected."
        )

        payload = {
            "action": "subscribe",
            "params": {
                "symbols": ",".join(
                    self.symbols
                )
            },
        }

        try:

            ws.send(
                json.dumps(
                    payload
                )
            )

            print(
                "[LIVE MARKET FEED] "
                f"Subscribed: {len(self.symbols)} symbols"
            )

        except Exception as error:

            print(
                "[LIVE MARKET FEED] "
                f"Subscription error: {error}"
            )

    # ============================================================
    # MESSAGE
    # ============================================================

    def _on_message(
        self,
        ws,
        message,
    ):

        try:

            data = json.loads(
                message
            )

        except (
            ValueError,
            TypeError,
        ):

            return

        if not isinstance(
            data,
            dict,
        ):
            return

        # --------------------------------------------------------
        # Ignore non-price events.
        # --------------------------------------------------------

        event = str(
            data.get(
                "event",
                "",
            )
        ).lower()

        if event in {
            "heartbeat",
            "subscribe-status",
            "subscription",
        }:
            return

        # --------------------------------------------------------
        # Extract symbol.
        # --------------------------------------------------------

        symbol = (
            data.get("symbol")
            or data.get("code")
        )

        if not symbol:
            return

        symbol = str(
            symbol
        ).upper()

        # --------------------------------------------------------
        # Extract price.
        # --------------------------------------------------------

        raw_price = (
            data.get("price")
            or data.get("close")
            or data.get("last")
        )

        if raw_price is None:
            return

        try:

            price = float(
                raw_price
            )

        except (
            ValueError,
            TypeError,
        ):

            return

        if price <= 0:
            return

        # --------------------------------------------------------
        # Timestamp.
        # --------------------------------------------------------

        raw_timestamp = (
            data.get("timestamp")
            or int(
                time.time() * 1000
            )
        )

        try:

            timestamp = int(
                raw_timestamp
            )

        except (
            ValueError,
            TypeError,
        ):

            timestamp = int(
                time.time() * 1000
            )

        # --------------------------------------------------------
        # Bid / Ask.
        #
        # WebSocket quote stream may not provide both.
        # If unavailable, derive a tiny synthetic spread only
        # for the local Core representation.
        #
        # The LAST price itself remains the provider's price.
        # --------------------------------------------------------

        bid = self._safe_float(
            data.get("bid")
        )

        ask = self._safe_float(
            data.get("ask")
        )

        if bid is None:
            bid = price

        if ask is None:
            ask = price

        # --------------------------------------------------------
        # Cache.
        # --------------------------------------------------------

        with self._lock:

            self.prices[
                symbol
            ] = price

            self.timestamps[
                symbol
            ] = timestamp

            self.bids[
                symbol
            ] = bid

            self.asks[
                symbol
            ] = ask

        # --------------------------------------------------------
        # Push to C++ Core.
        #
        # IMPORTANT:
        # This callback is running on the WebSocket thread.
        # The Core bridge should therefore be thread-safe.
        # --------------------------------------------------------

        try:

            self.engine.update_market(
                symbol,
                bid,
                ask,
                price,
                timestamp,
            )

        except Exception as error:

            print(
                "[LIVE MARKET FEED] "
                f"Core update failed for "
                f"{symbol}: {error}"
            )

        # --------------------------------------------------------
        # Optional callback.
        # --------------------------------------------------------

        if self.on_price is not None:

            try:

                self.on_price(
                    symbol,
                    price,
                    timestamp,
                )

            except Exception as error:

                print(
                    "[LIVE MARKET FEED] "
                    f"Price callback error: {error}"
                )

    # ============================================================
    # ERROR
    # ============================================================

    def _on_error(
        self,
        ws,
        error,
    ):

        print(
            "[LIVE MARKET FEED] "
            f"WebSocket error: {error}"
        )

    # ============================================================
    # CLOSE
    # ============================================================

    def _on_close(
        self,
        ws,
        close_status_code,
        close_msg,
    ):

        print(
            "[LIVE MARKET FEED] "
            f"Disconnected "
            f"({close_status_code}: {close_msg})"
        )

    # ============================================================
    # GET PRICE
    # ============================================================

    def get_price(
        self,
        symbol: str,
    ):

        normalized = self._normalize_symbol(
            symbol
        )

        with self._lock:

            price = self.prices.get(
                normalized
            )

            if price is not None:
                return price

            # Also try the original symbol.
            return self.prices.get(
                str(symbol).upper()
            )

    # ============================================================
    # SNAPSHOT
    # ============================================================

    def get_snapshot(
        self,
        symbol: str,
    ) -> dict | None:

        normalized = self._normalize_symbol(
            symbol
        )

        with self._lock:

            if normalized not in self.prices:
                return None

            return {
                "symbol": normalized,
                "price": self.prices[
                    normalized
                ],
                "bid": self.bids.get(
                    normalized
                ),
                "ask": self.asks.get(
                    normalized
                ),
                "timestamp": self.timestamps.get(
                    normalized
                ),
            }

    # ============================================================
    # SAFE FLOAT
    # ============================================================

    @staticmethod
    def _safe_float(
        value,
    ):

        if value is None:
            return None

        try:

            return float(
                value
            )

        except (
            ValueError,
            TypeError,
        ):

            return None

