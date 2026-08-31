#include "crytopz/engine.hpp"

namespace crytopz {

// ============================================================
// CONSTRUCTOR
// ============================================================

TradingEngine::TradingEngine(
    Money initial_balance
)
    : account_(initial_balance)
{
}


// ============================================================
// MARKET UPDATE
// ============================================================

void TradingEngine::update_market(
    const Symbol& symbol,
    Price bid,
    Price ask,
    Price last,
    std::uint64_t timestamp
)
{
    market_.update(
        symbol,
        bid,
        ask,
        last,
        timestamp
    );

    event_bus_.emit(
        Event{
            EventType::PriceUpdated,
            symbol,
            last,
            0.0
        }
    );
}


// ============================================================
// MARKET ORDER
// ============================================================

std::uint64_t TradingEngine::place_market_order(
    const Symbol& symbol,
    Side side,
    Quantity quantity
)
{
    if (quantity <= 0.0)
        return 0;

    const auto ticker =
        market_.get_ticker(symbol);

    const Price execution_price =
        side == Side::Buy
            ? ticker.ask
            : ticker.bid;

    if (execution_price <= 0.0)
        return 0;

    bool success = false;

    // --------------------------------------------------------
    // ACCOUNT EXECUTION
    // --------------------------------------------------------

    if (side == Side::Buy)
    {
        success =
            account_.buy(
                symbol,
                execution_price,
                quantity
            );
    }
    else
    {
        success =
            account_.sell(
                symbol,
                execution_price,
                quantity
            );
    }

    if (!success)
        return 0;

    // --------------------------------------------------------
    // ORDER HISTORY
    // --------------------------------------------------------

    const auto order_id =
        orders_.create_order(
            symbol,
            side,
            OrderType::Market,
            execution_price,
            quantity,
            ticker.timestamp
        );

    // --------------------------------------------------------
    // EVENT
    // --------------------------------------------------------

    event_bus_.emit(
        Event{
            EventType::OrderFilled,
            symbol,
            execution_price,
            quantity
        }
    );

    return order_id;
}


// ============================================================
// CANCEL ORDER
// ============================================================

bool TradingEngine::cancel_order(
    std::uint64_t order_id
)
{
    return orders_.cancel_order(
        order_id
    );
}


// ============================================================
// ACCOUNT
// ============================================================

const Account&
TradingEngine::account() const
{
    return account_;
}


// ============================================================
// MARKET ACCESS
// ============================================================

MarketData&
TradingEngine::market()
{
    return market_;
}


const MarketData&
TradingEngine::market() const
{
    return market_;
}


// ============================================================
// ORDER ACCESS
// ============================================================

const OrderManager&
TradingEngine::orders() const
{
    return orders_;
}


const std::vector<Order>&
TradingEngine::order_history() const
{
    return orders_.get_orders();
}


// ============================================================
// EVENT BUS
// ============================================================

EventBus&
TradingEngine::events()
{
    return event_bus_;
}

} // namespace crytopz