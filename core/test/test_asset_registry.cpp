#include "crytopz/asset_registry.hpp"

#include <cassert>
#include <iostream>

using namespace crytopz;

int main()
{
    std::cout
        << "========================================\n"
        << " Crytopz Asset Registry Test\n"
        << "========================================\n";


    AssetRegistry registry;


    // ========================================================
    // Add crypto
    // ========================================================

    assert(
        registry.add({
            "BTCUSDT",
            "Bitcoin",
            "BINANCE",
            "USDT",
            AssetType::Crypto
        })
    );

    std::cout
        << "[PASS] Add crypto\n";


    // ========================================================
    // Add stocks
    // ========================================================

    assert(
        registry.add({
            "AAPL",
            "Apple Inc.",
            "NASDAQ",
            "USD",
            AssetType::Stock
        })
    );

    assert(
        registry.add({
            "NVDA",
            "NVIDIA Corporation",
            "NASDAQ",
            "USD",
            AssetType::Stock
        })
    );

    std::cout
        << "[PASS] Add stocks\n";


    // ========================================================
    // Find
    // ========================================================

    const Asset* btc =
        registry.find("BTCUSDT");

    assert(btc != nullptr);
    assert(btc->type == AssetType::Crypto);

    const Asset* nvda =
        registry.find("NVDA");

    assert(nvda != nullptr);
    assert(nvda->type == AssetType::Stock);

    std::cout
        << "[PASS] Find\n";


    // ========================================================
    // Duplicate
    // ========================================================

    assert(
        !registry.add({
            "AAPL",
            "Duplicate",
            "NASDAQ",
            "USD",
            AssetType::Stock
        })
    );

    std::cout
        << "[PASS] Duplicate protection\n";


    // ========================================================
    // Filter
    // ========================================================

    auto crypto =
        registry.by_type(
            AssetType::Crypto
        );

    auto stocks =
        registry.by_type(
            AssetType::Stock
        );

    assert(
        crypto.size() == 1
    );

    assert(
        stocks.size() == 2
    );

    std::cout
        << "[PASS] Type filtering\n";


    // ========================================================
    // Remove
    // ========================================================

    assert(
        registry.remove("NVDA")
    );

    assert(
        registry.find("NVDA")
        == nullptr
    );

    std::cout
        << "[PASS] Remove\n";


    // ========================================================
    // Clear
    // ========================================================

    registry.clear();

    assert(
        registry.all().empty()
    );

    std::cout
        << "[PASS] Clear\n";


    std::cout
        << "========================================\n"
        << " ALL ASSET REGISTRY TESTS PASSED\n"
        << "========================================\n";

    return 0;
}