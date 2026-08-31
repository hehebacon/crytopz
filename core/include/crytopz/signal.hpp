#pragma once

#include "types.hpp"

namespace crytopz {


enum class SignalType
{
    Buy,
    Sell,
    Hold
};


struct Signal
{
    SignalType type;

    Symbol symbol;

    Quantity quantity = 0;
};


}