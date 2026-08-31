
import ctypes
import os
import sys


# ============================================================
# DLL PATH
# ============================================================

def get_dll_path():

    if getattr(sys, "frozen", False):

        base_dir = os.path.dirname(
            sys.executable
        )

    else:

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

    return os.path.join(
        base_dir,
        "crytopz_bridge.dll"
    )


DLL_PATH = get_dll_path()


if not os.path.exists(DLL_PATH):
    raise FileNotFoundError(
        f"Crytopz bridge DLL not found:\n{DLL_PATH}"
    )


# ============================================================
# LOAD DLL
# ============================================================

_bridge = ctypes.CDLL(DLL_PATH)


# ============================================================
# C TYPES
# ============================================================

_bridge.crytopz_create.argtypes = [
    ctypes.c_double
]

_bridge.crytopz_create.restype = (
    ctypes.c_void_p
)


_bridge.crytopz_destroy.argtypes = [
    ctypes.c_void_p
]

_bridge.crytopz_destroy.restype = None


_bridge.crytopz_update_market.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_uint64
]

_bridge.crytopz_update_market.restype = None


_bridge.crytopz_get_price.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p
]

_bridge.crytopz_get_price.restype = (
    ctypes.c_double
)


_bridge.crytopz_buy.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_double
]

_bridge.crytopz_buy.restype = (
    ctypes.c_uint64
)


_bridge.crytopz_sell.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_double
]

_bridge.crytopz_sell.restype = (
    ctypes.c_uint64
)


_bridge.crytopz_balance.argtypes = [
    ctypes.c_void_p
]

_bridge.crytopz_balance.restype = (
    ctypes.c_double
)


_bridge.crytopz_position_quantity.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p
]

_bridge.crytopz_position_quantity.restype = (
    ctypes.c_double
)


_bridge.crytopz_position_average_price.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p
]

_bridge.crytopz_position_average_price.restype = (
    ctypes.c_double
)


_bridge.crytopz_realized_pnl.argtypes = [
    ctypes.c_void_p
]

_bridge.crytopz_realized_pnl.restype = (
    ctypes.c_double
)
_bridge.crytopz_order_count.argtypes = [
    ctypes.c_void_p
]

_bridge.crytopz_order_count.restype = (
    ctypes.c_uint64
)


_bridge.crytopz_order_id.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint64
]

_bridge.crytopz_order_id.restype = (
    ctypes.c_uint64
)


_bridge.crytopz_order_symbol.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint64
]

_bridge.crytopz_order_symbol.restype = (
    ctypes.c_char_p
)


_bridge.crytopz_order_side.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint64
]

_bridge.crytopz_order_side.restype = (
    ctypes.c_int
)


_bridge.crytopz_order_type.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint64
]

_bridge.crytopz_order_type.restype = (
    ctypes.c_int
)


_bridge.crytopz_order_price.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint64
]

_bridge.crytopz_order_price.restype = (
    ctypes.c_double
)


_bridge.crytopz_order_quantity.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint64
]

_bridge.crytopz_order_quantity.restype = (
    ctypes.c_double
)


_bridge.crytopz_order_status.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint64
]

_bridge.crytopz_order_status.restype = (
    ctypes.c_int
)


# ============================================================
# CRYPTOPZ
# ============================================================

class Crytopz:

    def __init__(
        self,
        initial_balance=10000.0
    ):

        self.handle = _bridge.crytopz_create(
            float(initial_balance)
        )

        if not self.handle:
            raise RuntimeError(
                "Failed to create Crytopz Core."
            )
        # ========================================================
    # ORDER HISTORY
    # ========================================================

    def order_count(self):

        return _bridge.crytopz_order_count(
            self.handle
        )


    def get_order(self, index):

        index = int(index)

        symbol = (
            _bridge.crytopz_order_symbol(
                self.handle,
                index
            )
            .decode("utf-8")
        )

        side_value = (
            _bridge.crytopz_order_side(
                self.handle,
                index
            )
        )

        sides = {
            0: "BUY",
            1: "SELL"
        }

        return {
            "id":
                _bridge.crytopz_order_id(
                    self.handle,
                    index
                ),

            "symbol":
                symbol,

            "side":
                sides.get(
                    side_value,
                    "UNKNOWN"
                ),

            "type":
                _bridge.crytopz_order_type(
                    self.handle,
                    index
                ),

            "price":
                _bridge.crytopz_order_price(
                    self.handle,
                    index
                ),

            "quantity":
                _bridge.crytopz_order_quantity(
                    self.handle,
                    index
                ),

            "status":
                _bridge.crytopz_order_status(
                    self.handle,
                    index
                )
        }


    def order_history(self):

        count = self.order_count()

        return [
            self.get_order(index)
            for index in range(count)
        ]

    # ========================================================
    # MARKET
    # ========================================================

    def update_market(
        self,
        symbol,
        bid,
        ask,
        last,
        timestamp
    ):

        _bridge.crytopz_update_market(
            self.handle,
            symbol.encode("utf-8"),
            float(bid),
            float(ask),
            float(last),
            int(timestamp)
        )

    def price(
        self,
        symbol
    ):

        return _bridge.crytopz_get_price(
            self.handle,
            symbol.encode("utf-8")
        )

    # ========================================================
    # TRADING
    # ========================================================

    def buy(
        self,
        symbol,
        quantity
    ):

        return _bridge.crytopz_buy(
            self.handle,
            symbol.encode("utf-8"),
            float(quantity)
        )

    def sell(
        self,
        symbol,
        quantity
    ):

        return _bridge.crytopz_sell(
            self.handle,
            symbol.encode("utf-8"),
            float(quantity)
        )

    # ========================================================
    # ACCOUNT
    # ========================================================

    def balance(self):

        return _bridge.crytopz_balance(
            self.handle
        )

    def position(
        self,
        symbol
    ):

        encoded_symbol = symbol.encode(
            "utf-8"
        )

        return {
            "quantity":
                _bridge.crytopz_position_quantity(
                    self.handle,
                    encoded_symbol
                ),

            "average_price":
                _bridge.crytopz_position_average_price(
                    self.handle,
                    encoded_symbol
                )
        }

    def realized_pnl(self):

        return _bridge.crytopz_realized_pnl(
            self.handle
        )

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        if self.handle:

            _bridge.crytopz_destroy(
                self.handle
            )

            self.handle = None

    def __del__(self):

        try:
            self.close()
        except Exception:
            pass

