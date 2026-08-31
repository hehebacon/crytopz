#include "crytopz/pnl.hpp"

namespace crytopz {

Money PnLCalculator::unrealized(
Quantity quantity,
Price average_price,
Price market_price
)
{
return (market_price - average_price) * quantity;
}

Money PnLCalculator::realized(
Quantity quantity,
Price entry_price,
Price exit_price
)
{
return (exit_price - entry_price) * quantity;
}

PnLResult PnLCalculator::calculate(
Quantity quantity,
Price average_price,
Price market_price,
Money realized_pnl
)
{
PnLResult result;


result.realized = realized_pnl;

result.unrealized =
    unrealized(
        quantity,
        average_price,
        market_price
    );

result.total =
    result.realized +
    result.unrealized;

return result;


}

}
