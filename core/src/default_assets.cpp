#include "crytopz/default_assets.hpp"

namespace crytopz {

std::vector<Asset> create_default_assets()
{
    return {

        // =========================
        // CRYPTO
        // =========================

        {
            "BTCUSDT",
            "Bitcoin",
            "BINANCE",
            "USDT",
            AssetType::Crypto
        },

        {
            "ETHUSDT",
            "Ethereum",
            "BINANCE",
            "USDT",
            AssetType::Crypto
        },

        {
            "SOLUSDT",
            "Solana",
            "BINANCE",
            "USDT",
            AssetType::Crypto
        },

        {
            "BNBUSDT",
            "BNB",
            "BINANCE",
            "USDT",
            AssetType::Crypto
        },

        {
            "XRPUSDT",
            "XRP",
            "BINANCE",
            "USDT",
            AssetType::Crypto
        },


        // =========================
        // US STOCKS
        // =========================

        {
            "AAPL",
            "Apple Inc.",
            "NASDAQ",
            "USD",
            AssetType::Stock
        },

        {
            "MSFT",
            "Microsoft Corporation",
            "NASDAQ",
            "USD",
            AssetType::Stock
        },

        {
            "NVDA",
            "NVIDIA Corporation",
            "NASDAQ",
            "USD",
            AssetType::Stock
        },

        {
            "AMZN",
            "Amazon.com Inc.",
            "NASDAQ",
            "USD",
            AssetType::Stock
        },

        {
            "GOOGL",
            "Alphabet Inc.",
            "NASDAQ",
            "USD",
            AssetType::Stock
        },

        {
            "META",
            "Meta Platforms Inc.",
            "NASDAQ",
            "USD",
            AssetType::Stock
        },

        {
            "TSLA",
            "Tesla Inc.",
            "NASDAQ",
            "USD",
            AssetType::Stock
        },

        {
            "AVGO",
            "Broadcom Inc.",
            "NASDAQ",
            "USD",
            AssetType::Stock
        },

        {
            "AMD",
            "Advanced Micro Devices Inc.",
            "NASDAQ",
            "USD",
            AssetType::Stock
        }
    };
}

}