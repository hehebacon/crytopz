
class BotAPI:

    API_VERSION = "1"

    def __init__(self, core=None, permissions=None):

        self.core = core

        self.permissions = set(
            permissions or []
        )

        self.market = MarketAPI(self)
        self.account = AccountAPI(self)
        self.order = OrderAPI(self)

    # =====================================================
    # CORE
    # =====================================================

    def require_core(self):

        if self.core is None:
            raise RuntimeError(
                "Crytopz Core is not connected to BotAPI."
            )

        return self.core

    # =====================================================
    # PERMISSIONS
    # =====================================================

    def require_permission(self, *permissions):

        for permission in permissions:

            if permission in self.permissions:
                return True

        raise PermissionError(
            "Permission denied. Required one of: "
            + ", ".join(permissions)
        )

    # =====================================================
    # LOG
    # =====================================================

    def log(self, message):

        print(
            f"[BOT] {message}"
        )


# =========================================================
# MARKET
# =========================================================

class MarketAPI:

    def __init__(self, api):
        self.api = api

    def get_price(self, symbol):

        self.api.require_permission(
            "market.read"
        )

        core = self.api.require_core()

        if not hasattr(core, "get_price"):
            raise RuntimeError(
                "Core does not provide get_price()."
            )

        price = core.get_price(symbol)

        if price is None:
            raise RuntimeError(
                f"Core returned None price for {symbol}"
            )

        return float(price)

    def price(self, symbol):
        return self.get_price(symbol)


# =========================================================
# ACCOUNT
# =========================================================

class AccountAPI:

    def __init__(self, api):
        self.api = api

    def get_balance(self):

        self.api.require_permission(
            "account.read"
        )

        core = self.api.require_core()

        if hasattr(core, "get_balance"):
            value = core.get_balance()

        elif hasattr(core, "cash"):
            value = core.cash

        else:
            raise RuntimeError(
                "Core does not provide account balance."
            )

        if value is None:
            raise RuntimeError(
                "Core returned None balance."
            )

        return float(value)

    def get_equity(self):

        self.api.require_permission(
            "account.read"
        )

        core = self.api.require_core()

        if hasattr(core, "total_equity"):
            value = core.total_equity()

        elif hasattr(core, "get_equity"):
            value = core.get_equity()

        else:
            raise RuntimeError(
                "Core does not provide equity."
            )

        if value is None:
            raise RuntimeError(
                "Core returned None equity."
            )

        return float(value)

    def get_pnl(self):

        self.api.require_permission(
            "account.read"
        )

        core = self.api.require_core()

        if hasattr(core, "pnl"):
            value = core.pnl()

        elif hasattr(core, "get_pnl"):
            value = core.get_pnl()

        else:
            raise RuntimeError(
                "Core does not provide PnL."
            )

        if value is None:
            raise RuntimeError(
                "Core returned None PnL."
            )

        return float(value)

    def get_positions(self):

        self.api.require_permission(
            "account.read"
        )

        core = self.api.require_core()

        if hasattr(core, "get_positions"):
            value = core.get_positions()

        elif hasattr(core, "positions"):
            value = core.positions

        else:
            raise RuntimeError(
                "Core does not provide positions."
            )

        return value


# =========================================================
# ORDER
# =========================================================

class OrderAPI:

    def __init__(self, api):
        self.api = api

    def _place(self, symbol, side, quantity):

        self.api.require_permission(
            "trade.execute",
            "order.create"
        )

        core = self.api.require_core()

        if not hasattr(core, "place_order"):
            raise RuntimeError(
                "Core does not provide place_order()."
            )

        if quantity is None:
            raise ValueError(
                "Order quantity cannot be None."
            )

        quantity = float(quantity)

        if quantity <= 0:
            raise ValueError(
                "Order quantity must be greater than 0."
            )

        result = core.place_order(
            symbol,
            side,
            quantity
        )

        if result is None:
            raise RuntimeError(
                f"Core returned None for {side} order."
            )

        return result

    def buy(self, symbol, quantity):

        return self._place(
            symbol,
            "BUY",
            quantity
        )

    def sell(self, symbol, quantity):

        return self._place(
            symbol,
            "SELL",
            quantity
        )

    def cancel(self, order_id):

        self.api.require_permission(
            "trade.execute",
            "order.cancel"
        )

        core = self.api.require_core()

        if not hasattr(core, "cancel_order"):
            raise RuntimeError(
                "Core does not provide cancel_order()."
            )

        return core.cancel_order(
            order_id
        )


# =========================================================
# COMPATIBILITY
# =========================================================

# Cho bot cũ dùng sdk.price(), sdk.buy(), sdk.sell()

def _price(self, symbol):
    return self.market.get_price(symbol)


def _buy(self, symbol, quantity):
    return self.order.buy(symbol, quantity)


def _sell(self, symbol, quantity):
    return self.order.sell(symbol, quantity)


BotAPI.price = _price
BotAPI.buy = _buy
BotAPI.sell = _sell

