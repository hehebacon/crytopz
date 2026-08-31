from dataclasses import dataclass, field
from typing import Dict, List
import time


# =========================================================
# POSITION
# =========================================================

@dataclass
class Position:

    symbol: str

    quantity: float = 0.0

    average_price: float = 0.0


# =========================================================
# ORDER
# =========================================================

@dataclass
class Order:

    id: int

    symbol: str

    side: str

    quantity: float

    price: float

    status: str

    fee: float = 0.0

    limit_price: float = 0.0

    timestamp: float = field(
        default_factory=time.time
    )


# =========================================================
# PAPER TRADING ENGINE
# =========================================================

class PaperTradingEngine:

    def __init__(
        self,
        initial_balance=10_000.0,
        fee_rate=0.001
    ):

        self.initial_balance = float(
            initial_balance
        )

        self.cash = self.initial_balance

        self.fee_rate = float(
            fee_rate
        )

        self.positions: Dict[
            str,
            Position
        ] = {}

        self.orders: List[
            Order
        ] = []

        self.next_order_id = 1

        self._realized_pnl = 0.0

        self.prices = {

            "BTCUSDT": 105432.50,

            "ETHUSDT": 3821.42,

            "SOLUSDT": 182.14,

            "BNBUSDT": 742.30,

            "XRPUSDT": 2.91,

        }


    # =====================================================
    # MARKET DATA
    # =====================================================

    def get_price(self, symbol):

        return self.prices.get(
            symbol.upper(),
            0.0
        )


    def set_price(
        self,
        symbol,
        price
    ):

        symbol = symbol.upper()

        try:

            price = float(price)

        except (
            TypeError,
            ValueError
        ):

            return False


        if price <= 0:

            return False


        self.prices[symbol] = price

        # Check pending limit orders
        self.check_limit_orders()

        return True


    # =====================================================
    # INTERNAL ORDER ID
    # =====================================================

    def _new_order(
        self,
        symbol,
        side,
        quantity,
        price,
        status,
        fee=0.0,
        limit_price=0.0
    ):

        order = Order(

            id=self.next_order_id,

            symbol=symbol,

            side=side,

            quantity=quantity,

            price=price,

            status=status,

            fee=fee,

            limit_price=limit_price

        )

        self.orders.append(order)

        self.next_order_id += 1

        return order


    # =====================================================
    # MARKET BUY
    # =====================================================

    def buy(
        self,
        symbol,
        quantity
    ):

        symbol = symbol.upper()

        try:

            quantity = float(quantity)

        except (
            TypeError,
            ValueError
        ):

            return False, "Invalid quantity"


        if quantity <= 0:

            return False, "Invalid quantity"


        price = self.get_price(
            symbol
        )


        if price <= 0:

            return False, "Unknown symbol"


        value = (
            price
            * quantity
        )

        fee = (
            value
            * self.fee_rate
        )

        total = (
            value
            + fee
        )


        if total > self.cash:

            return False, (
                "Insufficient paper balance"
            )


        self.cash -= total


        self._add_position(
            symbol,
            quantity,
            price
        )


        order = self._new_order(

            symbol=symbol,

            side="BUY",

            quantity=quantity,

            price=price,

            status="FILLED",

            fee=fee

        )


        return True, order


    # =====================================================
    # MARKET SELL
    # =====================================================

    def sell(
        self,
        symbol,
        quantity
    ):

        symbol = symbol.upper()

        try:

            quantity = float(quantity)

        except (
            TypeError,
            ValueError
        ):

            return False, "Invalid quantity"


        if quantity <= 0:

            return False, "Invalid quantity"


        price = self.get_price(
            symbol
        )


        if price <= 0:

            return False, "Unknown symbol"


        position = self.positions.get(
            symbol
        )


        if position is None:

            return False, "No position"


        if quantity > position.quantity:

            return False, (
                "Insufficient position"
            )


        value = (
            price
            * quantity
        )

        fee = (
            value
            * self.fee_rate
        )

        revenue = (
            value
            - fee
        )


        realized = (

            price
            - position.average_price

        ) * quantity


        self._realized_pnl += (
            realized
        )


        self.cash += revenue


        self._remove_position(
            symbol,
            quantity
        )


        order = self._new_order(

            symbol=symbol,

            side="SELL",

            quantity=quantity,

            price=price,

            status="FILLED",

            fee=fee

        )


        return True, order


    # =====================================================
    # LIMIT BUY
    # =====================================================

    def place_limit_buy(
        self,
        symbol,
        quantity,
        limit_price
    ):

        symbol = symbol.upper()

        try:

            quantity = float(quantity)

            limit_price = float(
                limit_price
            )

        except (
            TypeError,
            ValueError
        ):

            return False, "Invalid order"


        if quantity <= 0:

            return False, "Invalid quantity"


        if limit_price <= 0:

            return False, (
                "Invalid limit price"
            )


        current_price = self.get_price(
            symbol
        )


        if current_price <= 0:

            return False, "Unknown symbol"


        value = (
            quantity
            * limit_price
        )

        fee = (
            value
            * self.fee_rate
        )

        required = (
            value
            + fee
        )


        if required > self.cash:

            return False, (
                "Insufficient paper balance"
            )


        # If already executable,
        # fill immediately.

        if current_price <= limit_price:

            return self.buy_at_price(
                symbol,
                quantity,
                limit_price
            )


        order = self._new_order(

            symbol=symbol,

            side="BUY",

            quantity=quantity,

            price=0.0,

            status="OPEN",

            fee=0.0,

            limit_price=limit_price

        )


        return True, order


    # =====================================================
    # LIMIT SELL
    # =====================================================

    def place_limit_sell(
        self,
        symbol,
        quantity,
        limit_price
    ):

        symbol = symbol.upper()

        try:

            quantity = float(quantity)

            limit_price = float(
                limit_price
            )

        except (
            TypeError,
            ValueError
        ):

            return False, "Invalid order"


        if quantity <= 0:

            return False, "Invalid quantity"


        if limit_price <= 0:

            return False, (
                "Invalid limit price"
            )


        position = self.positions.get(
            symbol
        )


        if position is None:

            return False, "No position"


        if quantity > position.quantity:

            return False, (
                "Insufficient position"
            )


        current_price = self.get_price(
            symbol
        )


        if current_price >= limit_price:

            return self.sell_at_price(
                symbol,
                quantity,
                limit_price
            )


        order = self._new_order(

            symbol=symbol,

            side="SELL",

            quantity=quantity,

            price=0.0,

            status="OPEN",

            limit_price=limit_price

        )


        return True, order


    # =====================================================
    # LIMIT CHECKER
    # =====================================================

    def check_limit_orders(self):

        # Copy list so status changes
        # don't break iteration.

        for order in list(
            self.orders
        ):

            if order.status != "OPEN":

                continue


            market_price = self.get_price(
                order.symbol
            )


            if order.side == "BUY":

                if (
                    market_price
                    <= order.limit_price
                ):

                    self._fill_limit_order(
                        order
                    )


            elif order.side == "SELL":

                if (
                    market_price
                    >= order.limit_price
                ):

                    self._fill_limit_order(
                        order
                    )


    # =====================================================
    # FILL LIMIT
    # =====================================================

    def _fill_limit_order(
        self,
        order
    ):

        price = order.limit_price


        if order.side == "BUY":

            success, result = (
                self.buy_at_price(
                    order.symbol,
                    order.quantity,
                    price,
                    create_order=False
                )
            )


        else:

            success, result = (
                self.sell_at_price(
                    order.symbol,
                    order.quantity,
                    price,
                    create_order=False
                )
            )


        if not success:

            order.status = "REJECTED"

            return


        order.price = price

        order.fee = (
            price
            * order.quantity
            * self.fee_rate
        )

        order.status = "FILLED"


    # =====================================================
    # BUY AT SPECIFIC PRICE
    # =====================================================

    def buy_at_price(
        self,
        symbol,
        quantity,
        price,
        create_order=True
    ):

        symbol = symbol.upper()

        value = (
            quantity
            * price
        )

        fee = (
            value
            * self.fee_rate
        )

        total = (
            value
            + fee
        )


        if total > self.cash:

            return False, (
                "Insufficient paper balance"
            )


        self.cash -= total


        self._add_position(
            symbol,
            quantity,
            price
        )


        if not create_order:

            return True, None


        order = self._new_order(

            symbol=symbol,

            side="BUY",

            quantity=quantity,

            price=price,

            status="FILLED",

            fee=fee

        )


        return True, order


    # =====================================================
    # SELL AT SPECIFIC PRICE
    # =====================================================

    def sell_at_price(
        self,
        symbol,
        quantity,
        price,
        create_order=True
    ):

        symbol = symbol.upper()


        position = self.positions.get(
            symbol
        )


        if position is None:

            return False, "No position"


        if quantity > position.quantity:

            return False, (
                "Insufficient position"
            )


        value = (
            quantity
            * price
        )

        fee = (
            value
            * self.fee_rate
        )

        revenue = (
            value
            - fee
        )


        realized = (

            price
            - position.average_price

        ) * quantity


        self._realized_pnl += (
            realized
        )


        self.cash += revenue


        self._remove_position(
            symbol,
            quantity
        )


        if not create_order:

            return True, None


        order = self._new_order(

            symbol=symbol,

            side="SELL",

            quantity=quantity,

            price=price,

            status="FILLED",

            fee=fee

        )


        return True, order


    # =====================================================
    # POSITION ADD
    # =====================================================

    def _add_position(
        self,
        symbol,
        quantity,
        price
    ):

        position = self.positions.get(
            symbol
        )


        if position is None:

            position = Position(
                symbol=symbol
            )

            self.positions[
                symbol
            ] = position


        old_value = (

            position.quantity
            * position.average_price

        )


        new_value = (
            old_value
            + (
                quantity
                * price
            )
        )


        position.quantity += quantity


        position.average_price = (
            new_value
            / position.quantity
        )


    # =====================================================
    # POSITION REMOVE
    # =====================================================

    def _remove_position(
        self,
        symbol,
        quantity
    ):

        position = self.positions.get(
            symbol
        )


        if position is None:

            return


        position.quantity -= quantity


        if position.quantity <= 1e-12:

            del self.positions[
                symbol
            ]


    # =====================================================
    # CANCEL ORDER
    # =====================================================

    def cancel_order(
        self,
        order_id
    ):

        for order in self.orders:

            if order.id != order_id:

                continue


            if order.status != "OPEN":

                return False, (
                    "Order is not open"
                )


            order.status = "CANCELLED"

            return True, order


        return False, "Order not found"


    # =====================================================
    # POSITION VALUE
    # =====================================================

    def position_value(self):

        total = 0.0


        for (
            symbol,
            position
        ) in self.positions.items():

            total += (

                position.quantity
                * self.get_price(symbol)

            )


        return total


    # =====================================================
    # UNREALIZED PNL
    # =====================================================

    def unrealized_pnl(self):

        total = 0.0


        for (
            symbol,
            position
        ) in self.positions.items():

            total += (

                self.get_price(symbol)
                - position.average_price

            ) * position.quantity


        return total


    # =====================================================
    # REALIZED PNL
    # =====================================================

    def realized_pnl(self):

        return self._realized_pnl


    # =====================================================
    # EQUITY
    # =====================================================

    def total_equity(self):

        return (
            self.cash
            + self.position_value()
        )


    # =====================================================
    # TOTAL PNL
    # =====================================================

    def pnl(self):

        return (
            self.total_equity()
            - self.initial_balance
        )


    # =====================================================
    # ACCOUNT
    # =====================================================

    def account(self):

        return {

            "cash": self.cash,

            "position_value":
                self.position_value(),

            "equity":
                self.total_equity(),

            "pnl":
                self.pnl(),

            "realized_pnl":
                self.realized_pnl(),

            "unrealized_pnl":
                self.unrealized_pnl(),

        }


    # =====================================================
    # SNAPSHOT
    # =====================================================

    def snapshot(self):

        return {

            "cash":
                self.cash,

            "position_value":
                self.position_value(),

            "equity":
                self.total_equity(),

            "pnl":
                self.pnl(),

            "realized_pnl":
                self.realized_pnl(),

            "unrealized_pnl":
                self.unrealized_pnl(),


            "positions": {

                symbol: {

                    "quantity":
                        position.quantity,

                    "average_price":
                        position.average_price,

                    "market_price":
                        self.get_price(
                            symbol
                        ),

                    "value":
                        (
                            position.quantity
                            * self.get_price(
                                symbol
                            )
                        ),

                    "unrealized_pnl":
                        (
                            self.get_price(
                                symbol
                            )
                            - position.average_price
                        )
                        * position.quantity,

                }

                for (
                    symbol,
                    position
                )
                in self.positions.items()

            },


            "orders": [

                {

                    "id":
                        order.id,

                    "symbol":
                        order.symbol,

                    "side":
                        order.side,

                    "quantity":
                        order.quantity,

                    "price":
                        order.price,

                    "limit_price":
                        order.limit_price,

                    "status":
                        order.status,

                    "fee":
                        order.fee,

                    "timestamp":
                        order.timestamp,

                }

                for order
                in self.orders

            ]

        }


    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.cash = (
            self.initial_balance
        )

        self.positions.clear()

        self.orders.clear()

        self.next_order_id = 1

        self._realized_pnl = 0.0


    # =====================================================
    # DEBUG
    # =====================================================

    def __repr__(self):

        return (

            "<PaperTradingEngine "
            f"cash=${self.cash:,.2f} "
            f"equity=${self.total_equity():,.2f} "
            f"pnl=${self.pnl():,.2f}>"

        )