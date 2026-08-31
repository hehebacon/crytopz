
#pragma once

#include <string>
#include <vector>

#include "credential.hpp"

namespace crytopz::identity {

struct LinkedAccount {
    std::string id;
    std::string provider;
    std::string type;
    bool connected = false;
};

struct AccountSettings {
    std::string language = "vi";
    std::string theme = "dark";
};

class Account {
public:
    Account() = default;

    Account(
        std::string id,
        std::string username
    );

    // ========================================================
    // BASIC IDENTITY
    // ========================================================

    const std::string& id() const;
    const std::string& username() const;

    // ========================================================
    // SETTINGS
    // ========================================================

    AccountSettings& settings();
    const AccountSettings& settings() const;

    // ========================================================
    // LINKED ACCOUNTS
    // ========================================================

    void addLinkedAccount(
        const LinkedAccount& account
    );

    const std::vector<LinkedAccount>&
    linkedAccounts() const;

    // ========================================================
    // CREDENTIAL
    // ========================================================

    void setCredential(
        const Credential& credential
    );

    bool hasCredential() const;

    bool verifyPassword(
        const std::string& password
    ) const;

    const Credential& credential() const;

private:
    std::string id_;
    std::string username_;

    AccountSettings settings_;

    Credential credential_;

    std::vector<LinkedAccount>
        linkedAccounts_;
};

}
