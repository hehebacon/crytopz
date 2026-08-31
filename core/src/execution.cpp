
#include "crytopz/execution.hpp"

namespace crytopz {

ExecutionEngine::ExecutionEngine(
    TradingEngine& engine
)
    : engine_(engine),
      risk_manager_(engine)
{
}


// ============================================================
// EXECUTE
// ============================================================

std::uint64_t ExecutionEngine::execute(
    const Signal& signal
)
{
    // --------------------------------------------------------
    // HOLD
    // --------------------------------------------------------

    if (signal.type == SignalType::Hold)
        return 0;


    // --------------------------------------------------------
    // RISK CHECK
    // --------------------------------------------------------

    last_risk_result_ =
        risk_manager_.check(signal);

    if (!last_risk_result_.approved())
        return 0;


    // --------------------------------------------------------
    // BUY
    // --------------------------------------------------------

    if (signal.type == SignalType::Buy)
    {
        return engine_.place_market_order(
            signal.symbol,
            Side::Buy,
            signal.quantity
        );
    }


    // --------------------------------------------------------
    // SELL
    // --------------------------------------------------------

    if (signal.type == SignalType::Sell)
    {
        return engine_.place_market_order(
            signal.symbol,
            Side::Sell,
            signal.quantity
        );
    }


    return 0;
}


// ============================================================
// LAST RISK RESULT
// ============================================================

const RiskResult&
ExecutionEngine::lastRiskResult() const
{
    return last_risk_result_;
}

}


