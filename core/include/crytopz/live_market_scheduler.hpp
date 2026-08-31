#pragma once

#include "live_market_feed.hpp"

#include <chrono>
#include <cstddef>

namespace crytopz {

class LiveMarketScheduler
{
public:

    LiveMarketScheduler(
        LiveMarketFeed& feed,
        std::chrono::milliseconds interval =
            std::chrono::seconds(5)
    );

    ~LiveMarketScheduler();

    bool start();

    void stop();

    bool running() const;

    void tick();

    std::size_t interval_ms() const;

private:

    void run();

private:

    LiveMarketFeed& feed_;

    std::chrono::milliseconds interval_;

    bool running_ = false;

    class Impl;
    Impl* impl_ = nullptr;
};

}