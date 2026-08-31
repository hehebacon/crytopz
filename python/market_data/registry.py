from __future__ import annotations

from typing import Iterable, Optional

from .instrument import Instrument


class InstrumentRegistry:
    """
    Registry containing all known Crytopz instruments.

    The registry is intentionally independent from prices.

    Later this can be populated from:
        - exchange listings
        - market-data providers
        - local database
        - Crytopz backend
    """

    def __init__(self):
        self._instruments: dict[str, Instrument] = {}

        self._load_builtin_instruments()

    # ============================================================
    # REGISTER
    # ============================================================

    def register(self, instrument: Instrument) -> None:
        """
        Add or replace an instrument.
        """

        symbol = instrument.symbol.strip().upper()

        if not symbol:
            raise ValueError("Instrument symbol cannot be empty.")

        self._instruments[symbol] = Instrument(
            symbol=symbol,
            name=instrument.name,
            asset_type=instrument.asset_type.upper(),
            exchange=instrument.exchange.upper(),
            country=instrument.country.upper(),
            currency=instrument.currency.upper(),
            description=instrument.description,
            provider_symbol=instrument.provider_symbol,
        )

    def register_many(
        self,
        instruments: Iterable[Instrument],
    ) -> None:
        for instrument in instruments:
            self.register(instrument)

    # ============================================================
    # GET
    # ============================================================

    def get(self, symbol: str) -> Optional[Instrument]:
        if not symbol:
            return None

        return self._instruments.get(
            symbol.strip().upper()
        )

    def require(self, symbol: str) -> Instrument:
        instrument = self.get(symbol)

        if instrument is None:
            raise KeyError(
                f"Unknown instrument: {symbol}"
            )

        return instrument

    # ============================================================
    # LIST
    # ============================================================

    def all(self) -> list[Instrument]:
        return list(self._instruments.values())

    def count(self) -> int:
        return len(self._instruments)

    def symbols(self) -> list[str]:
        return list(self._instruments.keys())

    # ============================================================
    # FILTER
    # ============================================================

    def by_type(
        self,
        asset_type: str,
    ) -> list[Instrument]:

        asset_type = asset_type.strip().upper()

        return [
            instrument
            for instrument in self._instruments.values()
            if instrument.asset_type.upper() == asset_type
        ]

    def by_exchange(
        self,
        exchange: str,
    ) -> list[Instrument]:

        exchange = exchange.strip().upper()

        return [
            instrument
            for instrument in self._instruments.values()
            if instrument.exchange.upper() == exchange
        ]

    def by_country(
        self,
        country: str,
    ) -> list[Instrument]:

        country = country.strip().upper()

        return [
            instrument
            for instrument in self._instruments.values()
            if instrument.country.upper() == country
        ]

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        query: str = "",
        asset_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[Instrument]:

        query = (query or "").strip().upper()

        if asset_type:
            asset_type = asset_type.strip().upper()

        results: list[Instrument] = []

        for instrument in self._instruments.values():

            if asset_type:
                if instrument.asset_type.upper() != asset_type:
                    continue

            if query:
                if query not in instrument.search_text:
                    continue

            results.append(instrument)

        # Better UX:
        # exact symbol matches first.
        if query:

            def sort_key(item: Instrument):
                symbol = item.symbol.upper()

                if symbol == query:
                    priority = 0
                elif symbol.startswith(query):
                    priority = 1
                elif query in symbol:
                    priority = 2
                else:
                    priority = 3

                return priority, symbol

            results.sort(key=sort_key)

        else:
            results.sort(
                key=lambda item: item.symbol
            )

        if limit is not None:
            return results[:max(0, limit)]

        return results

    # ============================================================
    # BUILT-IN UNIVERSE
    # ============================================================

    def _load_builtin_instruments(self) -> None:
        """
        Starter universe.

        This is NOT intended to represent every global security.
        It gives the application a useful initial universe until
        a real market-data universe provider is connected.
        """

        instruments = [

            # ----------------------------------------------------
            # US STOCKS
            # ----------------------------------------------------

            Instrument(
                symbol="AAPL",
                name="Apple Inc.",
                asset_type="STOCK",
                exchange="NASDAQ",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="MSFT",
                name="Microsoft Corporation",
                asset_type="STOCK",
                exchange="NASDAQ",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="NVDA",
                name="NVIDIA Corporation",
                asset_type="STOCK",
                exchange="NASDAQ",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="AMZN",
                name="Amazon.com Inc.",
                asset_type="STOCK",
                exchange="NASDAQ",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="GOOGL",
                name="Alphabet Inc.",
                asset_type="STOCK",
                exchange="NASDAQ",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="META",
                name="Meta Platforms Inc.",
                asset_type="STOCK",
                exchange="NASDAQ",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="TSLA",
                name="Tesla Inc.",
                asset_type="STOCK",
                exchange="NASDAQ",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="BRK.B",
                name="Berkshire Hathaway Inc.",
                asset_type="STOCK",
                exchange="NYSE",
                country="US",
                currency="USD",
            ),

            # ----------------------------------------------------
            # ETF
            # ----------------------------------------------------

            Instrument(
                symbol="SPY",
                name="SPDR S&P 500 ETF Trust",
                asset_type="ETF",
                exchange="NYSE",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="QQQ",
                name="Invesco QQQ Trust",
                asset_type="ETF",
                exchange="NASDAQ",
                country="US",
                currency="USD",
            ),

            # ----------------------------------------------------
            # JAPAN
            # ----------------------------------------------------

            Instrument(
                symbol="7203",
                name="Toyota Motor Corporation",
                asset_type="STOCK",
                exchange="TSE",
                country="JP",
                currency="JPY",
            ),

            # ----------------------------------------------------
            # HONG KONG
            # ----------------------------------------------------

            Instrument(
                symbol="0700",
                name="Tencent Holdings",
                asset_type="STOCK",
                exchange="HKEX",
                country="HK",
                currency="HKD",
            ),

            # ----------------------------------------------------
            # UK
            # ----------------------------------------------------

            Instrument(
                symbol="SHEL",
                name="Shell plc",
                asset_type="STOCK",
                exchange="LSE",
                country="GB",
                currency="GBP",
            ),

            # ----------------------------------------------------
            # CRYPTO
            # ----------------------------------------------------

            Instrument(
                symbol="BTCUSDT",
                name="Bitcoin / Tether",
                asset_type="CRYPTO",
                exchange="CRYPTO",
                country="GLOBAL",
                currency="USDT",
            ),

            Instrument(
                symbol="ETHUSDT",
                name="Ethereum / Tether",
                asset_type="CRYPTO",
                exchange="CRYPTO",
                country="GLOBAL",
                currency="USDT",
            ),

            Instrument(
                symbol="SOLUSDT",
                name="Solana / Tether",
                asset_type="CRYPTO",
                exchange="CRYPTO",
                country="GLOBAL",
                currency="USDT",
            ),

            Instrument(
                symbol="BNBUSDT",
                name="BNB / Tether",
                asset_type="CRYPTO",
                exchange="CRYPTO",
                country="GLOBAL",
                currency="USDT",
            ),

            Instrument(
                symbol="XRPUSDT",
                name="XRP / Tether",
                asset_type="CRYPTO",
                exchange="CRYPTO",
                country="GLOBAL",
                currency="USDT",
            ),

            Instrument(
                symbol="ADAUSDT",
                name="Cardano / Tether",
                asset_type="CRYPTO",
                exchange="CRYPTO",
                country="GLOBAL",
                currency="USDT",
            ),

            # ----------------------------------------------------
            # FOREX
            # ----------------------------------------------------

            Instrument(
                symbol="EURUSD",
                name="Euro / US Dollar",
                asset_type="FOREX",
                exchange="FX",
                country="GLOBAL",
                currency="USD",
            ),

            Instrument(
                symbol="GBPUSD",
                name="British Pound / US Dollar",
                asset_type="FOREX",
                exchange="FX",
                country="GLOBAL",
                currency="USD",
            ),

            Instrument(
                symbol="USDJPY",
                name="US Dollar / Japanese Yen",
                asset_type="FOREX",
                exchange="FX",
                country="GLOBAL",
                currency="JPY",
            ),

            # ----------------------------------------------------
            # INDEX
            # ----------------------------------------------------

            Instrument(
                symbol="SPX",
                name="S&P 500 Index",
                asset_type="INDEX",
                exchange="INDEX",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="NDX",
                name="Nasdaq-100 Index",
                asset_type="INDEX",
                exchange="INDEX",
                country="US",
                currency="USD",
            ),

            Instrument(
                symbol="DJI",
                name="Dow Jones Industrial Average",
                asset_type="INDEX",
                exchange="INDEX",
                country="US",
                currency="USD",
            ),
        ]

        self.register_many(instruments)