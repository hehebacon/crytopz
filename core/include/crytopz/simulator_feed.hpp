#pragma once

#include "market_feed.hpp"
#include "engine.hpp"

#include <cstdint>


namespace crytopz {


class SimulatorFeed : public MarketFeed
{

public:

    explicit SimulatorFeed(
        TradingEngine& engine
    );


    void start() override;


    void stop() override;


    void tick();



private:

    TradingEngine& engine_;


    bool running_ = false;


    std::uint64_t timestamp_ = 0;


    Price btc_price_ = 100'000.0;


    Price eth_price_ = 4'500.0;

};


}