#pragma once

#include "trading_account.hpp"

#include <cstdint>
#include <string>

namespace crytopz {

enum class OrderSide
{
    BUY,
    SELL
};

struct OrderRequest
{
    std::string symbol;
    OrderSide side = OrderSide::BUY;
    double quantity = 0.0;
    double price = 0.0;
};

struct OrderResult
{
    bool success = false;

    std::string order_id;

    double filled_quantity = 0.0;
    double filled_price = 0.0;

    std::string message;
};

class ExecutionRouter
{
public:

    explicit ExecutionRouter(
        TradingAccountManager& account_manager
    );

    OrderResult place_order(
        const OrderRequest& request
    );

private:

    OrderResult execute_local(
        const OrderRequest& request,
        TradingAccount& account
    );

    OrderResult execute_sandbox(
        const OrderRequest& request,
        TradingAccount& account
    );

    OrderResult execute_live(
        const OrderRequest& request,
        TradingAccount& account
    );

private:

    TradingAccountManager& account_manager_;

    std::uint64_t next_order_id_ = 1;
};

}