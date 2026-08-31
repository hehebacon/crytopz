#pragma once

#include "event_bus.hpp"
#include "types.hpp"
#include "market.hpp"
#include "order.hpp"
#include "account.hpp"
#include "order_manager.hpp"

#include <cstdint>
#include <vector>


namespace crytopz {

class TradingEngine
{

public:

    explicit TradingEngine(
        Money initial_balance
    );


    // ========================================================
    // MARKET
    // ========================================================

    void update_market(
        const Symbol& symbol,
        Price bid,
        Price ask,
        Price last,
        std::uint64_t timestamp
    );


    // ========================================================
    // TRADING
    // ========================================================

    std::uint64_t place_market_order(
        const Symbol& symbol,
        Side side,
        Quantity quantity
    );


    bool cancel_order(
        std::uint64_t order_id
    );


    // ========================================================
    // ACCOUNT
    // ========================================================

    const Account& account() const;


    // ========================================================
    // MARKET ACCESS
    // ========================================================

    MarketData& market();
    const MarketData& market() const;


    // ========================================================
    // ORDER ACCESS
    // ========================================================

    const OrderManager& orders() const;


    const std::vector<Order>& order_history() const;


    // ========================================================
    // EVENT BUS
    // ========================================================

    EventBus& events();


private:

    // ========================================================
    // CORE SYSTEMS
    // ========================================================

    MarketData market_;

    OrderManager orders_;

    Account account_;

    EventBus event_bus_;
};

}