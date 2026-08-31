#pragma once

#include "market.hpp"
#include "signal.hpp"


namespace crytopz {


class Strategy
{

public:

    virtual ~Strategy() = default;


    virtual Signal on_price(
        const Ticker& ticker
    ) = 0;


};


}