#include "crytopz/live_market_feed.hpp"
#include "crytopz/crypto_market_provider.hpp"
#include "crytopz/winhttp_client.hpp"

#include <cmath>
#include <iostream>

using namespace crytopz;


// ============================================================
// HELPERS
// ============================================================

bool valid_price(double price)
{
    return std::isfinite(price) && price > 0.0;
}


bool check_price(
    const MarketData& market_data,
    const std::string& symbol
)
{
    const double price =
        market_data.get_price(symbol);

    if (!valid_price(price))
    {
        std::cout
            << "[FAIL] Invalid price: "
            << symbol
            << " = "
            << price
            << "\n";

        return false;
    }

    return true;
}


// ============================================================
// MAIN
// ============================================================

int main()
{
    std::cout
        << "========================================\n"
        << " Crytopz Live Market Feed Test\n"
        << "========================================\n";


    // ========================================================
    // CREATE COMPONENTS
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

    if (!feed.add_symbol("ETHUSDT"))
    {
        std::cout
            << "[FAIL] Add ETHUSDT\n";

        return 1;
    }

    if (!feed.add_symbol("SOLUSDT"))
    {
        std::cout
            << "[FAIL] Add SOLUSDT\n";

        return 1;
    }

    std::cout
        << "[PASS] Symbols added\n";


    // ========================================================
    // DUPLICATE PROTECTION
    // ========================================================

    if (feed.add_symbol("BTCUSDT"))
    {
        std::cout
            << "[FAIL] Duplicate symbol protection\n";

        return 1;
    }

    std::cout
        << "[PASS] Duplicate protection\n";


    // ========================================================
    // SYMBOL COUNT
    // ========================================================

    if (feed.symbols().size() != 3)
    {
        std::cout
            << "[FAIL] Symbol count\n"
            << "Count: "
            << feed.symbols().size()
            << "\n";

        return 1;
    }

    std::cout
        << "[PASS] Symbol count\n";


    // ========================================================
    // START
    // ========================================================

    if (!feed.start())
    {
        std::cout
            << "[FAIL] Feed start\n";

        return 1;
    }

    if (!feed.running())
    {
        std::cout
            << "[FAIL] Feed running state\n";

        return 1;
    }

    std::cout
        << "[PASS] Feed started\n";


    // ========================================================
    // PROVIDER
    // ========================================================

    if (!provider.running())
    {
        std::cout
            << "[FAIL] Provider not running\n";

        return 1;
    }

    std::cout
        << "[PASS] Provider running\n";


    // ========================================================
    // LIVE UPDATE #1
    // ========================================================

    const std::size_t updated =
        feed.update();

    if (updated != 3)
    {
        std::cout
            << "[FAIL] Live update #1\n"
            << "Updated: "
            << updated
            << "\n";

        return 1;
    }

    std::cout
        << "[PASS] Live update #1\n";


    // ========================================================
    // VERIFY MARKET DATA
    // ========================================================

    if (!market_data.has_symbol("BTCUSDT"))
    {
        std::cout
            << "[FAIL] BTCUSDT missing\n";

        return 1;
    }

    if (!market_data.has_symbol("ETHUSDT"))
    {
        std::cout
            << "[FAIL] ETHUSDT missing\n";

        return 1;
    }

    if (!market_data.has_symbol("SOLUSDT"))
    {
        std::cout
            << "[FAIL] SOLUSDT missing\n";

        return 1;
    }

    std::cout
        << "[PASS] MarketData symbols\n";


    // ========================================================
    // VERIFY PRICES
    // ========================================================

    if (!check_price(
            market_data,
            "BTCUSDT"))
    {
        return 1;
    }

    if (!check_price(
            market_data,
            "ETHUSDT"))
    {
        return 1;
    }

    if (!check_price(
            market_data,
            "SOLUSDT"))
    {
        return 1;
    }

    std::cout
        << "[PASS] Market prices valid\n";


    // ========================================================
    // PRINT PRICES
    // ========================================================

    std::cout
        << "\n"
        << "----------------------------------------\n"
        << " LIVE PRICES\n"
        << "----------------------------------------\n";

    std::cout
        << "BTCUSDT: "
        << market_data.get_price("BTCUSDT")
        << "\n";

    std::cout
        << "ETHUSDT: "
        << market_data.get_price("ETHUSDT")
        << "\n";

    std::cout
        << "SOLUSDT: "
        << market_data.get_price("SOLUSDT")
        << "\n";


    // ========================================================
    // LIVE UPDATE #2
    // ========================================================

    const std::size_t updated_again =
        feed.update();

    if (updated_again != 3)
    {
        std::cout
            << "[FAIL] Live update #2\n"
            << "Updated: "
            << updated_again
            << "\n";

        return 1;
    }

    std::cout
        << "[PASS] Live update #2\n";


    // ========================================================
    // REMOVE SYMBOL
    // ========================================================

    if (!feed.remove_symbol("SOLUSDT"))
    {
        std::cout
            << "[FAIL] Remove SOLUSDT\n";

        return 1;
    }

    if (feed.symbols().size() != 2)
    {
        std::cout
            << "[FAIL] Symbol count after removal\n";

        return 1;
    }

    std::cout
        << "[PASS] Symbol removal\n";


    // ========================================================
    // UPDATE AFTER REMOVAL
    // ========================================================

    const std::size_t updated_after_remove =
        feed.update();

    if (updated_after_remove != 2)
    {
        std::cout
            << "[FAIL] Update after symbol removal\n"
            << "Updated: "
            << updated_after_remove
            << "\n";

        return 1;
    }

    std::cout
        << "[PASS] Update after symbol removal\n";


    // ========================================================
    // STOP
    // ========================================================

    feed.stop();

    if (feed.running())
    {
        std::cout
            << "[FAIL] Feed stop\n";

        return 1;
    }

    if (provider.running())
    {
        std::cout
            << "[FAIL] Provider stop\n";

        return 1;
    }

    std::cout
        << "[PASS] Feed stopped\n";


    // ========================================================
    // UPDATE WHILE STOPPED
    // ========================================================

    const std::size_t stopped_update =
        feed.update();

    if (stopped_update != 0)
    {
        std::cout
            << "[FAIL] Update while stopped\n"
            << "Updated: "
            << stopped_update
            << "\n";

        return 1;
    }

    std::cout
        << "[PASS] Update blocked while stopped\n";


    // ========================================================
    // FINAL
    // ========================================================

    std::cout
        << "\n"
        << "========================================\n"
        << " ALL LIVE MARKET FEED TESTS PASSED\n"
        << "========================================\n";


    return 0;
}