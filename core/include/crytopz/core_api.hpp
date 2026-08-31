#pragma once

#include "engine.hpp"
#include "order.hpp"
#include "crypto_market_provider.hpp"
#include "live_market_feed.hpp"
#include "live_market_scheduler.hpp"
#include "winhttp_client.hpp"

#include <chrono>
#include <cstddef>
#include <cstdint>
#include <string>

namespace crytopz {

class CoreAPI
{
public:


explicit CoreAPI(
    double initial_balance
);

~CoreAPI();


// ========================================================
// MARKET
// ========================================================

void update_market(
    const std::string& symbol,
    double bid,
    double ask,
    double last,
    std::uint64_t timestamp
);

double get_price(
    const std::string& symbol
) const;


// ========================================================
// LIVE MARKET
// ========================================================

bool start_live_market();

void stop_live_market();

bool live_market_running() const;

std::size_t live_market_interval_ms() const;


// ========================================================
// TRADING
// ========================================================

std::uint64_t buy(
    const std::string& symbol,
    double quantity
);

std::uint64_t sell(
    const std::string& symbol,
    double quantity
);


// ========================================================
// ACCOUNT
// ========================================================

double balance() const;

Position position(
    const std::string& symbol
) const;

double realized_pnl() const;


// ========================================================
// PORTFOLIO / FINANCIAL STATE
// ========================================================

double unrealized_pnl() const;

double position_value() const;

double equity() const;

double total_pnl() const;


// ========================================================
// ORDER HISTORY
// ========================================================

std::size_t order_count() const;

const Order* get_order(
    std::size_t index
) const;


private:


TradingEngine engine_;

WinHttpClient http_client_;

CryptoMarketProvider market_provider_;

LiveMarketFeed live_market_feed_;

LiveMarketScheduler live_market_scheduler_;


};

} // namespace crytopz
