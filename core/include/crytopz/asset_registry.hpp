#pragma once

#include "asset.hpp"

#include <string>
#include <vector>

namespace crytopz {

class AssetRegistry
{
public:

    AssetRegistry();

    // ========================================================
    // ASSETS
    // ========================================================

    const std::vector<Asset>&
    all() const;

    const Asset*
    find(
        const std::string& symbol
    ) const;

    // ========================================================
    // FILTER
    // ========================================================

    std::vector<Asset>
    by_type(
        AssetType type
    ) const;

    // ========================================================
    // MANAGEMENT
    // ========================================================

    bool add(
        const Asset& asset
    );

    bool remove(
        const std::string& symbol
    );

    void clear();

private:

    std::vector<Asset> assets_;
};

}