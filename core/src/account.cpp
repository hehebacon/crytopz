
#include "crytopz/account.hpp"

namespace crytopz {

Account::Account(
    Money initial_balance
)
    : initial_balance_(initial_balance),
      balance_(initial_balance),
      realized_pnl_(0.0)
{
}


// ============================================================
// BALANCE
// ============================================================

Money Account::balance() const
{
    return balance_;
}

Money Account::initial_balance() const
{
    return initial_balance_;
}


// ============================================================
// BUY
// ============================================================

bool Account::buy(
    const Symbol& symbol,
    Price price,
    Quantity quantity
)
{
    if (quantity <= 0.0)
        return false;

    if (price <= 0.0)
        return false;

    const Money cost =
        price * quantity;

    if (cost > balance_)
        return false;

    balance_ -= cost;

    auto& position =
        positions_[symbol.value];

    position.symbol = symbol;

    const Quantity old_quantity =
        position.quantity;

    const Quantity new_quantity =
        old_quantity + quantity;

    if (new_quantity > 0.0)
    {
        position.average_price =
            (
                position.average_price *
                old_quantity
                +
                price * quantity
            )
            /
            new_quantity;
    }

    position.quantity =
        new_quantity;

    return true;
}


// ============================================================
// SELL
// ============================================================

bool Account::sell(
    const Symbol& symbol,
    Price price,
    Quantity quantity
)
{
    if (quantity <= 0.0)
        return false;

    if (price <= 0.0)
        return false;

    auto it =
        positions_.find(symbol.value);

    if (it == positions_.end())
        return false;

    Position& position =
        it->second;

    if (position.quantity < quantity)
        return false;

    // --------------------------------------------------------
    // Calculate realized PnL before reducing position.
    // --------------------------------------------------------

    const Money pnl =
        (price - position.average_price)
        * quantity;

    realized_pnl_ += pnl;

    // --------------------------------------------------------
    // Receive sale proceeds.
    // --------------------------------------------------------

    balance_ +=
        price * quantity;

    // --------------------------------------------------------
    // Reduce position.
    // --------------------------------------------------------

    position.quantity -= quantity;

    // --------------------------------------------------------
    // If position is completely closed,
    // reset average price.
    // --------------------------------------------------------

    if (position.quantity <= 0.0)
    {
        position.quantity = 0.0;
        position.average_price = 0.0;
    }

    return true;
}


// ============================================================
// POSITION
// ============================================================

Position Account::get_position(
    const Symbol& symbol
) const
{
    auto it =
        positions_.find(symbol.value);

    if (it == positions_.end())
        return {};

    return it->second;
}


// ============================================================
// REALIZED PNL
// ============================================================

Money Account::realized_pnl() const
{
    return realized_pnl_;
}


// ============================================================
// UNREALIZED PNL
// ============================================================

Money Account::unrealized_pnl(
    const Symbol& symbol,
    Price market_price
) const
{
    if (market_price <= 0.0)
        return 0.0;

    const Position position =
        get_position(symbol);

    if (position.quantity <= 0.0)
        return 0.0;

    return
        (
            market_price -
            position.average_price
        )
        *
        position.quantity;
}


// ============================================================
// POSITION VALUE
// ============================================================

Money Account::position_value(
    const Symbol& symbol,
    Price market_price
) const
{
    if (market_price <= 0.0)
        return 0.0;

    const Position position =
        get_position(symbol);

    if (position.quantity <= 0.0)
        return 0.0;

    return
        market_price *
        position.quantity;
}


// ============================================================
// SINGLE POSITION EQUITY
// ============================================================

Money Account::equity(
    const Symbol& symbol,
    Price market_price
) const
{
    return
        balance_ +
        position_value(
            symbol,
            market_price
        );
}


// ============================================================
// TOTAL UNREALIZED PNL
// ============================================================

Money Account::unrealized_pnl(
    const std::unordered_map<
        std::string,
        Price
    >& market_prices
) const
{
    Money result = 0.0;

    for (const auto& entry : positions_)
    {
        const std::string& symbol =
            entry.first;

        const Position& position =
            entry.second;

        if (position.quantity <= 0.0)
            continue;

        auto price_it =
            market_prices.find(symbol);

        if (price_it == market_prices.end())
            continue;

        const Price market_price =
            price_it->second;

        if (market_price <= 0.0)
            continue;

        result +=
            (
                market_price -
                position.average_price
            )
            *
            position.quantity;
    }

    return result;
}


// ============================================================
// TOTAL EQUITY
// ============================================================

Money Account::equity(
    const std::unordered_map<
        std::string,
        Price
    >& market_prices
) const
{
    Money result =
        balance_;

    for (const auto& entry : positions_)
    {
        const std::string& symbol =
            entry.first;

        const Position& position =
            entry.second;

        if (position.quantity <= 0.0)
            continue;

        auto price_it =
            market_prices.find(symbol);

        if (price_it == market_prices.end())
            continue;

        const Price market_price =
            price_it->second;

        if (market_price <= 0.0)
            continue;

        result +=
            market_price *
            position.quantity;
    }

    return result;
}


// ============================================================
// TOTAL PNL
// ============================================================

Money Account::total_pnl(
    const std::unordered_map<
        std::string,
        Price
    >& market_prices
) const
{
    return
        realized_pnl_ +
        unrealized_pnl(
            market_prices
        );
}

}


