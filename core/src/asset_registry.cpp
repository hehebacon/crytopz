#include "crytopz/asset_registry.hpp"

#include <algorithm>

namespace crytopz {

AssetRegistry::AssetRegistry()
{
}


// ============================================================
// ALL
// ============================================================

const std::vector<Asset>&
AssetRegistry::all() const
{
    return assets_;
}


// ============================================================
// FIND
// ============================================================

const Asset*
AssetRegistry::find(
    const std::string& symbol
) const
{
    for (const auto& asset : assets_)
    {
        if (asset.symbol == symbol)
            return &asset;
    }

    return nullptr;
}


// ============================================================
// BY TYPE
// ============================================================

std::vector<Asset>
AssetRegistry::by_type(
    AssetType type
) const
{
    std::vector<Asset> result;

    for (const auto& asset : assets_)
    {
        if (asset.type == type)
            result.push_back(asset);
    }

    return result;
}


// ============================================================
// ADD
// ============================================================

bool AssetRegistry::add(
    const Asset& asset
)
{
    if (asset.symbol.empty())
        return false;

    if (find(asset.symbol))
        return false;

    assets_.push_back(asset);

    return true;
}


// ============================================================
// REMOVE
// ============================================================

bool AssetRegistry::remove(
    const std::string& symbol
)
{
    auto it =
        std::find_if(
            assets_.begin(),
            assets_.end(),
            [&](const Asset& asset)
            {
                return asset.symbol == symbol;
            }
        );

    if (it == assets_.end())
        return false;

    assets_.erase(it);

    return true;
}


// ============================================================
// CLEAR
// ============================================================

void AssetRegistry::clear()
{
    assets_.clear();
}

}