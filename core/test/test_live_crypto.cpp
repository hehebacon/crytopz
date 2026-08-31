#include "crytopz/live_market_scheduler.hpp"
#include "crytopz/crypto_market_provider.hpp"
#include "crytopz/winhttp_client.hpp"

#include <chrono>
#include <iostream>
#include <thread>

using namespace crytopz;

int main()
{
    std::cout
        << "========================================\n"
        << " Crytopz Live Market Scheduler Test\n"
        << "========================================\n";


    WinHttpClient http;

    CryptoMarketProvider provider(http);

    MarketData market_data;

    LiveMarketFeed feed(
        provider,
        market_data
    );


    // ========================================================
    // Symbols
    // ========================================================

    feed.add_symbol("BTCUSDT");
    feed.add_symbol("ETHUSDT");
    feed.add_symbol("SOLUSDT");

    std::cout
        << "[PASS] Symbols configured\n";


    // ========================================================
    // Scheduler
    // ========================================================

    LiveMarketScheduler scheduler(
        feed,
        std::chrono::seconds(2)
    );


    if (scheduler.interval_ms() != 2000)
    {
        std::cout
            << "[FAIL] Interval\n";

        return 1;
    }

    std::cout
        << "[PASS] Interval configured\n";


    // ========================================================
    // Start
    // ========================================================

    if (!scheduler.start())
    {
        std::cout
            << "[FAIL] Scheduler start\n";

        return 1;
    }

    std::cout
        << "[PASS] Scheduler started\n";


    // ========================================================
    // Duplicate start
    // ========================================================

    if (scheduler.start())
    {
        std::cout
            << "[FAIL] Duplicate start protection\n";

        scheduler.stop();

        return 1;
    }

    std::cout
        << "[PASS] Duplicate start protection\n";


    // ========================================================
    // Wait for live update
    // ========================================================

    std::this_thread::sleep_for(
        std::chrono::seconds(3)
    );


    // ========================================================
    // Verify market data
    // ========================================================

    if (!market_data.has_symbol("BTCUSDT"))
    {
        std::cout
            << "[FAIL] BTCUSDT update\n";

        scheduler.stop();

        return 1;
    }

    if (!market_data.has_symbol("ETHUSDT"))
    {
        std::cout
            << "[FAIL] ETHUSDT update\n";

        scheduler.stop();

        return 1;
    }

    if (!market_data.has_symbol("SOLUSDT"))
    {
        std::cout
            << "[FAIL] SOLUSDT update\n";

        scheduler.stop();

        return 1;
    }

    std::cout
        << "[PASS] Automatic market updates\n";


    // ========================================================
    // Prices
    // ========================================================

    std::cout
        << "[PRICE] BTCUSDT "
        << market_data.get_price("BTCUSDT")
        << "\n";

    std::cout
        << "[PRICE] ETHUSDT "
        << market_data.get_price("ETHUSDT")
        << "\n";

    std::cout
        << "[PRICE] SOLUSDT "
        << market_data.get_price("SOLUSDT")
        << "\n";


    // ========================================================
    // Stop
    // ========================================================

    scheduler.stop();

    if (scheduler.running())
    {
        std::cout
            << "[FAIL] Scheduler stop\n";

        return 1;
    }

    std::cout
        << "[PASS] Scheduler stopped\n";


    // ========================================================
    // Finish
    // ========================================================

    std::cout
        << "========================================\n"
        << " ALL LIVE MARKET SCHEDULER TESTS PASSED\n"
        << "========================================\n";

    return 0;
}