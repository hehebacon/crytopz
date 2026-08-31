#pragma once

#include "market.hpp"
#include "market_provider.hpp"

#include <cstdint>
#include <string>
#include <vector>

namespace crytopz {

class LiveMarketFeed
{
public:

    LiveMarketFeed(
        MarketProvider& provider,
        MarketData& market_data
    );

    bool start();

    void stop();

    bool running() const;

    // Fetch toàn bộ symbols một lần
    std::size_t update();

    // Thêm / xóa symbol
    bool add_symbol(
        const std::string& symbol
    );

    bool remove_symbol(
        const std::string& symbol
    );

    const std::vector<std::string>& symbols() const;

private:

    MarketProvider& provider_;
    MarketData& market_data_;

    std::vector<std::string> symbols_;

    bool running_ = false;
};

}