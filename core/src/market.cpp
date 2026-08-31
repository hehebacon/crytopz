#include "crytopz/market.hpp"

namespace crytopz {

// ============================================================
// UPDATE
// ============================================================

void MarketData::update(
    const Symbol& symbol,
    Price bid,
    Price ask,
    Price last,
    std::uint64_t timestamp
)
{
    auto& ticker =
        tickers_[symbol.value];

    const Price previous =
        ticker.last;

    ticker.symbol =
        symbol;

    ticker.bid =
        bid;

    ticker.ask =
        ask;

    ticker.previous_last =
        previous;

    ticker.last =
        last;

    ticker.timestamp =
        timestamp;

    // --------------------------------------------------------
    // First update
    // --------------------------------------------------------

    if (previous <= 0.0)
    {
        ticker.change =
            0.0;

        ticker.change_percent =
            0.0;

        ticker.direction =
            PriceDirection::Unchanged;

        return;
    }

    // --------------------------------------------------------
    // Price change
    // --------------------------------------------------------

    ticker.change =
        last - previous;

    ticker.change_percent =
        (ticker.change / previous)
        * 100.0;

    // --------------------------------------------------------
    // Direction
    // --------------------------------------------------------

    if (last > previous)
    {
        ticker.direction =
            PriceDirection::Up;
    }
    else if (last < previous)
    {
        ticker.direction =
            PriceDirection::Down;
    }
    else
    {
        ticker.direction =
            PriceDirection::Unchanged;
    }
}


// ============================================================
// GET TICKER
// ============================================================

Ticker MarketData::get_ticker(
    const Symbol& symbol
) const
{
    const auto it =
        tickers_.find(symbol.value);

    if (it == tickers_.end())
        return {};

    return it->second;
}


// ============================================================
// GET PRICE
// ============================================================

double MarketData::get_price(
    const std::string& symbol
) const
{
    const auto it =
        tickers_.find(symbol);

    if (it == tickers_.end())
        return 0.0;

    return it->second.last;
}


// ============================================================
// HAS SYMBOL
// ============================================================

bool MarketData::has_symbol(
    const std::string& symbol
) const
{
    return
        tickers_.find(symbol)
        != tickers_.end();
}


// ============================================================
// SYMBOL LIST
// ============================================================

std::vector<std::string>
MarketData::symbols() const
{
    std::vector<std::string> result;

    result.reserve(
        tickers_.size()
    );

    for (const auto& entry : tickers_)
    {
        result.push_back(
            entry.first
        );
    }

    return result;
}


// ============================================================
// SIZE
// ============================================================

std::size_t MarketData::size() const
{
    return tickers_.size();
}


// ============================================================
// CLEAR
// ============================================================

void MarketData::clear()
{
    tickers_.clear();
}

} // namespace crytopz
