
#pragma once

#include "engine.hpp"
#include "signal.hpp"

#include <string>

namespace crytopz {

enum class RiskStatus {
    Approved,
    InvalidQuantity,
    InvalidPrice,
    InsufficientBalance,
    PositionLimitExceeded,
    ExposureLimitExceeded
};

struct RiskResult {
    RiskStatus status = RiskStatus::Approved;
    std::string reason;

    bool approved() const {
        return status == RiskStatus::Approved;
    }
};

struct RiskLimits {
    // Maximum quantity allowed in one order.
    Quantity max_order_quantity = 1.0;

    // Maximum absolute position quantity.
    Quantity max_position_quantity = 10.0;

    // Maximum notional exposure for one symbol.
    Money max_symbol_exposure = 100'000.0;
};

class RiskManager {
public:
    explicit RiskManager(
        TradingEngine& engine
    );

    RiskResult check(
        const Signal& signal
    ) const;

    const RiskLimits& limits() const;

    void setLimits(
        const RiskLimits& limits
    );

private:
    TradingEngine& engine_;

    RiskLimits limits_;
};

}
