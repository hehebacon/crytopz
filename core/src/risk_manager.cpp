#include "crytopz/risk_manager.hpp"

namespace crytopz {

RiskManager::RiskManager(
    TradingEngine& engine
)
    : engine_(engine)
{
}


// ============================================================
// LIMITS
// ============================================================

const RiskLimits&
RiskManager::limits() const
{
    return limits_;
}


void RiskManager::setLimits(
    const RiskLimits& limits
)
{
    limits_ = limits;
}


// ============================================================
// RISK CHECK
// ============================================================

RiskResult RiskManager::check(
    const Signal& signal
) const
{
    // --------------------------------------------------------
    // Quantity
    // --------------------------------------------------------

    if (signal.quantity <= 0.0)
    {
        return {
            RiskStatus::InvalidQuantity,
            "Order quantity must be greater than zero"
        };
    }

    if (
        signal.quantity >
        limits_.max_order_quantity
    )
    {
        return {
            RiskStatus::PositionLimitExceeded,
            "Order quantity exceeds maximum order quantity"
        };
    }


    // --------------------------------------------------------
    // Market price
    // --------------------------------------------------------

    const auto ticker =
        engine_.market().get_ticker(
            signal.symbol
        );

    if (ticker.last <= 0.0)
    {
        return {
            RiskStatus::InvalidPrice,
            "Market price is invalid"
        };
    }


    // --------------------------------------------------------
    // Current position
    // --------------------------------------------------------

    const Position position =
        engine_.account().get_position(
            signal.symbol
        );


    // ========================================================
    // BUY
    // ========================================================

    if (
        signal.type ==
        SignalType::Buy
    )
    {
        const Quantity new_position =
            position.quantity +
            signal.quantity;

        if (
            new_position >
            limits_.max_position_quantity
        )
        {
            return {
                RiskStatus::PositionLimitExceeded,
                "Position limit exceeded"
            };
        }


        const Money order_value =
            ticker.last *
            signal.quantity;

        if (
            order_value >
            engine_.account().balance()
        )
        {
            return {
                RiskStatus::InsufficientBalance,
                "Insufficient account balance"
            };
        }


        if (
            order_value >
            limits_.max_symbol_exposure
        )
        {
            return {
                RiskStatus::ExposureLimitExceeded,
                "Symbol exposure limit exceeded"
            };
        }
    }


    // ========================================================
    // SELL
    // ========================================================

    else if (
        signal.type ==
        SignalType::Sell
    )
    {
        if (
            signal.quantity >
            position.quantity
        )
        {
            return {
                RiskStatus::PositionLimitExceeded,
                "Sell quantity exceeds current position"
            };
        }
    }


    // ========================================================
    // UNKNOWN SIGNAL
    // ========================================================

    else
    {
        return {
            RiskStatus::InvalidQuantity,
            "Unsupported signal type"
        };
    }


    // ========================================================
    // APPROVED
    // ========================================================

    return {
        RiskStatus::Approved,
        "Risk check passed"
    };
}

}