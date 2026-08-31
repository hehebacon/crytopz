#include "crytopz/market.hpp"

#include <cassert>
#include <cmath>
#include <iostream>

using namespace crytopz;

int main()
{
    std::cout
        << "========================================\n"
        << " Crytopz Market Data Test\n"
        << "========================================\n";

    MarketData market;

    Symbol btc{"BTCUSDT"};

    // ========================================================
    // First update
    // ========================================================

    market.update(
        btc,
        100000.0,
        100010.0,
        100005.0,
        1000
    );

    auto ticker =
        market.get_ticker(btc);

    assert(
        std::abs(
            ticker.last - 100005.0
        ) < 0.000001
    );

    assert(
        ticker.direction ==
        PriceDirection::Unchanged
    );

    std::cout
        << "[PASS] First market update\n";


    // ========================================================
    // Second update
    // ========================================================

    market.update(
        btc,
        100100.0,
        100110.0,
        100105.0,
        2000
    );

    ticker =
        market.get_ticker(btc);

    assert(
        std::abs(
            ticker.previous_last - 100005.0
        ) < 0.000001
    );

    assert(
        std::abs(
            ticker.change - 100.0
        ) < 0.000001
    );

    assert(
        ticker.direction ==
        PriceDirection::Up
    );

    std::cout
        << "[PASS] Price increase\n";


    // ========================================================
    // get_price
    // ========================================================

    assert(
        std::abs(
            market.get_price("BTCUSDT")
            - 100105.0
        ) < 0.000001
    );

    std::cout
        << "[PASS] get_price\n";


    // ========================================================
    // Unknown symbol
    // ========================================================

    assert(
        market.get_price("UNKNOWN")
        == 0.0
    );

    assert(
        !market.has_symbol("UNKNOWN")
    );

    std::cout
        << "[PASS] Unknown symbol\n";


    // ========================================================
    // Multiple symbols
    // ========================================================

    market.update(
        Symbol{"ETHUSDT"},
        4000.0,
        4001.0,
        4000.5,
        3000
    );

    assert(
        market.has_symbol("BTCUSDT")
    );

    assert(
        market.has_symbol("ETHUSDT")
    );

    assert(
        market.size() == 2
    );

    std::cout
        << "[PASS] Multiple symbols\n";


    // ========================================================
    // Clear
    // ========================================================

    market.clear();

    assert(
        market.size() == 0
    );

    assert(
        market.get_price("BTCUSDT")
        == 0.0
    );

    std::cout
        << "[PASS] Clear\n";


    std::cout
        << "========================================\n"
        << " ALL MARKET DATA TESTS PASSED\n"
        << "========================================\n";

    return 0;
}