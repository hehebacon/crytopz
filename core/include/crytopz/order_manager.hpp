
#pragma once

#include "order.hpp"

#include <vector>
#include <cstdint>

namespace crytopz {

class OrderManager {

public:

    // ========================================================
    // CREATE ORDER
    // ========================================================

    std::uint64_t create_order(
        const Symbol& symbol,
        Side side,
        OrderType type,
        Price price,
        Quantity quantity,
        std::uint64_t timestamp
    );


    // ========================================================
    // CANCEL
    // ========================================================

    bool cancel_order(
        std::uint64_t order_id
    );


    // ========================================================
    // GET ORDER
    // ========================================================

    Order get_order(
        std::uint64_t order_id
    ) const;


    // ========================================================
    // GET ORDER BY INDEX
    // ========================================================

    const Order* get_order_by_index(
        std::size_t index
    ) const;


    // ========================================================
    // ALL ORDERS
    // ========================================================

    const std::vector<Order>& get_orders() const;


private:

    std::vector<Order> orders_;

    std::uint64_t next_order_id_ = 1;
};

} // namespace crytopz

