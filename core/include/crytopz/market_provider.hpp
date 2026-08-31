#pragma once

#include "market.hpp"

#include <string>

namespace crytopz {

class MarketProvider
{
public:

    virtual ~MarketProvider() = default;

    virtual bool start() = 0;

    virtual void stop() = 0;

    virtual bool running() const = 0;

    // Fetch data and update the provider market.
    virtual bool fetch(
        const std::string& symbol
    ) = 0;

    // Fetch data and return the resulting ticker.
    virtual bool fetch(
        const std::string& symbol,
        Ticker& ticker
    ) = 0;
};

} // namespace crytopz