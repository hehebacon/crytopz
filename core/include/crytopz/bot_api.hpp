#pragma once

#include "engine.hpp"

namespace crytopz {


class BotAPI
{

public:

    explicit BotAPI(
        TradingEngine& engine
    );


    Price price(
        const Symbol& symbol
    );


    std::uint64_t buy(
        const Symbol& symbol,
        Quantity quantity
    );


    std::uint64_t sell(
        const Symbol& symbol,
        Quantity quantity
    );


    Money balance();


private:

    TradingEngine& engine_;

};


}