
#pragma once

#include <cstdint>

#ifdef _WIN32
#define CRYTOPZ_API __declspec(dllexport)
#else
#define CRYTOPZ_API
#endif

extern "C"
{

// ============================================================
// CORE LIFECYCLE
// ============================================================

CRYTOPZ_API void* crytopz_create(
    double initial_balance
);

CRYTOPZ_API void crytopz_destroy(
    void* handle
);


// ============================================================
// MARKET
// ============================================================

CRYTOPZ_API void crytopz_update_market(
    void* handle,
    const char* symbol,
    double bid,
    double ask,
    double last,
    std::uint64_t timestamp
);

CRYTOPZ_API double crytopz_get_price(
    void* handle,
    const char* symbol
);


// ============================================================
// LIVE MARKET
// ============================================================

CRYTOPZ_API int crytopz_start_live_market(
    void* handle
);

CRYTOPZ_API void crytopz_stop_live_market(
    void* handle
);

CRYTOPZ_API int crytopz_live_market_running(
    void* handle
);

CRYTOPZ_API std::uint64_t crytopz_live_market_interval_ms(
    void* handle
);


// ============================================================
// TRADING
// ============================================================

CRYTOPZ_API std::uint64_t crytopz_buy(
    void* handle,
    const char* symbol,
    double quantity
);

CRYTOPZ_API std::uint64_t crytopz_sell(
    void* handle,
    const char* symbol,
    double quantity
);


// ============================================================
// ACCOUNT
// ============================================================

CRYTOPZ_API double crytopz_balance(
    void* handle
);

CRYTOPZ_API double crytopz_position_quantity(
    void* handle,
    const char* symbol
);

CRYTOPZ_API double crytopz_position_average_price(
    void* handle,
    const char* symbol
);

CRYTOPZ_API double crytopz_realized_pnl(
    void* handle
);


// ============================================================
// PORTFOLIO / FINANCIAL STATE
// ============================================================

CRYTOPZ_API double crytopz_unrealized_pnl(
    void* handle
);

CRYTOPZ_API double crytopz_position_value(
    void* handle
);

CRYTOPZ_API double crytopz_equity(
    void* handle
);

CRYTOPZ_API double crytopz_total_pnl(
    void* handle
);


// ============================================================
// ORDER HISTORY
// ============================================================

CRYTOPZ_API std::uint64_t crytopz_order_count(
    void* handle
);

CRYTOPZ_API std::uint64_t crytopz_order_id(
    void* handle,
    std::uint64_t index
);

CRYTOPZ_API const char* crytopz_order_symbol(
    void* handle,
    std::uint64_t index
);

CRYTOPZ_API int crytopz_order_side(
    void* handle,
    std::uint64_t index
);

CRYTOPZ_API int crytopz_order_type(
    void* handle,
    std::uint64_t index
);

CRYTOPZ_API double crytopz_order_price(
    void* handle,
    std::uint64_t index
);

CRYTOPZ_API double crytopz_order_quantity(
    void* handle,
    std::uint64_t index
);

CRYTOPZ_API int crytopz_order_status(
    void* handle,
    std::uint64_t index
);

CRYTOPZ_API std::uint64_t crytopz_order_timestamp(
    void* handle,
    std::uint64_t index
);

}

