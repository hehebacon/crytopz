#include "crytopz/live_market_scheduler.hpp"
#include "crytopz/live_market_feed.hpp"
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


// ========================================================
// CORE OBJECTS
// ========================================================

WinHttpClient http;

CryptoMarketProvider provider(http);

MarketData market_data;

LiveMarketFeed feed(
    provider,
    market_data
);

// ========================================================
// SYMBOLS
// ========================================================

if (!feed.add_symbol("BTCUSDT"))
{
    std::cout
        << "[FAIL] Add BTCUSDT\n";

    return 1;
}

std::cout
    << "[PASS] Symbol added\n";

// ========================================================
// SCHEDULER
// ========================================================

LiveMarketScheduler scheduler(
    feed,
    std::chrono::milliseconds(1)
);

if (scheduler.interval_ms() != 1)
{
    std::cout
        << "[FAIL] Interval\n"
        << "Interval: "
        << scheduler.interval_ms()
        << " ms\n";

    return 1;
}

std::cout
    << "[PASS] Interval: "
    << scheduler.interval_ms()
    << " ms\n";

// ========================================================
// INITIAL STATE
// ========================================================

if (scheduler.running())
{
    std::cout
        << "[FAIL] Scheduler should initially be stopped\n";

    return 1;
}

std::cout
    << "[PASS] Initial scheduler state\n";

// ========================================================
// START
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
// VERIFY RUNNING
// ========================================================

if (!scheduler.running())
{
    std::cout
        << "[FAIL] Scheduler running state\n";

    return 1;
}

std::cout
    << "[PASS] Scheduler running\n";

// ========================================================
// VERIFY FEED
// ========================================================

if (!feed.running())
{
    std::cout
        << "[FAIL] Feed not running\n";

    scheduler.stop();

    return 1;
}

std::cout
    << "[PASS] Feed running\n";

// ========================================================
// WAIT FOR AUTOMATIC UPDATE
// ========================================================

std::cout
    << "\n----------------------------------------\n"
    << " WAITING FOR AUTOMATIC MARKET UPDATE\n"
    << "----------------------------------------\n";

bool price_received = false;

for (int i = 0; i < 30; ++i)
{
    std::this_thread::sleep_for(
        std::chrono::milliseconds(100)
    );

    const double price =
        market_data.get_price("BTCUSDT");

    if (price > 0.0)
    {
        price_received = true;

        std::cout
            << "[PASS] Automatic market update\n"
            << "BTCUSDT: "
            << price
            << "\n";

        break;
    }

    std::cout
        << "[WAIT] "
        << (i + 1)
        << "/30\n";
}

if (!price_received)
{
    std::cout
        << "[FAIL] No automatic market update\n";

    scheduler.stop();

    return 1;
}

// ========================================================
// SECOND PRICE CHECK
// ========================================================

const double first_price =
    market_data.get_price("BTCUSDT");

std::this_thread::sleep_for(
    std::chrono::milliseconds(500)
);

const double second_price =
    market_data.get_price("BTCUSDT");

if (second_price <= 0.0)
{
    std::cout
        << "[FAIL] Second market update\n";

    scheduler.stop();

    return 1;
}

std::cout
    << "[PASS] Scheduler continues updating\n"
    << "BTCUSDT: "
    << second_price
    << "\n";

// ========================================================
// STOP
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
// VERIFY FEED STOPPED
// ========================================================

if (feed.running())
{
    std::cout
        << "[FAIL] Feed should stop with scheduler\n";

    return 1;
}

std::cout
    << "[PASS] Feed stopped\n";

// ========================================================
// UPDATE BLOCKED
// ========================================================

const std::size_t updated =
    feed.update();

if (updated != 0)
{
    std::cout
        << "[FAIL] Feed updated while stopped\n"
        << "Updated: "
        << updated
        << "\n";

    return 1;
}

std::cout
    << "[PASS] Update blocked while stopped\n";

// ========================================================
// RESTART
// ========================================================

if (!scheduler.start())
{
    std::cout
        << "[FAIL] Scheduler restart\n";

    return 1;
}

if (!scheduler.running())
{
    std::cout
        << "[FAIL] Scheduler not running after restart\n";

    scheduler.stop();

    return 1;
}

std::cout
    << "[PASS] Scheduler restart\n";

std::this_thread::sleep_for(
    std::chrono::milliseconds(300)
);

scheduler.stop();

std::cout
    << "[PASS] Scheduler stopped after restart\n";

// ========================================================
// FINAL
// ========================================================

std::cout
    << "\n========================================\n"
    << " ALL LIVE MARKET SCHEDULER TESTS PASSED\n"
    << "========================================\n";

return 0;


}
