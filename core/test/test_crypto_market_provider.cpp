#include "crytopz/crypto_market_provider.hpp"

#include <cassert>
#include <iostream>
#include <string>

using namespace crytopz;


// ============================================================
// FAKE HTTP CLIENT
// ============================================================

class FakeHttpClient : public HttpClient
{
public:

    HttpResponse get(
        const std::string& url
    ) override
    {
        last_url = url;

        HttpResponse response;

        response.success = true;
        response.status_code = 200;

        response.body =
            R"({
                "symbol": "BTCUSDT",
                "price": "100000.00"
            })";

        return response;
    }

    std::string last_url;
};


// ============================================================
// TEST
// ============================================================

int main()
{
    std::cout
        << "========================================\n"
        << " Crytopz Crypto Provider Test\n"
        << "========================================\n";


    MarketData market;

    FakeHttpClient http_client;


    CryptoMarketProvider provider(
        http_client,
        market
    );


    // ========================================================
    // Initial state
    // ========================================================

    assert(
        !provider.running()
    );

    std::cout
        << "[PASS] Initial state\n";


    // ========================================================
    // Start
    // ========================================================

    assert(
        provider.start()
    );

    assert(
        provider.running()
    );

    std::cout
        << "[PASS] Start\n";


    // ========================================================
    // Double start should fail
    // ========================================================

    assert(
        !provider.start()
    );

    assert(
        provider.running()
    );

    std::cout
        << "[PASS] Duplicate start protection\n";


    // ========================================================
    // Empty symbol
    // ========================================================

    assert(
        !provider.fetch("")
    );

    std::cout
        << "[PASS] Invalid symbol protection\n";


    // ========================================================
    // Fetch
    // ========================================================

    assert(
        provider.fetch("BTCUSDT")
    );

    assert(
        http_client.last_url
        ==
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    );

    std::cout
        << "[PASS] HTTP fetch\n";


    // ========================================================
    // MarketData updated
    // ========================================================

    assert(
        market.has_symbol("BTCUSDT")
    );

    assert(
        market.get_price("BTCUSDT")
        ==
        100000.0
    );

    std::cout
        << "[PASS] MarketData update\n";


    // ========================================================
    // Direct ticker fetch
    // ========================================================

    Ticker ticker;

    assert(
        provider.fetch(
            "BTCUSDT",
            ticker
        )
    );

    assert(
        ticker.symbol.value
        ==
        "BTCUSDT"
    );

    assert(
        ticker.last
        ==
        100000.0
    );

    assert(
        ticker.timestamp > 0
    );

    std::cout
        << "[PASS] Direct ticker fetch\n";


    // ========================================================
    // Stop
    // ========================================================

    provider.stop();

    assert(
        !provider.running()
    );

    std::cout
        << "[PASS] Stop\n";


    // ========================================================
    // Fetch while stopped
    // ========================================================

    assert(
        !provider.fetch("BTCUSDT")
    );

    std::cout
        << "[PASS] Fetch while stopped\n";


    std::cout
        << "========================================\n"
        << " ALL CRYPTO PROVIDER TESTS PASSED\n"
        << "========================================\n";


    return 0;
}