from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Instrument:
    """
    Describes a tradable market instrument.

    This class contains metadata only.
    Price/volume data belongs to MarketDataProvider.
    """

    symbol: str
    name: str

    asset_type: str
    exchange: str

    country: str
    currency: str

    description: str = ""

    # Optional provider-specific identifier.
    provider_symbol: Optional[str] = None

    @property
    def display_symbol(self) -> str:
        return self.symbol

    @property
    def display_name(self) -> str:
        return self.name

    @property
    def search_text(self) -> str:
        """
        Normalized text used by Markets search.
        """
        return " ".join(
            [
                self.symbol,
                self.name,
                self.asset_type,
                self.exchange,
                self.country,
                self.currency,
            ]
        ).upper()

    @property
    def is_stock(self) -> bool:
        return self.asset_type.upper() == "STOCK"

    @property
    def is_crypto(self) -> bool:
        return self.asset_type.upper() == "CRYPTO"

    @property
    def is_etf(self) -> bool:
        return self.asset_type.upper() == "ETF"

    @property
    def is_forex(self) -> bool:
        return self.asset_type.upper() == "FOREX"

    @property
    def is_index(self) -> bool:
        return self.asset_type.upper() == "INDEX"

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "asset_type": self.asset_type,
            "exchange": self.exchange,
            "country": self.country,
            "currency": self.currency,
            "description": self.description,
            "provider_symbol": self.provider_symbol,
        }