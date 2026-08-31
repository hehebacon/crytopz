#include "crytopz/bridge.hpp"
#include "crytopz/core_api.hpp"

#include <cstdint>
#include <cstddef>
#include <string>

#ifdef _WIN32
#define CRYTOPZ_EXPORT __declspec(dllexport)
#else
#define CRYTOPZ_EXPORT
#endif

namespace
{

crytopz::CoreAPI* get_core(void* handle)
{
    return static_cast<crytopz::CoreAPI*>(handle);
}

const crytopz::Order* get_order(
    void* handle,
    std::uint64_t index
)
{
    if (!handle)
        return nullptr;

    return get_core(handle)->get_order(
        static_cast<std::size_t>(index)
    );
}

}

extern "C"
{

// ============================================================
// CORE
// ============================================================

CRYTOPZ_EXPORT
void* crytopz_create(double initial_balance)
{
    if (initial_balance < 0.0)
        return nullptr;

    try
    {
        return new crytopz::CoreAPI(initial_balance);
    }
    catch (...)
    {
        return nullptr;
    }
}


CRYTOPZ_EXPORT
void crytopz_destroy(void* handle)
{
    if (!handle)
        return;

    delete get_core(handle);
}


// ============================================================
// MARKET
// ============================================================

CRYTOPZ_EXPORT
void crytopz_update_market(
    void* handle,
    const char* symbol,
    double bid,
    double ask,
    double last,
    std::uint64_t timestamp
)
{
    if (!handle || !symbol)
        return;

    get_core(handle)->update_market(
        std::string(symbol),
        bid,
        ask,
        last,
        timestamp
    );
}


CRYTOPZ_EXPORT
double crytopz_get_price(
    void* handle,
    const char* symbol
)
{
    if (!handle || !symbol)
        return 0.0;

    return get_core(handle)->get_price(
        std::string(symbol)
    );
}


// ============================================================
// TRADING
// ============================================================

CRYTOPZ_EXPORT
std::uint64_t crytopz_buy(
    void* handle,
    const char* symbol,
    double quantity
)
{
    if (!handle || !symbol)
        return 0;

    return get_core(handle)->buy(
        std::string(symbol),
        quantity
    );
}


CRYTOPZ_EXPORT
std::uint64_t crytopz_sell(
    void* handle,
    const char* symbol,
    double quantity
)
{
    if (!handle || !symbol)
        return 0;

    return get_core(handle)->sell(
        std::string(symbol),
        quantity
    );
}


// ============================================================
// ACCOUNT
// ============================================================

CRYTOPZ_EXPORT
double crytopz_balance(void* handle)
{
    if (!handle)
        return 0.0;

    return get_core(handle)->balance();
}


CRYTOPZ_EXPORT
double crytopz_position_quantity(
    void* handle,
    const char* symbol
)
{
    if (!handle || !symbol)
        return 0.0;

    return get_core(handle)
        ->position(std::string(symbol))
        .quantity;
}


CRYTOPZ_EXPORT
double crytopz_position_average_price(
    void* handle,
    const char* symbol
)
{
    if (!handle || !symbol)
        return 0.0;

    return get_core(handle)
        ->position(std::string(symbol))
        .average_price;
}


CRYTOPZ_EXPORT
double crytopz_realized_pnl(void* handle)
{
    if (!handle)
        return 0.0;

    return get_core(handle)->realized_pnl();
}


// ============================================================
// PORTFOLIO
// ============================================================

CRYTOPZ_EXPORT
double crytopz_unrealized_pnl(void* handle)
{
    if (!handle)
        return 0.0;

    return get_core(handle)->unrealized_pnl();
}


CRYTOPZ_EXPORT
double crytopz_position_value(void* handle)
{
    if (!handle)
        return 0.0;

    return get_core(handle)->position_value();
}


CRYTOPZ_EXPORT
double crytopz_equity(void* handle)
{
    if (!handle)
        return 0.0;

    return get_core(handle)->equity();
}


CRYTOPZ_EXPORT
double crytopz_total_pnl(void* handle)
{
    if (!handle)
        return 0.0;

    return get_core(handle)->total_pnl();
}


// ============================================================
// ORDER HISTORY
// ============================================================

CRYTOPZ_EXPORT
std::uint64_t crytopz_order_count(void* handle)
{
    if (!handle)
        return 0;

    return static_cast<std::uint64_t>(
        get_core(handle)->order_count()
    );
}


CRYTOPZ_EXPORT
std::uint64_t crytopz_order_id(
    void* handle,
    std::uint64_t index
)
{
    const auto* order =
        get_order(handle, index);

    if (!order)
        return 0;

    return order->id;
}


CRYTOPZ_EXPORT
const char* crytopz_order_symbol(
    void* handle,
    std::uint64_t index
)
{
    static thread_local std::string value;

    value.clear();

    const auto* order =
        get_order(handle, index);

    if (!order)
        return "";

    value = order->symbol.value;

    return value.c_str();
}


CRYTOPZ_EXPORT
int crytopz_order_side(
    void* handle,
    std::uint64_t index
)
{
    const auto* order =
        get_order(handle, index);

    if (!order)
        return -1;

    return order->side == crytopz::Side::Buy
        ? 0
        : 1;
}


CRYTOPZ_EXPORT
int crytopz_order_type(
    void* handle,
    std::uint64_t index
)
{
    const auto* order =
        get_order(handle, index);

    if (!order)
        return -1;

    return static_cast<int>(
        order->type
    );
}


CRYTOPZ_EXPORT
double crytopz_order_price(
    void* handle,
    std::uint64_t index
)
{
    const auto* order =
        get_order(handle, index);

    if (!order)
        return 0.0;

    return order->price;
}


CRYTOPZ_EXPORT
double crytopz_order_quantity(
    void* handle,
    std::uint64_t index
)
{
    const auto* order =
        get_order(handle, index);

    if (!order)
        return 0.0;

    return order->quantity;
}


CRYTOPZ_EXPORT
int crytopz_order_status(
    void* handle,
    std::uint64_t index
)
{
    const auto* order =
        get_order(handle, index);

    if (!order)
        return -1;

    return static_cast<int>(
        order->status
    );
}


CRYTOPZ_EXPORT
std::uint64_t crytopz_order_timestamp(
    void* handle,
    std::uint64_t index
)
{
    const auto* order =
        get_order(handle, index);

    if (!order)
        return 0;

    return order->timestamp;
}

}