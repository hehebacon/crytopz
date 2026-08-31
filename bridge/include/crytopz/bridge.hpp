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
// CORE LIFETIME
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
// TRADING ACCOUNT
// ============================================================

CRYTOPZ_API int crytopz_set_active_account(
    void* handle,
    const char* account_id
);

CRYTOPZ_API const char* crytopz_active_account_id(
    void* handle
);

CRYTOPZ_API const char* crytopz_active_account_name(
    void* handle
);

CRYTOPZ_API const char* crytopz_active_account_mode(
    void* handle
);

}