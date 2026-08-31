#pragma once

#include "types.hpp"

namespace crytopz {


class MarketFeed
{

public:

    virtual ~MarketFeed() = default;


    virtual void start() = 0;


    virtual void stop() = 0;


};


}