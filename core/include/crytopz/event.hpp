#pragma once

#include "types.hpp"

namespace crytopz {


enum class EventType
{
    PriceUpdated,
    OrderCreated,
    OrderFilled,
    PositionChanged
};


struct Event
{

    EventType type;

    Symbol symbol;

    Price price = 0.0;

    Quantity quantity = 0.0;

};


}