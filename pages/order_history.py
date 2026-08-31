
import customtkinter as ctk
from datetime import datetime


class OrderHistoryPage(ctk.CTkFrame):

    def __init__(self, parent, app):

        super().__init__(
            parent,
            corner_radius=0
        )

        self.app = app

        self.filter_side = "ALL"
        self.filter_symbol = "ALL"

        self.build_ui()
        self.refresh()


    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        ctk.CTkLabel(
            header,
            text="Order History",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        self.count_label = ctk.CTkLabel(
            header,
            text="0 orders",
            text_color="gray"
        )

        self.count_label.pack(
            side="left",
            padx=15
        )


        # =================================================
        # FILTERS
        # =================================================

        filters = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        filters.pack(
            fill="x",
            padx=25,
            pady=(0, 12)
        )


        ctk.CTkLabel(
            filters,
            text="Side",
            text_color="gray"
        ).pack(
            side="left",
            padx=(15, 5)
        )


        self.side_menu = ctk.CTkOptionMenu(
            filters,
            values=[
                "ALL",
                "BUY",
                "SELL"
            ],
            command=self.change_side_filter
        )

        self.side_menu.set("ALL")

        self.side_menu.pack(
            side="left",
            padx=5,
            pady=10
        )


        ctk.CTkLabel(
            filters,
            text="Symbol",
            text_color="gray"
        ).pack(
            side="left",
            padx=(15, 5)
        )


        self.symbol_menu = ctk.CTkOptionMenu(
            filters,
            values=["ALL"],
            command=self.change_symbol_filter
        )

        self.symbol_menu.set("ALL")

        self.symbol_menu.pack(
            side="left",
            padx=5,
            pady=10
        )


        ctk.CTkButton(
            filters,
            text="Refresh",
            width=90,
            command=self.refresh
        ).pack(
            side="right",
            padx=15
        )


        # =================================================
        # TABLE
        # =================================================

        self.table = ctk.CTkScrollableFrame(
            self,
            corner_radius=14
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )


        self.build_table_header()


    # =====================================================
    # TABLE HEADER
    # =====================================================

    def build_table_header(self):

        header = ctk.CTkFrame(
            self.table,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            pady=(5, 8)
        )

        columns = [
            ("ID", 70),
            ("Time", 155),
            ("Symbol", 120),
            ("Side", 90),
            ("Type", 90),
            ("Price", 150),
            ("Quantity", 120),
            ("Status", 100)
        ]

        for text, width in columns:

            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                anchor="w",
                text_color="gray",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=3
            )


    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        if not hasattr(
            self.app,
            "engine"
        ):
            return


        engine = self.app.engine


        try:

            history = engine.order_history()

        except Exception as exc:

            self.show_empty(
                f"Order history unavailable: {exc}"
            )

            return


        # -------------------------------------------------
        # UPDATE SYMBOL FILTER
        # -------------------------------------------------

        symbols = sorted(
            {
                order.get("symbol", "")
                for order in history
                if order.get("symbol")
            }
        )

        values = ["ALL"] + symbols

        current = self.symbol_menu.get()

        self.symbol_menu.configure(
            values=values
        )

        if current in values:
            self.symbol_menu.set(current)
        else:
            self.symbol_menu.set("ALL")
            self.filter_symbol = "ALL"


        # -------------------------------------------------
        # FILTER
        # -------------------------------------------------

        filtered = []

        for order in history:

            side = order.get(
                "side",
                "UNKNOWN"
            )

            symbol = order.get(
                "symbol",
                ""
            )


            if (
                self.filter_side != "ALL"
                and side != self.filter_side
            ):
                continue


            if (
                self.filter_symbol != "ALL"
                and symbol != self.filter_symbol
            ):
                continue


            filtered.append(order)


        self.count_label.configure(
            text=f"{len(filtered)} orders"
        )


        # -------------------------------------------------
        # CLEAR TABLE
        # -------------------------------------------------

        for widget in self.table.winfo_children():

            widget.destroy()


        self.build_table_header()


        # -------------------------------------------------
        # EMPTY
        # -------------------------------------------------

        if not filtered:

            self.show_empty(
                "No orders found."
            )

            return


        # -------------------------------------------------
        # ORDERS
        # -------------------------------------------------

        for order in reversed(filtered):

            self.add_order_row(
                order
            )


    # =====================================================
    # ORDER ROW
    # =====================================================

    def add_order_row(
        self,
        order
    ):

        row = ctk.CTkFrame(
            self.table,
            corner_radius=8
        )

        row.pack(
            fill="x",
            pady=3
        )


        timestamp = order.get(
            "timestamp",
            0
        )


        if timestamp:

            try:

                # Core timestamp = milliseconds
                dt = datetime.fromtimestamp(
                    timestamp / 1000
                )

                time_text = dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            except Exception:

                time_text = "Unknown"

        else:

            time_text = "Unknown"


        values = [
            str(order.get("id", "-")),
            time_text,
            order.get("symbol", "-"),
            order.get("side", "UNKNOWN"),
            self.order_type_text(
                order.get("type", -1)
            ),
            f"${order.get('price', 0):,.2f}",
            f"{order.get('quantity', 0):g}",
            self.order_status_text(
                order.get("status", -1)
            )
        ]


        widths = [
            70,
            155,
            120,
            90,
            90,
            150,
            120,
            100
        ]


        for index, value in enumerate(values):

            text_color = None


            # BUY / SELL
            if index == 3:

                if value == "BUY":
                    text_color = "#4ade80"

                elif value == "SELL":
                    text_color = "#f87171"


            # STATUS
            if index == 7:

                if value == "FILLED":
                    text_color = "#4ade80"

                elif value == "CANCELLED":
                    text_color = "#f87171"


            ctk.CTkLabel(
                row,
                text=value,
                width=widths[index],
                anchor="w",
                text_color=text_color
            ).pack(
                side="left",
                padx=3,
                pady=10
            )


    # =====================================================
    # EMPTY
    # =====================================================

    def show_empty(
        self,
        message
    ):

        ctk.CTkLabel(
            self.table,
            text=message,
            text_color="gray"
        ).pack(
            pady=35
        )


    # =====================================================
    # FILTER
    # =====================================================

    def change_side_filter(
        self,
        value
    ):

        self.filter_side = value

        self.refresh()


    def change_symbol_filter(
        self,
        value
    ):

        self.filter_symbol = value

        self.refresh()


    # =====================================================
    # ENUM DISPLAY
    # =====================================================

    def order_type_text(
        self,
        value
    ):

        types = {
            0: "Market",
            1: "Limit",
            2: "Stop",
            3: "Stop Limit"
        }

        return types.get(
            value,
            str(value)
        )


    def order_status_text(
        self,
        value
    ):

        statuses = {
            0: "Pending",
            1: "Filled",
            2: "Cancelled",
            3: "Rejected"
        }

        return statuses.get(
            value,
            str(value)
        )

