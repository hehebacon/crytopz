#include "crytopz/simulator_feed.hpp"


namespace crytopz {



SimulatorFeed::SimulatorFeed(
    TradingEngine& engine
)
:
engine_(engine)
{

}



void SimulatorFeed::start()
{
    running_ = true;
}



void SimulatorFeed::stop()
{
    running_ = false;
}



void SimulatorFeed::tick()
{

    if(!running_)
        return;



    timestamp_++;



    // BTC simulation

    btc_price_ += 5;


    engine_.update_market(
        Symbol{"BTCUSDT"},
        btc_price_ - 5,
        btc_price_ + 5,
        btc_price_,
        timestamp_
    );



    // ETH simulation

    eth_price_ += 1;


    engine_.update_market(
        Symbol{"ETHUSDT"},
        eth_price_ - 1,
        eth_price_ + 1,
        eth_price_,
        timestamp_
    );

}



}
