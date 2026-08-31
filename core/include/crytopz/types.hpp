#pragma once

#include <string>
#include <cstdint>

namespace crytopz {

using Price = double;
using Quantity = double;
using Money = double;

enum class Side {
    Buy,
    Sell
};

enum class OrderType {
    Market,
    Limit
};

enum class OrderStatus
{
    Pending,
    Filled,
    Cancelled
};

struct Symbol {
    std::string value;
};

}