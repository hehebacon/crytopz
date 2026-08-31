
#include "crytopz/core_api.hpp"

#include <chrono>
#include <cstdint>
#include <iostream>
#include <thread>

using namespace crytopz;

int main()
{
    std::cout
        << "========================================\n"
        << " Crytopz CoreAPI Live Market Test\n"
        << "========================================\n\n";


    // ========================================================
    // CREATE CORE
    // ========================================================

    CoreAPI core(10000.0);

    std::cout
        << "[PASS] CoreAPI created\n";


    // ========================================================
    // INITIAL ACCOUNT
    // ========================================================

    std::cout
        << "[ACCOUNT]\n"
        << "Balance: "
        << core.balance()
        << "\n"
        << "Equity: "
        << core.equity()
        << "\n\n";


    // ========================================================
    // START LIVE MARKET
    // ========================================================

    if (!core.start_live_market())
    {
        std::cout
            << "[FAIL] Live market start\n";

        return 1;
    }

    std::cout
        << "[PASS] Live market started\n"
        << "[LIVE MARKET] Running: "
        << (core.live_market_running() ? "YES" : "NO")
        << "\n"
        << "[LIVE MARKET] Interval: "
        << core.live_market_interval_ms()
        << " ms\n\n";


    // ========================================================
    // WAIT FOR LIVE DATA
    // ========================================================

    std::cout
        << "[WAIT] Waiting for live market data...\n";

    bool btc_received = false;

    for (int i = 0; i < 20; ++i)
    {
        const double price =
            core.get_price("BTCUSDT");

        if (price > 0.0)
        {
            btc_received = true;

            std::cout
                << "[PASS] BTCUSDT price received: "
                << price
                << "\n";

            break;
        }

        std::this_thread::sleep_for(
            std::chrono::milliseconds(500)
        );
    }


    if (!btc_received)
    {
        std::cout
            << "[FAIL] BTCUSDT price not received\n";

        core.stop_live_market();

        return 1;
    }


    // ========================================================
    // OTHER SYMBOLS
    // ========================================================

    std::cout
        << "\n[MARKET]\n";

    std::cout
        << "BTCUSDT: "
        << core.get_price("BTCUSDT")
        << "\n";

    std::cout
        << "ETHUSDT: "
        << core.get_price("ETHUSDT")
        << "\n";

    std::cout
        << "SOLUSDT: "
        << core.get_price("SOLUSDT")
        << "\n";

    std::cout
        << "BNBUSDT: "
        << core.get_price("BNBUSDT")
        << "\n";

    std::cout
        << "XRPUSDT: "
        << core.get_price("XRPUSDT")
        << "\n";


    // ========================================================
    // BUY
    // ========================================================

    std::cout
        << "\n[TRADING]\n";

    const std::uint64_t buy_id =
        core.buy(
            "BTCUSDT",
            0.01
        );

    if (buy_id == 0)
    {
        std::cout
            << "[FAIL] BUY order\n";

        core.stop_live_market();

        return 1;
    }

    std::cout
        << "[PASS] BUY order\n"
        << "Order ID: "
        << buy_id
        << "\n";


    // ========================================================
    // ACCOUNT AFTER BUY
    // ========================================================

    std::cout
        << "\n[AFTER BUY]\n"
        << "Balance: "
        << core.balance()
        << "\n"
        << "Position: "
        << core.position("BTCUSDT").quantity
        << "\n"
        << "Average Price: "
        << core.position("BTCUSDT").average_price
        << "\n"
        << "Position Value: "
        << core.position_value()
        << "\n"
        << "Unrealized PNL: "
        << core.unrealized_pnl()
        << "\n"
        << "Equity: "
        << core.equity()
        << "\n";


    // ========================================================
    // WAIT FOR MARKET UPDATE
    // ========================================================

    std::cout
        << "\n[WAIT] Waiting for another market update...\n";

    std::this_thread::sleep_for(
        std::chrono::seconds(2)
    );


    std::cout
        << "[MARKET] BTCUSDT: "
        << core.get_price("BTCUSDT")
        << "\n";

    std::cout
        << "[PNL] Unrealized: "
        << core.unrealized_pnl()
        << "\n";


    // ========================================================
    // SELL
    // ========================================================

    const std::uint64_t sell_id =
        core.sell(
            "BTCUSDT",
            0.01
        );

    if (sell_id == 0)
    {
        std::cout
            << "[FAIL] SELL order\n";

        core.stop_live_market();

        return 1;
    }

    std::cout
        << "\n[PASS] SELL order\n"
        << "Order ID: "
        << sell_id
        << "\n";


    // ========================================================
    // FINAL ACCOUNT
    // ========================================================

    std::cout
        << "\n[FINAL ACCOUNT]\n"
        << "Balance: "
        << core.balance()
        << "\n"
        << "Position: "
        << core.position("BTCUSDT").quantity
        << "\n"
        << "Realized PNL: "
        << core.realized_pnl()
        << "\n"
        << "Unrealized PNL: "
        << core.unrealized_pnl()
        << "\n"
        << "Total PNL: "
        << core.total_pnl()
        << "\n"
        << "Equity: "
        << core.equity()
        << "\n";


    // ========================================================
    // ORDER HISTORY
    // ========================================================

    std::cout
        << "\n[ORDERS]\n"
        << "Order count: "
        << core.order_count()
        << "\n";

    for (std::size_t i = 0;
         i < core.order_count();
         ++i)
    {
        const Order* order =
            core.get_order(i);

        if (!order)
            continue;

        std::cout
            << "Order #"
            << order->id
            << " | "
            << order->symbol.value
            << " | Qty: "
            << order->quantity
            << " | Price: "
            << order->price
            << "\n";
    }


    // ========================================================
    // STOP
    // ========================================================

    core.stop_live_market();

    if (core.live_market_running())
    {
        std::cout
            << "[FAIL] Live market stop\n";

        return 1;
    }

    std::cout
        << "\n[PASS] Live market stopped\n";


    // ========================================================
    // SUCCESS
    // ========================================================

    std::cout
        << "\n========================================\n"
        << " ALL COREAPI TESTS PASSED\n"
        << "========================================\n";

    return 0;
}

