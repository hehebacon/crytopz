from __future__ import annotations

import random
import time
import threading


class MockMarketFeed:
    """
    Paper-mode market data generator.

    Generates a lightweight random-walk + trend price stream
    and sends every tick into CrytopzAPI.update_market().
    """

    def __init__(
        self,
        engine,
        interval_ms: int = 500,
    ):
        self.engine = engine
        self.interval_ms = max(100, int(interval_ms))

        self.running = False
        self._after_id = None

        # ----------------------------------------------------
        # Initial prices
        # ----------------------------------------------------

        self.prices = {
            "BTCUSDT": 100000.0,
            "ETHUSDT": 4000.0,
            "SOLUSDT": 200.0,
            "BNBUSDT": 700.0,
            "XRPUSDT": 2.5,
        }

        # ----------------------------------------------------
        # Volatility
        # ----------------------------------------------------

        self.volatility = {
            "BTCUSDT": 0.0010,
            "ETHUSDT": 0.0015,
            "SOLUSDT": 0.0025,
            "BNBUSDT": 0.0015,
            "XRPUSDT": 0.0030,
        }

        # Small directional trend.
        self.trend = {
            symbol: 0.0
            for symbol in self.prices
        }

        # ----------------------------------------------------
        # Seed initial market state
        # ----------------------------------------------------

        self._seed_market()

    # ========================================================
    # SEED
    # ========================================================

    def _seed_market(self):

        timestamp = int(
            time.time() * 1000
        )

        for symbol, price in self.prices.items():

            spread = price * 0.0001

            bid = price - spread
            ask = price + spread
            last = price

            try:

                self.engine.update_market(
                    symbol,
                    bid,
                    ask,
                    last,
                    timestamp,
                )

            except Exception as error:

                print(
                    f"[MARKET FEED] "
                    f"Seed failed for {symbol}: {error}"
                )

    # ========================================================
    # START
    # ========================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self._schedule_next()

        print(
            "[MARKET FEED] Started"
        )

    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        self.running = False

        if self._after_id is not None:

            try:
                self.engine.after_cancel(
                    self._after_id
                )
            except Exception:
                pass

            self._after_id = None

        print(
            "[MARKET FEED] Stopped"
        )

    # ========================================================
    # SCHEDULE
    # ========================================================

    def _schedule_next(self):

        if not self.running:
            return

        try:

            self._after_id = self.engine.after(
                self.interval_ms,
                self._tick
            )

        except Exception as error:

            self.running = False

            print(
                f"[MARKET FEED] "
                f"Schedule error: {error}"
            )

    # ========================================================
    # TICK
    # ========================================================

    def _tick(self):

        self._after_id = None

        if not self.running:
            return

        timestamp = int(
            time.time() * 1000
        )

        for symbol in self.prices:

            self._update_symbol(
                symbol,
                timestamp
            )

        self._schedule_next()

    # ========================================================
    # SYMBOL UPDATE
    # ========================================================

    def _update_symbol(
        self,
        symbol: str,
        timestamp: int,
    ):

        old_price = self.prices[
            symbol
        ]

        volatility = self.volatility[
            symbol
        ]

        # ----------------------------------------------------
        # Random movement
        # ----------------------------------------------------

        random_move = random.gauss(
            0.0,
            volatility
        )

        # ----------------------------------------------------
        # Slowly changing trend
        # ----------------------------------------------------

        self.trend[symbol] += random.gauss(
            0.0,
            volatility * 0.08
        )

        self.trend[symbol] = max(
            -volatility * 0.5,
            min(
                volatility * 0.5,
                self.trend[symbol]
            )
        )

        movement = (
            random_move
            + self.trend[symbol]
        )

        new_price = (
            old_price
            * (1.0 + movement)
        )

        if new_price <= 0:
            new_price = old_price

        self.prices[
            symbol
        ] = new_price

        # ----------------------------------------------------
        # Spread
        # ----------------------------------------------------

        spread = (
            new_price
            * 0.0001
        )

        bid = new_price - spread
        ask = new_price + spread
        last = new_price

        # ----------------------------------------------------
        # Push into C++ Core
        # ----------------------------------------------------

        try:

            self.engine.update_market(
                symbol,
                bid,
                ask,
                last,
                timestamp,
            )

        except Exception as error:

            print(
                f"[MARKET FEED] "
                f"{symbol}: {error}"
            )