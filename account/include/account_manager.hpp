
#pragma once

#include "account.hpp"

#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

namespace crytopz::identity {

class AccountManager {
public:
    AccountManager() = default;
    ~AccountManager() = default;

    AccountManager(const AccountManager&) = delete;

    AccountManager& operator=(
        const AccountManager&
    ) = delete;

    // ========================================================
    // CREATE ACCOUNT
    // ========================================================

    // Create account without credential.
    bool createAccount(
        const std::string& id,
        const std::string& username
    );

    // Create account with password.
    bool createAccount(
        const std::string& id,
        const std::string& username,
        const std::string& password
    );

    // ========================================================
    // DELETE ACCOUNT
    // ========================================================

    bool deleteAccount(
        const std::string& id
    );

    // ========================================================
    // ACCOUNT LOOKUP
    // ========================================================

    Account* getAccount(
        const std::string& id
    );

    const Account* getAccount(
        const std::string& id
    ) const;

    bool accountExists(
        const std::string& id
    ) const;

    // ========================================================
    // ACCOUNT COLLECTION
    // ========================================================

    std::size_t accountCount() const;

    std::vector<const Account*>
    getAccounts() const;

    // ========================================================
    // MANAGEMENT
    // ========================================================

    void clear();

private:
    std::unordered_map<
        std::string,
        std::unique_ptr<Account>
    > accounts_;
};

}
