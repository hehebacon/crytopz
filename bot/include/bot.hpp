#pragma once

#include <string>

namespace crytopz::bot {

class Bot {
public:
    virtual ~Bot() = default;

    virtual const std::string& id() const = 0;
    virtual const std::string& name() const = 0;

    virtual bool start() = 0;
    virtual void stop() = 0;

    virtual bool running() const = 0;

    virtual void onMarketUpdate(
        const std::string& symbol,
        double price
    ) = 0;
};

}