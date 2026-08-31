
#include "crytopz/crypto_market_provider.hpp"

#include <nlohmann/json.hpp>

#include <chrono>
#include <cstdint>
#include <string>

namespace crytopz {

// ============================================================
// CONSTRUCTOR
// ============================================================

CryptoMarketProvider::CryptoMarketProvider(
    HttpClient& http_client
)
    : http_client_(http_client),
      market_(nullptr)
{
}


// ============================================================
// CONSTRUCTOR WITH MARKET
// ============================================================

CryptoMarketProvider::CryptoMarketProvider(
    HttpClient& http_client,
    MarketData& market
)
    : http_client_(http_client),
      market_(&market)
{
}


// ============================================================
// START
// ============================================================

bool CryptoMarketProvider::start()
{
    if (running_)
        return false;

    running_ = true;

    return true;
}


// ============================================================
// STOP
// ============================================================

void CryptoMarketProvider::stop()
{
    running_ = false;
}


// ============================================================
// RUNNING
// ============================================================

bool CryptoMarketProvider::running() const
{
    return running_;
}


// ============================================================
// FETCH
// ============================================================

bool CryptoMarketProvider::fetch(
    const std::string& symbol
)
{
    Ticker ticker;

    if (!fetch(symbol, ticker))
        return false;

    // --------------------------------------------------------
    // Push live market data into Core MarketData
    // --------------------------------------------------------

    if (market_ != nullptr)
    {
        market_->update(
            ticker.symbol,
            ticker.bid,
            ticker.ask,
            ticker.last,
            ticker.timestamp
        );
    }

    return true;
}


// ============================================================
// FETCH WITH TICKER
// ============================================================

bool CryptoMarketProvider::fetch(
    const std::string& symbol,
    Ticker& ticker
)
{
    if (!running_)
        return false;

    if (symbol.empty())
        return false;


    // --------------------------------------------------------
    // Normalize symbol
    // --------------------------------------------------------

    std::string normalized_symbol = symbol;

    for (char& c : normalized_symbol)
    {
        if (c >= 'a' && c <= 'z')
        {
            c = static_cast<char>(
                c - 'a' + 'A'
            );
        }
    }


    // --------------------------------------------------------
    // Binance BOOK TICKER
    //
    // Gives:
    //     bidPrice
    //     askPrice
    //
    // This is required by the execution engine.
    // --------------------------------------------------------

    const std::string url =
        "https://api.binance.com/api/v3/ticker/bookTicker?symbol="
        + normalized_symbol;


    // --------------------------------------------------------
    // HTTP GET
    // --------------------------------------------------------

    HttpResponse response =
        http_client_.get(url);


    if (!response.success)
        return false;

    if (response.status_code != 200)
        return false;


    // --------------------------------------------------------
    // JSON
    // --------------------------------------------------------

    try
    {
        const auto json =
            nlohmann::json::parse(
                response.body
            );


        if (!json.contains("symbol") ||
            !json.contains("bidPrice") ||
            !json.contains("askPrice"))
        {
            return false;
        }


        // ----------------------------------------------------
        // Symbol
        // ----------------------------------------------------

        const std::string api_symbol =
            json.at("symbol").get<std::string>();


        // ----------------------------------------------------
        // Bid / Ask
        // ----------------------------------------------------

        const double bid =
            std::stod(
                json.at("bidPrice").get<std::string>()
            );

        const double ask =
            std::stod(
                json.at("askPrice").get<std::string>()
            );


        if (bid <= 0.0 ||
            ask <= 0.0)
        {
            return false;
        }


        if (ask < bid)
        {
            return false;
        }


        // ----------------------------------------------------
        // Last
        //
        // bookTicker does not provide last trade price.
        //
        // Use a second endpoint for the actual last price.
        // ----------------------------------------------------

        const std::string price_url =
            "https://api.binance.com/api/v3/ticker/price?symbol="
            + normalized_symbol;


        HttpResponse price_response =
            http_client_.get(price_url);


        if (!price_response.success)
            return false;

        if (price_response.status_code != 200)
            return false;


        const auto price_json =
            nlohmann::json::parse(
                price_response.body
            );


        if (!price_json.contains("price"))
            return false;


        const double last =
            std::stod(
                price_json.at("price").get<std::string>()
            );


        if (last <= 0.0)
            return false;


        // ----------------------------------------------------
        // Timestamp
        // ----------------------------------------------------

        const auto now =
            std::chrono::duration_cast<
                std::chrono::milliseconds
            >(
                std::chrono::system_clock::now()
                    .time_since_epoch()
            );


        const std::uint64_t timestamp =
            static_cast<std::uint64_t>(
                now.count()
            );


        // ----------------------------------------------------
        // Build ticker
        // ----------------------------------------------------

        ticker = {};

        ticker.symbol =
            Symbol{
                api_symbol
            };

        ticker.bid =
            bid;

        ticker.ask =
            ask;

        ticker.last =
            last;

        ticker.previous_last =
            0.0;

        ticker.change =
            0.0;

        ticker.change_percent =
            0.0;

        ticker.direction =
            PriceDirection::Unchanged;

        ticker.timestamp =
            timestamp;


        // ----------------------------------------------------
        // Push into MarketData
        //
        // This also makes fetch(symbol, ticker) useful as
        // a standalone provider call while keeping the
        // normal fetch(symbol) path responsible for the
        // MarketData update.
        // ----------------------------------------------------

        return true;
    }
    catch (...)
    {
        return false;
    }
}

} // namespace crytopz

