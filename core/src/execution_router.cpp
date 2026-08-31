#include "crytopz/execution_router.hpp"

#include <sstream>
#include <iomanip>

namespace crytopz {

ExecutionRouter::ExecutionRouter(
    TradingAccountManager& account_manager
)
    : account_manager_(account_manager)
{
}

OrderResult ExecutionRouter::place_order(
    const OrderRequest& request
)
{
    OrderResult result;

    if (request.symbol.empty()) {
        result.message = "Symbol is empty";
        return result;
    }

    if (request.quantity <= 0.0) {
        result.message = "Quantity must be greater than zero";
        return result;
    }

    TradingAccount* account =
        account_manager_.get_active_account();

    if (account == nullptr) {
        result.message = "No active trading account";
        return result;
    }

    switch (account->mode) {

        case TradingMode::LOCAL:
            return execute_local(request, *account);

        case TradingMode::SANDBOX:
            return execute_sandbox(request, *account);

        case TradingMode::LIVE:
            return execute_live(request, *account);
    }

    result.message = "Unknown trading mode";
    return result;
}

OrderResult ExecutionRouter::execute_local(
    const OrderRequest& request,
    TradingAccount& account
)
{
    OrderResult result;

    const double cost =
        request.quantity * request.price;

    if (request.side == OrderSide::BUY) {

        if (cost > account.virtual_balance) {
            result.message =
                "Insufficient virtual balance";
            return result;
        }

        account.virtual_balance -= cost;
    }

    std::ostringstream id;

    id << "LOCAL-"
       << std::setw(8)
       << std::setfill('0')
       << next_order_id_++;

    result.success = true;
    result.order_id = id.str();
    result.filled_quantity = request.quantity;
    result.filled_price = request.price;
    result.message = "Local order executed";

    return result;
}

OrderResult ExecutionRouter::execute_sandbox(
    const OrderRequest& request,
    TradingAccount& account
)
{
    (void)request;
    (void)account;

    OrderResult result;

    result.success = false;
    result.message =
        "Sandbox adapter is not connected yet";

    return result;
}

OrderResult ExecutionRouter::execute_live(
    const OrderRequest& request,
    TradingAccount& account
)
{
    (void)request;
    (void)account;

    OrderResult result;

    result.success = false;
    result.message =
        "Live broker adapter is not connected";

    return result;
}

}
