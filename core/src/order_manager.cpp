
#include "crytopz/order_manager.hpp"

namespace crytopz {


// ============================================================
// CREATE ORDER
// ============================================================

std::uint64_t OrderManager::create_order(
    const Symbol& symbol,
    Side side,
    OrderType type,
    Price price,
    Quantity quantity,
    std::uint64_t timestamp
)
{
    Order order;

    order.id =
        next_order_id_++;

    order.symbol =
        symbol;

    order.side =
        side;

    order.type =
        type;

    order.price =
        price;

    order.quantity =
        quantity;

    order.status =
        OrderStatus::Filled;

    order.timestamp =
        timestamp;


    orders_.push_back(
        order
    );


    return order.id;
}


// ============================================================
// CANCEL ORDER
// ============================================================

bool OrderManager::cancel_order(
    std::uint64_t order_id
)
{
    for (auto& order : orders_)
    {
        if (order.id != order_id)
            continue;


        // Filled orders cannot be cancelled.
        if (order.status ==
            OrderStatus::Filled)
        {
            return false;
        }


        order.status =
            OrderStatus::Cancelled;


        return true;
    }


    return false;
}


// ============================================================
// GET ORDER BY ID
// ============================================================

Order OrderManager::get_order(
    std::uint64_t order_id
) const
{
    for (const auto& order : orders_)
    {
        if (order.id ==
            order_id)
        {
            return order;
        }
    }


    return {};
}


// ============================================================
// GET ORDER BY INDEX
// ============================================================

const Order*
OrderManager::get_order_by_index(
    std::size_t index
) const
{
    if (index >= orders_.size())
        return nullptr;


    return &orders_[index];
}


// ============================================================
// GET ALL ORDERS
// ============================================================

const std::vector<Order>&
OrderManager::get_orders() const
{
    return orders_;
}

} // namespace crytopz


