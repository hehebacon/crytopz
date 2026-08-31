
#pragma once

#include "signal.hpp"
#include "engine.hpp"
#include "risk_manager.hpp"

#include <cstdint>

namespace crytopz {

class ExecutionEngine
{
public:

    explicit ExecutionEngine(
        TradingEngine& engine
    );


    // ========================================================
    // EXECUTE ORDER
    // ========================================================

    std::uint64_t execute(
        const Signal& signal
    );


    // ========================================================
    // LAST RISK RESULT
    // ========================================================

    const RiskResult& lastRiskResult() const;


private:

    TradingEngine& engine_;

    RiskManager risk_manager_;

    RiskResult last_risk_result_;
};

}

