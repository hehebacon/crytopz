#pragma once

#include "types.hpp"

namespace crytopz {

struct PnLResult
{
Money realized = 0.0;
Money unrealized = 0.0;
Money total = 0.0;
};

class PnLCalculator
{
public:


static Money unrealized(
    Quantity quantity,
    Price average_price,
    Price market_price
);

static Money realized(
    Quantity quantity,
    Price entry_price,
    Price exit_price
);

static PnLResult calculate(
    Quantity quantity,
    Price average_price,
    Price market_price,
    Money realized_pnl
);


};

}
