#include "crytopz/core_api.hpp"

#include <chrono>

namespace crytopz {

// ============================================================
// CONSTRUCTOR
// ============================================================

CoreAPI::CoreAPI(
    double initial_balance
)
    : engine_(initial_balance),
      http_client_(),
      market_provider_(
          http_client_,
          engine_.market()
      ),
      live_market_feed_(
          market_provider_,
          engine_.market()
      ),
      live_market_scheduler_(
          live_market_feed_,
          // ----------------------------------------------------
          // 1000 ms = 1 second
          //
          // Do NOT use 1 ms here.
          // The market provider performs HTTP requests, so a
          // 1 ms scheduler would generate an excessive amount
          // of requests.
          // ----------------------------------------------------
          std::chrono::milliseconds(1000)
      )
{
    // ========================================================
    // DEFAULT LIVE SYMBOLS
    // ========================================================

    live_market_feed_.add_symbol("BTCUSDT");
    live_market_feed_.add_symbol("ETHUSDT");
    live_market_feed_.add_symbol("SOLUSDT");
    live_market_feed_.add_symbol("BNBUSDT");
    live_market_feed_.add_symbol("XRPUSDT");
}


// ============================================================
// DESTRUCTOR
// ============================================================

CoreAPI::~CoreAPI()
{
    // --------------------------------------------------------
    // Always stop the scheduler first.
    // --------------------------------------------------------

    live_market_scheduler_.stop();

    // --------------------------------------------------------
    // Then stop the feed.
    // --------------------------------------------------------

    live_market_feed_.stop();

    // --------------------------------------------------------
    // Finally stop the provider.
    // --------------------------------------------------------

    market_provider_.stop();
}


// ============================================================
// MARKET
// ============================================================

void CoreAPI::update_market(
    const std::string& symbol,
    double bid,
    double ask,
    double last,
    std::uint64_t timestamp
)
{
    engine_.update_market(
        Symbol{symbol},
        bid,
        ask,
        last,
        timestamp
    );
}


double CoreAPI::get_price(
    const std::string& symbol
) const
{
    return engine_.market().get_price(
        symbol
    );
}


// ============================================================
// LIVE MARKET
// ============================================================

bool CoreAPI::start_live_market()
{
    return live_market_scheduler_.start();
}


void CoreAPI::stop_live_market()
{
    live_market_scheduler_.stop();
}


bool CoreAPI::live_market_running() const
{
    return live_market_scheduler_.running();
}


std::size_t CoreAPI::live_market_interval_ms() const
{
    return live_market_scheduler_.interval_ms();
}


// ============================================================
// TRADING
// ============================================================

std::uint64_t CoreAPI::buy(
    const std::string& symbol,
    double quantity
)
{
    return engine_.place_market_order(
        Symbol{symbol},
        Side::Buy,
        quantity
    );
}


std::uint64_t CoreAPI::sell(
    const std::string& symbol,
    double quantity
)
{
    return engine_.place_market_order(
        Symbol{symbol},
        Side::Sell,
        quantity
    );
}


// ============================================================
// ACCOUNT
// ============================================================

double CoreAPI::balance() const
{
    return engine_.account().balance();
}


Position CoreAPI::position(
    const std::string& symbol
) const
{
    return engine_.account().get_position(
        Symbol{symbol}
    );
}


double CoreAPI::realized_pnl() const
{
    return engine_.account().realized_pnl();
}


// ============================================================
// PORTFOLIO / FINANCIAL STATE
// ============================================================

double CoreAPI::unrealized_pnl() const
{
    double total = 0.0;

    const auto symbols =
        engine_.market().symbols();

    for (const auto& symbol : symbols)
    {
        const Position position =
            engine_.account().get_position(
                Symbol{symbol}
            );

        if (position.quantity <= 0.0)
            continue;

        const Price market_price =
            engine_.market().get_price(
                symbol
            );

        if (market_price <= 0.0)
            continue;

        total +=
            (
                market_price -
                position.average_price
            )
            *
            position.quantity;
    }

    return total;
}


double CoreAPI::position_value() const
{
    double total = 0.0;

    const auto symbols =
        engine_.market().symbols();

    for (const auto& symbol : symbols)
    {
        const Position position =
            engine_.account().get_position(
                Symbol{symbol}
            );

        if (position.quantity <= 0.0)
            continue;

        const Price market_price =
            engine_.market().get_price(
                symbol
            );

        if (market_price <= 0.0)
            continue;

        total +=
            market_price *
            position.quantity;
    }

    return total;
}


double CoreAPI::equity() const
{
    return
        engine_.account().balance()
        +
        position_value();
}


double CoreAPI::total_pnl() const
{
    return
        realized_pnl()
        +
        unrealized_pnl();
}


// ============================================================
// ORDER HISTORY
// ============================================================

std::size_t CoreAPI::order_count() const
{
    return engine_.order_history().size();
}


const Order*
CoreAPI::get_order(
    std::size_t index
) const
{
    const auto& orders =
        engine_.order_history();

    if (index >= orders.size())
        return nullptr;

    return &orders[index];
}

} // namespace crytopz