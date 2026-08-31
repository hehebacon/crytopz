#include "crytopz/bridge.hpp"
#include "crytopz/core_api.hpp"

#include <cstddef>
#include <cstdint>
#include <string>

#ifdef _WIN32
#define CRYTOPZ_EXPORT __declspec(dllexport)
#else
#define CRYTOPZ_EXPORT
#endif

namespace
{

// ============================================================
// CORE HANDLE
// ============================================================

crytopz::CoreAPI* get_core(void* handle)
{
    if (!handle)
        return nullptr;

    return static_cast<crytopz::CoreAPI*>(handle);
}


// ============================================================
// ORDER HELPER
// ============================================================

const crytopz::Order* get_order(
    void* handle,
    std::uint64_t index
)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return nullptr;

    return core->get_order(
        static_cast<std::size_t>(index)
    );
}

} // namespace


// ============================================================
// C API
// ============================================================

extern "C"
{

// ============================================================
// CORE LIFECYCLE
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
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return;

    delete core;
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
    crytopz::CoreAPI* core = get_core(handle);

    if (!core || !symbol)
        return;

    core->update_market(
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
    crytopz::CoreAPI* core = get_core(handle);

    if (!core || !symbol)
        return 0.0;

    return core->get_price(
        std::string(symbol)
    );
}


// ============================================================
// LIVE MARKET
// ============================================================

CRYTOPZ_EXPORT
int crytopz_start_live_market(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0;

    return core->start_live_market()
        ? 1
        : 0;
}


CRYTOPZ_EXPORT
void crytopz_stop_live_market(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return;

    core->stop_live_market();
}


CRYTOPZ_EXPORT
int crytopz_live_market_running(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0;

    return core->live_market_running()
        ? 1
        : 0;
}


CRYTOPZ_EXPORT
std::uint64_t crytopz_live_market_interval_ms(
    void* handle
)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0;

    return static_cast<std::uint64_t>(
        core->live_market_interval_ms()
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
    crytopz::CoreAPI* core = get_core(handle);

    if (!core || !symbol)
        return 0;

    return core->buy(
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
    crytopz::CoreAPI* core = get_core(handle);

    if (!core || !symbol)
        return 0;

    return core->sell(
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
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0.0;

    return core->balance();
}


CRYTOPZ_EXPORT
double crytopz_position_quantity(
    void* handle,
    const char* symbol
)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core || !symbol)
        return 0.0;

    return core->position(
        std::string(symbol)
    ).quantity;
}


CRYTOPZ_EXPORT
double crytopz_position_average_price(
    void* handle,
    const char* symbol
)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core || !symbol)
        return 0.0;

    return core->position(
        std::string(symbol)
    ).average_price;
}


CRYTOPZ_EXPORT
double crytopz_realized_pnl(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0.0;

    return core->realized_pnl();
}


// ============================================================
// PORTFOLIO / FINANCIAL STATE
// ============================================================

CRYTOPZ_EXPORT
double crytopz_unrealized_pnl(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0.0;

    return core->unrealized_pnl();
}


CRYTOPZ_EXPORT
double crytopz_position_value(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0.0;

    return core->position_value();
}


CRYTOPZ_EXPORT
double crytopz_equity(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0.0;

    return core->equity();
}


CRYTOPZ_EXPORT
double crytopz_total_pnl(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0.0;

    return core->total_pnl();
}


// ============================================================
// ORDER HISTORY
// ============================================================

CRYTOPZ_EXPORT
std::uint64_t crytopz_order_count(void* handle)
{
    crytopz::CoreAPI* core = get_core(handle);

    if (!core)
        return 0;

    return static_cast<std::uint64_t>(
        core->order_count()
    );
}


CRYTOPZ_EXPORT
std::uint64_t crytopz_order_id(
    void* handle,
    std::uint64_t index
)
{
    const crytopz::Order* order =
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

    const crytopz::Order* order =
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
    const crytopz::Order* order =
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
    const crytopz::Order* order =
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
    const crytopz::Order* order =
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
    const crytopz::Order* order =
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
    const crytopz::Order* order =
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
    const crytopz::Order* order =
        get_order(handle, index);

    if (!order)
        return 0;

    return order->timestamp;
}

} // extern "C"