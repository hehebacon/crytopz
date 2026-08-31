
#pragma once

#include "types.hpp"

#include <cstdint>

namespace crytopz {

struct Order {

    // ========================================================
    // ID
    // ========================================================

    std::uint64_t id = 0;


    // ========================================================
    // MARKET
    // ========================================================

    Symbol symbol;

    Side side = Side::Buy;

    OrderType type = OrderType::Market;


    // ========================================================
    // EXECUTION
    // ========================================================

    Price price = 0.0;

    Quantity quantity = 0.0;


    // ========================================================
    // STATUS
    // ========================================================

    OrderStatus status = OrderStatus::Pending;


    // ========================================================
    // TIMESTAMP
    // ========================================================
    //
    // Unix timestamp in milliseconds.
    //
    // 0 means the order has no timestamp.
    //

    std::uint64_t timestamp = 0;
};

} // namespace crytopz

