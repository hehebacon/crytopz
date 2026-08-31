#include "crytopz/core_api.hpp"

namespace crytopz {

// ============================================================
// CONSTRUCTOR
// ============================================================

CoreAPI::CoreAPI(
    Money initial_balance
)
    : engine_(initial_balance),
      risk_(engine_),
      account_manager_(),
      execution_router_(account_manager_),
      execution_(engine_)
{
    // Synchronize the default LOCAL account
    // with the CoreAPI starting balance.

    TradingAccount* account =
        account_manager_.get_active_account();

    if (account != nullptr) {
        account->virtual_balance =
            initial_balance;
    }
}


// ============================================================
// MARKET
// ============================================================

void CoreAPI::update_market(
    const std::string& symbol,
    Price bid,
    Price ask,
    Price last,
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


Price CoreAPI::get_price(
    const std::string& symbol
) const
{
    const auto ticker =
        engine_.market().get_ticker(
            Symbol{symbol}
        );

    return ticker.last;
}


// ============================================================
// TRADING
// ============================================================

std::uint64_t CoreAPI::buy(
    const std::string& symbol,
    Quantity quantity
)
{
    Signal signal;

    signal.type =
        SignalType::Buy;

    signal.symbol =
        Symbol{symbol};

    signal.quantity =
        quantity;

    return execution_.execute(
        signal
    );
}


std::uint64_t CoreAPI::sell(
    const std::string& symbol,
    Quantity quantity
)
{
    Signal signal;

    signal.type =
        SignalType::Sell;

    signal.symbol =
        Symbol{symbol};

    signal.quantity =
        quantity;

    return execution_.execute(
        signal
    );
}


// ============================================================
// ACCOUNT
// ============================================================

Money CoreAPI::balance() const
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


Money CoreAPI::realized_pnl() const
{
    return engine_.account().realized_pnl();
}


Money CoreAPI::unrealized_pnl(
    const std::unordered_map<
        std::string,
        Price
    >& prices
) const
{
    return engine_.account().unrealized_pnl(
        prices
    );
}


Money CoreAPI::total_pnl(
    const std::unordered_map<
        std::string,
        Price
    >& prices
) const
{
    return engine_.account().total_pnl(
        prices
    );
}


Money CoreAPI::equity(
    const std::unordered_map<
        std::string,
        Price
    >& prices
) const
{
    return engine_.account().equity(
        prices
    );
}


// ============================================================
// TRADING ACCOUNT SYSTEM
// ============================================================

TradingAccountManager&
CoreAPI::accounts()
{
    return account_manager_;
}


const TradingAccountManager&
CoreAPI::accounts() const
{
    return account_manager_;
}


ExecutionRouter&
CoreAPI::router()
{
    return execution_router_;
}


const ExecutionRouter&
CoreAPI::router() const
{
    return execution_router_;
}


bool CoreAPI::set_active_account(
    const std::string& id
)
{
    return account_manager_.set_active_account(
        id
    );
}


const TradingAccount*
CoreAPI::active_account() const
{
    return account_manager_.get_active_account();
}


// ============================================================
// RISK
// ============================================================

RiskResult CoreAPI::check_order(
    const Signal& signal
) const
{
    return risk_.check(
        signal
    );
}


const RiskLimits&
CoreAPI::risk_limits() const
{
    return risk_.limits();
}


void CoreAPI::set_risk_limits(
    const RiskLimits& limits
)
{
    risk_.setLimits(
        limits
    );
}


// ============================================================
// ENGINE ACCESS
// ============================================================

TradingEngine&
CoreAPI::engine()
{
    return engine_;
}


const TradingEngine&
CoreAPI::engine() const
{
    return engine_;
}

}
