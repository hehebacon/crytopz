
from __future__ import annotations

import ctypes
from pathlib import Path
from typing import Optional


# ============================================================
# PATHS
# ============================================================

PYTHON_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PYTHON_DIR.parent

# Common Crytopz DLL locations.
_DLL_CANDIDATES = [
    # Python directory
    PYTHON_DIR / "crytopz_bridge.dll",

    # Project root
    PROJECT_DIR / "crytopz_bridge.dll",

    # Single-config build
    PROJECT_DIR / "build" / "crytopz_bridge.dll",

    # Multi-config Visual Studio build
    PROJECT_DIR / "build" / "Release" / "crytopz_bridge.dll",
    PROJECT_DIR / "build" / "Debug" / "crytopz_bridge.dll",

    # Current CMake output location
    PROJECT_DIR / "build" / "bin" / "Release" / "crytopz_bridge.dll",
    PROJECT_DIR / "build" / "bin" / "Debug" / "crytopz_bridge.dll",
]


def _find_bridge_dll() -> Path:
    for dll_path in _DLL_CANDIDATES:
        if dll_path.exists():
            return dll_path.resolve()

    searched = "\n".join(
        f"  - {path}"
        for path in _DLL_CANDIDATES
    )

    raise FileNotFoundError(
        "Crytopz bridge DLL not found.\n\n"
        "Searched:\n"
        f"{searched}"
    )


BRIDGE_DLL = _find_bridge_dll()


# ============================================================
# DLL LOAD
# ============================================================

try:
    _bridge = ctypes.CDLL(str(BRIDGE_DLL))
except OSError as error:
    raise RuntimeError(
        "Failed to load Crytopz bridge DLL.\n"
        f"DLL: {BRIDGE_DLL}\n"
        f"Error: {error}"
    ) from error


# ============================================================
# TYPES
# ============================================================

HANDLE = ctypes.c_void_p
SYMBOL = ctypes.c_char_p

UINT64 = ctypes.c_uint64
DOUBLE = ctypes.c_double
INT = ctypes.c_int


# ============================================================
# DLL FUNCTION HELPER
# ============================================================

def _bind(
    name: str,
    argtypes: list,
    restype,
):
    """
    Bind one exported C function.

    Raises a clear error when Python is using an incompatible
    Crytopz bridge DLL.
    """

    try:
        function = getattr(_bridge, name)

    except AttributeError as error:
        raise RuntimeError(
            "Crytopz bridge is missing exported function:\n"
            f"  {name}\n\n"
            f"DLL: {BRIDGE_DLL}\n\n"
            "Rebuild crytopz_bridge before starting Crytopz."
        ) from error

    function.argtypes = argtypes
    function.restype = restype

    return function


# ============================================================
# CORE LIFETIME
# ============================================================

_crytopz_create = _bind(
    "crytopz_create",
    [DOUBLE],
    HANDLE,
)

_crytopz_destroy = _bind(
    "crytopz_destroy",
    [HANDLE],
    None,
)


# ============================================================
# MARKET
# ============================================================

_crytopz_update_market = _bind(
    "crytopz_update_market",
    [
        HANDLE,
        SYMBOL,
        DOUBLE,
        DOUBLE,
        DOUBLE,
        UINT64,
    ],
    None,
)

_crytopz_get_price = _bind(
    "crytopz_get_price",
    [
        HANDLE,
        SYMBOL,
    ],
    DOUBLE,
)


# ============================================================
# LIVE MARKET
# ============================================================

_crytopz_start_live_market = _bind(
    "crytopz_start_live_market",
    [HANDLE],
    INT,
)

_crytopz_stop_live_market = _bind(
    "crytopz_stop_live_market",
    [HANDLE],
    None,
)

_crytopz_live_market_running = _bind(
    "crytopz_live_market_running",
    [HANDLE],
    INT,
)

_crytopz_live_market_interval_ms = _bind(
    "crytopz_live_market_interval_ms",
    [HANDLE],
    UINT64,
)


# ============================================================
# TRADING
# ============================================================

_crytopz_buy = _bind(
    "crytopz_buy",
    [
        HANDLE,
        SYMBOL,
        DOUBLE,
    ],
    UINT64,
)

_crytopz_sell = _bind(
    "crytopz_sell",
    [
        HANDLE,
        SYMBOL,
        DOUBLE,
    ],
    UINT64,
)


# ============================================================
# ACCOUNT
# ============================================================

_crytopz_balance = _bind(
    "crytopz_balance",
    [HANDLE],
    DOUBLE,
)

_crytopz_position_quantity = _bind(
    "crytopz_position_quantity",
    [
        HANDLE,
        SYMBOL,
    ],
    DOUBLE,
)

_crytopz_position_average_price = _bind(
    "crytopz_position_average_price",
    [
        HANDLE,
        SYMBOL,
    ],
    DOUBLE,
)

_crytopz_realized_pnl = _bind(
    "crytopz_realized_pnl",
    [HANDLE],
    DOUBLE,
)


# ============================================================
# PORTFOLIO / FINANCIAL STATE
# ============================================================

_crytopz_unrealized_pnl = _bind(
    "crytopz_unrealized_pnl",
    [HANDLE],
    DOUBLE,
)

_crytopz_position_value = _bind(
    "crytopz_position_value",
    [HANDLE],
    DOUBLE,
)

_crytopz_equity = _bind(
    "crytopz_equity",
    [HANDLE],
    DOUBLE,
)

_crytopz_total_pnl = _bind(
    "crytopz_total_pnl",
    [HANDLE],
    DOUBLE,
)


# ============================================================
# ORDERS
# ============================================================

_crytopz_order_count = _bind(
    "crytopz_order_count",
    [HANDLE],
    UINT64,
)

_crytopz_order_id = _bind(
    "crytopz_order_id",
    [
        HANDLE,
        UINT64,
    ],
    UINT64,
)

_crytopz_order_symbol = _bind(
    "crytopz_order_symbol",
    [
        HANDLE,
        UINT64,
    ],
    SYMBOL,
)

_crytopz_order_side = _bind(
    "crytopz_order_side",
    [
        HANDLE,
        UINT64,
    ],
    INT,
)

_crytopz_order_type = _bind(
    "crytopz_order_type",
    [
        HANDLE,
        UINT64,
    ],
    INT,
)

_crytopz_order_price = _bind(
    "crytopz_order_price",
    [
        HANDLE,
        UINT64,
    ],
    DOUBLE,
)

_crytopz_order_quantity = _bind(
    "crytopz_order_quantity",
    [
        HANDLE,
        UINT64,
    ],
    DOUBLE,
)

_crytopz_order_status = _bind(
    "crytopz_order_status",
    [
        HANDLE,
        UINT64,
    ],
    INT,
)

_crytopz_order_timestamp = _bind(
    "crytopz_order_timestamp",
    [
        HANDLE,
        UINT64,
    ],
    UINT64,
)


# ============================================================
# API
# ============================================================

class CrytopzAPI:
    """
    Python adapter for the native Crytopz C++ Core.

    Python owns no financial state.

    C++ Core owns:
        - account balance
        - positions
        - orders
        - execution
        - realized PnL
        - unrealized PnL
        - position value
        - equity
        - total PnL
        - live market feed
        - live market scheduler

    Python only:
        - communicates with the native bridge
        - controls the live market lifecycle
        - converts native values
        - prepares UI-friendly dictionaries
    """

    # ========================================================
    # INIT
    # ========================================================

    def __init__(
        self,
        initial_balance: float = 10000.0,
    ):
        try:
            self.initial_balance = float(initial_balance)

        except (TypeError, ValueError) as error:
            raise ValueError(
                "initial_balance must be a valid number."
            ) from error

        if self.initial_balance < 0:
            raise ValueError(
                "initial_balance cannot be negative."
            )

        self._handle: Optional[HANDLE] = None

        # Frontend compatibility only.
        # Actual financial logic belongs to C++.
        self.fee_rate = 0.0001

        self.supported_symbols = [
            "BTCUSDT",
            "ETHUSDT",
            "SOLUSDT",
            "BNBUSDT",
            "XRPUSDT",
        ]

        self._create_core()

    # ========================================================
    # CORE
    # ========================================================

    def _create_core(self) -> None:
        if self._handle is not None:
            return

        handle = _crytopz_create(
            DOUBLE(self.initial_balance)
        )

        if not handle:
            raise RuntimeError(
                "Crytopz Core returned a null handle."
            )

        self._handle = handle

    def _require_handle(self) -> HANDLE:
        if self._handle is None:
            raise RuntimeError(
                "Crytopz Core is closed or unavailable."
            )

        return self._handle

    # ========================================================
    # LIFECYCLE
    # ========================================================

    def close(self) -> None:
        """
        Stop live market before destroying the C++ Core.
        """

        handle = self._handle

        if handle is None:
            return

        try:
            # Scheduler must stop before Core destruction.
            try:
                _crytopz_stop_live_market(handle)
            except Exception:
                pass

            _crytopz_destroy(handle)

        finally:
            self._handle = None

    def reset(self) -> None:
        """
        Destroy and recreate the native Core.
        """

        self.close()
        self._create_core()

    def __enter__(self) -> "CrytopzAPI":
        self._require_handle()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    # ========================================================
    # PROPERTIES
    # ========================================================

    @property
    def handle(self):
        return self._handle

    @property
    def cash(self) -> float:
        return self.balance()

    @property
    def total_equity(self) -> float:
        return float(
            _crytopz_equity(
                self._require_handle()
            )
        )

    @property
    def positions_map(self) -> dict:
        return {
            position["symbol"]: position
            for position in self.positions()
        }

    # ========================================================
    # VALIDATION
    # ========================================================

    @staticmethod
    def _symbol(symbol: str) -> bytes:
        if not isinstance(symbol, str):
            raise TypeError(
                "symbol must be a string."
            )

        normalized = symbol.strip().upper()

        if not normalized:
            raise ValueError(
                "symbol cannot be empty."
            )

        return normalized.encode("utf-8")

    @staticmethod
    def _validate_quantity(
        quantity: float,
    ) -> float:

        try:
            value = float(quantity)

        except (TypeError, ValueError) as error:
            raise ValueError(
                "Quantity must be a valid number."
            ) from error

        if value <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        return value

    @staticmethod
    def _validate_price(
        price: float,
        name: str,
    ) -> float:

        try:
            value = float(price)

        except (TypeError, ValueError) as error:
            raise ValueError(
                f"{name} must be a valid number."
            ) from error

        if value < 0:
            raise ValueError(
                f"{name} cannot be negative."
            )

        return value

    # ========================================================
    # MARKET
    # ========================================================

    def update_market(
        self,
        symbol: str,
        bid: float,
        ask: float,
        last: float,
        timestamp: int = 0,
    ) -> None:

        bid = self._validate_price(
            bid,
            "bid",
        )

        ask = self._validate_price(
            ask,
            "ask",
        )

        last = self._validate_price(
            last,
            "last",
        )

        try:
            timestamp = int(timestamp)

        except (TypeError, ValueError) as error:
            raise ValueError(
                "timestamp must be an integer."
            ) from error

        if timestamp < 0:
            raise ValueError(
                "timestamp cannot be negative."
            )

        _crytopz_update_market(
            self._require_handle(),
            self._symbol(symbol),
            DOUBLE(bid),
            DOUBLE(ask),
            DOUBLE(last),
            UINT64(timestamp),
        )

    def get_price(
        self,
        symbol: str,
    ) -> float:

        return float(
            _crytopz_get_price(
                self._require_handle(),
                self._symbol(symbol),
            )
        )

    # ========================================================
    # LIVE MARKET
    # ========================================================

    def start_live_market(self) -> bool:
        """
        Start the native C++ live market scheduler.

        Returns:
            True  -> scheduler started
            False -> scheduler was already running / refused
        """

        return bool(
            _crytopz_start_live_market(
                self._require_handle()
            )
        )

    def stop_live_market(self) -> None:
        """
        Stop the native C++ live market scheduler.
        """

        _crytopz_stop_live_market(
            self._require_handle()
        )

    def live_market_running(self) -> bool:
        """
        Check whether native live market is running.
        """

        return bool(
            _crytopz_live_market_running(
                self._require_handle()
            )
        )

    def live_market_interval_ms(self) -> int:
        """
        Get the native live market scheduler interval.
        """

        return int(
            _crytopz_live_market_interval_ms(
                self._require_handle()
            )
        )

    @property
    def live_market_enabled(self) -> bool:
        return self.live_market_running()

    @property
    def live_market_interval(self) -> int:
        return self.live_market_interval_ms()

    # ========================================================
    # TRADING
    # ========================================================

    def buy(
        self,
        symbol: str,
        quantity: float,
    ) -> int:

        quantity = self._validate_quantity(
            quantity
        )

        order_id = _crytopz_buy(
            self._require_handle(),
            self._symbol(symbol),
            DOUBLE(quantity),
        )

        return int(order_id)

    def sell(
        self,
        symbol: str,
        quantity: float,
    ) -> int:

        quantity = self._validate_quantity(
            quantity
        )

        order_id = _crytopz_sell(
            self._require_handle(),
            self._symbol(symbol),
            DOUBLE(quantity),
        )

        return int(order_id)

    # ========================================================
    # ACCOUNT
    # ========================================================

    def balance(self) -> float:
        return float(
            _crytopz_balance(
                self._require_handle()
            )
        )

    def get_balance(self) -> float:
        return self.balance()

    def get_cash(self) -> float:
        return self.cash

    def get_total_equity(self) -> float:
        return self.total_equity

    # ========================================================
    # POSITIONS
    # ========================================================

    def position_quantity(
        self,
        symbol: str,
    ) -> float:

        return float(
            _crytopz_position_quantity(
                self._require_handle(),
                self._symbol(symbol),
            )
        )

    def position_average_price(
        self,
        symbol: str,
    ) -> float:

        return float(
            _crytopz_position_average_price(
                self._require_handle(),
                self._symbol(symbol),
            )
        )

    def position(
        self,
        symbol: str,
    ) -> dict:

        normalized = symbol.strip().upper()

        quantity = self.position_quantity(
            normalized
        )

        average_price = self.position_average_price(
            normalized
        )

        return {
            "symbol": normalized,
            "quantity": quantity,
            "average_price": average_price,
        }

    def positions(
        self,
        symbols: Optional[list[str]] = None,
    ) -> list[dict]:

        if symbols is None:
            symbols = self.supported_symbols

        result = []

        for symbol in symbols:
            position = self.position(symbol)

            if abs(position["quantity"]) > 1e-12:
                result.append(position)

        return result

    # ========================================================
    # PNL
    # ========================================================

    def realized_pnl(self) -> float:
        return float(
            _crytopz_realized_pnl(
                self._require_handle()
            )
        )

    def unrealized_pnl(self) -> float:
        return float(
            _crytopz_unrealized_pnl(
                self._require_handle()
            )
        )

    def position_value(self) -> float:
        return float(
            _crytopz_position_value(
                self._require_handle()
            )
        )

    def pnl(self) -> float:
        return float(
            _crytopz_total_pnl(
                self._require_handle()
            )
        )

    def get_realized_pnl(self) -> float:
        return self.realized_pnl()

    def get_unrealized_pnl(self) -> float:
        return self.unrealized_pnl()

    def get_pnl(self) -> float:
        return self.pnl()

    # ========================================================
    # ACCOUNT SNAPSHOT
    # ========================================================

    def account(self) -> dict:

        cash = self.cash
        position_value = self.position_value()
        realized = self.realized_pnl()
        unrealized = self.unrealized_pnl()
        equity = self.total_equity
        pnl = self.pnl()

        return {
            "cash": cash,
            "balance": cash,
            "total_equity": equity,
            "equity": equity,
            "position_value": position_value,
            "realized_pnl": realized,
            "unrealized_pnl": unrealized,
            "pnl": pnl,
        }

    # ========================================================
    # PORTFOLIO
    # ========================================================

    def portfolio(
        self,
        symbols: Optional[list[str]] = None,
    ) -> dict:

        account = self.account()

        return {
            "cash": account["cash"],
            "balance": account["balance"],
            "total_equity": account["total_equity"],
            "equity": account["equity"],
            "position_value": account["position_value"],
            "realized_pnl": account["realized_pnl"],
            "unrealized_pnl": account["unrealized_pnl"],
            "pnl": account["pnl"],
            "positions": self.positions(symbols),
        }

    # ========================================================
    # ORDERS
    # ========================================================

    def order_count(self) -> int:
        return int(
            _crytopz_order_count(
                self._require_handle()
            )
        )

    def _validate_order_index(
        self,
        index: int,
    ) -> int:

        try:
            index = int(index)

        except (TypeError, ValueError) as error:
            raise ValueError(
                "Order index must be an integer."
            ) from error

        count = self.order_count()

        if index < 0 or index >= count:
            raise IndexError(
                f"Order index out of range: "
                f"{index} (count={count})"
            )

        return index

    def order_id(
        self,
        index: int,
    ) -> int:

        index = self._validate_order_index(index)

        return int(
            _crytopz_order_id(
                self._require_handle(),
                UINT64(index),
            )
        )

    def order_symbol(
        self,
        index: int,
    ) -> str:

        index = self._validate_order_index(index)

        value = _crytopz_order_symbol(
            self._require_handle(),
            UINT64(index),
        )

        if not value:
            return ""

        return value.decode(
            "utf-8",
            errors="replace",
        )

    def order_side(
        self,
        index: int,
    ) -> int:

        index = self._validate_order_index(index)

        return int(
            _crytopz_order_side(
                self._require_handle(),
                UINT64(index),
            )
        )

    def order_type(
        self,
        index: int,
    ) -> int:

        index = self._validate_order_index(index)

        return int(
            _crytopz_order_type(
                self._require_handle(),
                UINT64(index),
            )
        )

    def order_price(
        self,
        index: int,
    ) -> float:

        index = self._validate_order_index(index)

        return float(
            _crytopz_order_price(
                self._require_handle(),
                UINT64(index),
            )
        )

    def order_quantity(
        self,
        index: int,
    ) -> float:

        index = self._validate_order_index(index)

        return float(
            _crytopz_order_quantity(
                self._require_handle(),
                UINT64(index),
            )
        )

    def order_status(
        self,
        index: int,
    ) -> int:

        index = self._validate_order_index(index)

        return int(
            _crytopz_order_status(
                self._require_handle(),
                UINT64(index),
            )
        )

    def order_timestamp(
        self,
        index: int,
    ) -> int:

        index = self._validate_order_index(index)

        return int(
            _crytopz_order_timestamp(
                self._require_handle(),
                UINT64(index),
            )
        )

    # ========================================================
    # ORDER OBJECT
    # ========================================================

    def get_order(
        self,
        index: int,
    ) -> Optional[dict]:

        try:
            index = int(index)

        except (TypeError, ValueError):
            return None

        count = self.order_count()

        if index < 0 or index >= count:
            return None

        return {
            "id": self.order_id(index),
            "symbol": self.order_symbol(index),
            "side": self.order_side(index),
            "type": self.order_type(index),
            "price": self.order_price(index),
            "quantity": self.order_quantity(index),
            "status": self.order_status(index),
            "timestamp": self.order_timestamp(index),
        }

    def orders(self) -> list[dict]:

        result = []

        count = self.order_count()

        for index in range(count):
            order = self.get_order(index)

            if order is not None:
                result.append(order)

        return result

    def order_history(self) -> list[dict]:
        return self.orders()

    # ========================================================
    # SNAPSHOT
    # ========================================================

    def snapshot(
        self,
        symbols: Optional[list[str]] = None,
    ) -> dict:

        return {
            "account": self.account(),
            "portfolio": self.portfolio(symbols),
            "orders": self.orders(),
            "live_market": {
                "running": self.live_market_running(),
                "interval_ms": self.live_market_interval_ms(),
            },
        }

