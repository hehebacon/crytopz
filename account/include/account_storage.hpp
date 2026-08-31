#pragma once

#include "account_manager.hpp"

#include <string>

namespace crytopz::identity {

class AccountStorage {
public:
    static bool save(
        const AccountManager& manager,
        const std::string& path
    );

    static bool load(
        AccountManager& manager,
        const std::string& path
    );
};

}