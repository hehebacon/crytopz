#pragma once

#include "market_provider.hpp"
#include "http_client.hpp"
#include "market.hpp"

#include <string>

namespace crytopz {

class CryptoMarketProvider : public MarketProvider
{
public:

    // ========================================================
    // CONSTRUCTORS
    // ========================================================

    explicit CryptoMarketProvider(
        HttpClient& http_client
    );

    CryptoMarketProvider(
        HttpClient& http_client,
        MarketData& market
    );


    // ========================================================
    // LIFECYCLE
    // ========================================================

    bool start() override;

    void stop() override;

    bool running() const override;


    // ========================================================
    // FETCH
    // ========================================================

    bool fetch(
        const std::string& symbol
    ) override;

    bool fetch(
        const std::string& symbol,
        Ticker& ticker
    ) override;


private:

    HttpClient& http_client_;

    MarketData* market_ = nullptr;

    bool running_ = false;
};

} // namespace crytopz