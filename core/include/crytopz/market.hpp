#pragma once

#include "types.hpp"

#include <cstdint>
#include <string>
#include <unordered_map>
#include <vector>

namespace crytopz {

enum class PriceDirection
{
    Unchanged,
    Up,
    Down
};

struct Ticker
{
    Symbol symbol;

    Price bid = 0.0;
    Price ask = 0.0;
    Price last = 0.0;

    Price previous_last = 0.0;

    Price change = 0.0;
    double change_percent = 0.0;

    PriceDirection direction =
        PriceDirection::Unchanged;

    std::uint64_t timestamp = 0;
};

class MarketData
{
public:

    // ========================================================
    // UPDATE
    // ========================================================

    void update(
        const Symbol& symbol,
        Price bid,
        Price ask,
        Price last,
        std::uint64_t timestamp
    );

    // ========================================================
    // READ
    // ========================================================

    Ticker get_ticker(
        const Symbol& symbol
    ) const;

    double get_price(
        const std::string& symbol
    ) const;

    bool has_symbol(
        const std::string& symbol
    ) const;

    // ========================================================
    // SYMBOLS
    // ========================================================

    std::vector<std::string> symbols() const;

    std::size_t size() const;

    // ========================================================
    // CLEAR
    // ========================================================

    void clear();

private:

    std::unordered_map<
        std::string,
        Ticker
    > tickers_;
};

} // namespace crytopz