#pragma once

#include <string>

namespace crytopz {

enum class AssetType
{
    Crypto,
    Stock
};

struct Asset
{
    std::string symbol;
    std::string name;
    std::string exchange;
    std::string currency;

    AssetType type =
        AssetType::Stock;
};

}