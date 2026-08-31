
#pragma once

#include "types.hpp"

#include <string>
#include <unordered_map>

namespace crytopz {

struct Position {
    Symbol symbol;

    Quantity quantity = 0.0;
    Price average_price = 0.0;
};

class Account {
public:
    explicit Account(Money initial_balance);

    // ========================================================
    // BALANCE
    // ========================================================

    Money balance() const;

    // ========================================================
    // ORDERS
    // ========================================================

    bool buy(
        const Symbol& symbol,
        Price price,
        Quantity quantity
    );

    bool sell(
        const Symbol& symbol,
        Price price,
        Quantity quantity
    );

    // ========================================================
    // POSITIONS
    // ========================================================

    Position get_position(
        const Symbol& symbol
    ) const;

    // ========================================================
    // PNL
    // ========================================================

    // Realized profit/loss from completed sells.
    Money realized_pnl() const;

    // Unrealized PnL for one open position.
    Money unrealized_pnl(
        const Symbol& symbol,
        Price market_price
    ) const;

    // Current market value of one position.
    Money position_value(
        const Symbol& symbol,
        Price market_price
    ) const;

    // Cash + current market value of one position.
    Money equity(
        const Symbol& symbol,
        Price market_price
    ) const;

    // ========================================================
    // PORTFOLIO
    // ========================================================

    // Total unrealized PnL using supplied market prices.
    Money unrealized_pnl(
        const std::unordered_map<
            std::string,
            Price
        >& market_prices
    ) const;

    // Total account equity using supplied market prices.
    Money equity(
        const std::unordered_map<
            std::string,
            Price
        >& market_prices
    ) const;

    // Initial capital used by this account.
    Money initial_balance() const;

    // Total PnL = realized + unrealized.
    Money total_pnl(
        const std::unordered_map<
            std::string,
            Price
        >& market_prices
    ) const;

private:
    Money initial_balance_;
    Money balance_;

    Money realized_pnl_;

    std::unordered_map<
        std::string,
        Position
    > positions_;
};

}
