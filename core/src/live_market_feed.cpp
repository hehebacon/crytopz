#include "crytopz/live_market_feed.hpp"
#include "crytopz/crypto_market_provider.hpp"
#include "crytopz/winhttp_client.hpp"

#include <algorithm>
#include <cctype>

namespace crytopz {

// ============================================================
// CONSTRUCTOR
// ============================================================

LiveMarketFeed::LiveMarketFeed(
    MarketProvider& provider,
    MarketData& market_data
)
    : provider_(provider),
      market_data_(market_data)
{
}

// ============================================================
// START
// ============================================================

bool LiveMarketFeed::start()
{
    if (running_)
        return false;

    // Provider phải chạy trước khi feed update.
    if (!provider_.running())
    {
        if (!provider_.start())
            return false;
    }

    running_ = true;

    return true;
}

// ============================================================
// STOP
// ============================================================

void LiveMarketFeed::stop()
{
    if (!running_)
    {
        // Đảm bảo provider cũng không còn chạy.
        if (provider_.running())
            provider_.stop();

        return;
    }

    running_ = false;

    // Feed owns the provider lifecycle while running.
    if (provider_.running())
        provider_.stop();
}

// ============================================================
// RUNNING
// ============================================================

bool LiveMarketFeed::running() const
{
    return running_;
}

// ============================================================
// UPDATE
// ============================================================

std::size_t LiveMarketFeed::update()
{
    if (!running_)
        return 0;

    std::size_t updated = 0;

    for (const auto& symbol : symbols_)
    {
        Ticker ticker;

        if (!provider_.fetch(
                symbol,
                ticker))
        {
            continue;
        }

        market_data_.update(
            ticker.symbol,
            ticker.bid,
            ticker.ask,
            ticker.last,
            ticker.timestamp
        );

        ++updated;
    }

    return updated;
}

// ============================================================
// ADD SYMBOL
// ============================================================

bool LiveMarketFeed::add_symbol(
    const std::string& symbol
)
{
    if (symbol.empty())
        return false;

    std::string normalized = symbol;

    for (char& c : normalized)
    {
        c = static_cast<char>(
            std::toupper(
                static_cast<unsigned char>(c)
            )
        );
    }

    if (normalized.empty())
        return false;

    const auto it =
        std::find(
            symbols_.begin(),
            symbols_.end(),
            normalized
        );

    if (it != symbols_.end())
        return false;

    symbols_.push_back(normalized);

    return true;
}

// ============================================================
// REMOVE SYMBOL
// ============================================================

bool LiveMarketFeed::remove_symbol(
    const std::string& symbol
)
{
    if (symbol.empty())
        return false;

    std::string normalized = symbol;

    for (char& c : normalized)
    {
        c = static_cast<char>(
            std::toupper(
                static_cast<unsigned char>(c)
            )
        );
    }

    const auto it =
        std::find(
            symbols_.begin(),
            symbols_.end(),
            normalized
        );

    if (it == symbols_.end())
        return false;

    symbols_.erase(it);

    return true;
}

// ============================================================
// SYMBOLS
// ============================================================

const std::vector<std::string>&
LiveMarketFeed::symbols() const
{
    return symbols_;
}

} // namespace crytopz