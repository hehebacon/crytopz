
import tkinter as tk
from tkinter import ttk, messagebox

from frontend_api import CrytopzAPI


class CrytopzDemo:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Crytopz - Demo"
        )

        self.root.geometry(
            "700x500"
        )

        self.api = CrytopzAPI(
            10000.0
        )

        self.symbol = "BTCUSDT"

        # =========================================
        # INITIAL MARKET
        # =========================================

        self.api.update_market(
            self.symbol,
            100000,
            100010,
            100005,
            1
        )

        # =========================================
        # TITLE
        # =========================================

        title = ttk.Label(
            root,
            text="CRYPTOPZ",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=20
        )

        subtitle = ttk.Label(
            root,
            text="Trading Terminal — Demo"
        )

        subtitle.pack()

        # =========================================
        # MARKET
        # =========================================

        market_frame = ttk.LabelFrame(
            root,
            text="Market"
        )

        market_frame.pack(
            fill="x",
            padx=30,
            pady=15
        )

        self.price_label = ttk.Label(
            market_frame,
            text="BTCUSDT: $100005.00",
            font=("Arial", 18)
        )

        self.price_label.pack(
            pady=15
        )

        # =========================================
        # ACCOUNT
        # =========================================

        account_frame = ttk.LabelFrame(
            root,
            text="Account"
        )

        account_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.balance_label = ttk.Label(
            account_frame,
            text=""
        )

        self.balance_label.pack(
            pady=5
        )

        self.position_label = ttk.Label(
            account_frame,
            text=""
        )

        self.position_label.pack(
            pady=5
        )

        self.pnl_label = ttk.Label(
            account_frame,
            text=""
        )

        self.pnl_label.pack(
            pady=5
        )

        # =========================================
        # ORDER
        # =========================================

        order_frame = ttk.LabelFrame(
            root,
            text="Order"
        )

        order_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        ttk.Label(
            order_frame,
            text="Quantity:"
        ).pack(
            side="left",
            padx=10
        )

        self.quantity = ttk.Entry(
            order_frame,
            width=12
        )

        self.quantity.insert(
            0,
            "0.01"
        )

        self.quantity.pack(
            side="left",
            padx=10
        )

        ttk.Button(
            order_frame,
            text="BUY",
            command=self.buy
        ).pack(
            side="left",
            padx=10
        )

        ttk.Button(
            order_frame,
            text="SELL",
            command=self.sell
        ).pack(
            side="left",
            padx=10
        )

        # =========================================
        # LOG
        # =========================================

        log_frame = ttk.LabelFrame(
            root,
            text="Activity"
        )

        log_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        self.log = tk.Text(
            log_frame,
            height=6,
            state="disabled"
        )

        self.log.pack(
            fill="both",
            expand=True
        )

        # =========================================
        # INITIAL REFRESH
        # =========================================

        self.refresh()

        self.write_log(
            "Crytopz Demo started."
        )

        self.write_log(
            f"Market loaded: {self.symbol}"
        )

        # =========================================
        # START MARKET FEED
        # =========================================

        self.start_market_feed()

    # =============================================
    # MARKET FEED
    # =============================================

    def start_market_feed(self):

        try:

            price = self.api.tick()

            self.refresh()

            self.write_log(
                f"MARKET | "
                f"{self.symbol} "
                f"${price:,.2f}"
            )

        except Exception as e:

            self.write_log(
                f"MARKET ERROR: {e}"
            )

        finally:

            self.root.after(
                1000,
                self.start_market_feed
            )

    # =============================================
    # BUY
    # =============================================

    def buy(self):

        try:

            quantity = float(
                self.quantity.get().strip()
            )

            if quantity <= 0:
                raise ValueError

        except (ValueError, TypeError):

            messagebox.showerror(
                "Invalid quantity",
                "Quantity must be greater than zero."
            )

            return

        try:

            order_id = self.api.buy(
                self.symbol,
                quantity
            )

        except Exception as e:

            self.write_log(
                f"BUY ERROR: {e}"
            )

            return

        if not order_id:

            self.write_log(
                f"BUY REJECTED | "
                f"{quantity} {self.symbol}"
            )

            self.refresh()

            return

        self.write_log(
            f"BUY FILLED | "
            f"{quantity} {self.symbol} | "
            f"Order #{order_id}"
        )

        self.refresh()

    # =============================================
    # SELL
    # =============================================

    def sell(self):

        try:

            quantity = float(
                self.quantity.get().strip()
            )

            if quantity <= 0:
                raise ValueError

        except (ValueError, TypeError):

            messagebox.showerror(
                "Invalid quantity",
                "Quantity must be greater than zero."
            )

            return

        try:

            order_id = self.api.sell(
                self.symbol,
                quantity
            )

        except Exception as e:

            self.write_log(
                f"SELL ERROR: {e}"
            )

            return

        if not order_id:

            self.write_log(
                f"SELL REJECTED | "
                f"{quantity} {self.symbol}"
            )

            self.refresh()

            return

        self.write_log(
            f"SELL FILLED | "
            f"{quantity} {self.symbol} | "
            f"Order #{order_id}"
        )

        self.refresh()

    # =============================================
    # REFRESH
    # =============================================

    def refresh(self):

        try:

            snapshot = self.api.snapshot(
                self.symbol
            )

        except Exception as e:

            # GUI có thể chưa tạo đủ widget
            # trong quá trình khởi tạo.
            if hasattr(self, "log"):

                self.write_log(
                    f"REFRESH ERROR: {e}"
                )

            return

        self.price_label.config(
            text=(
                f"{self.symbol}: "
                f"${snapshot['price']:,.2f}"
            )
        )

        self.balance_label.config(
            text=(
                f"Balance: "
                f"${snapshot['balance']:,.2f}"
            )
        )

        self.position_label.config(
            text=(
                f"Position: "
                f"{snapshot['position']:.4f} "
                f"{self.symbol}"
            )
        )

        self.pnl_label.config(
            text=(
                f"Realized PnL: "
                f"${snapshot['realized_pnl']:,.2f}"
            )
        )

    # =============================================
    # LOG
    # =============================================

    def write_log(self, message):

        self.log.config(
            state="normal"
        )

        self.log.insert(
            "end",
            message + "\n"
        )

        self.log.see(
            "end"
        )

        self.log.config(
            state="disabled"
        )

    # =============================================
    # CLOSE
    # =============================================

    def close(self):

        try:

            self.api.close()

        except Exception as e:

            print(
                f"[CLOSE ERROR] {e}"
            )

        self.root.destroy()


# =============================================
# START APPLICATION
# =============================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CrytopzDemo(
        root
    )

    root.protocol(
        "WM_DELETE_WINDOW",
        app.close
    )

    root.mainloop()

