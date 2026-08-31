#include <crytopz/trading_account.hpp>

#include <algorithm>

namespace crytopz {

TradingAccountManager::TradingAccountManager() {
    // Default account:
    // None - No Connection
    TradingAccount local;

    local.id = "local";
    local.name = "None - No Connection";
    local.mode = TradingMode::LOCAL;
    local.broker = "";
    local.connected = false;
    local.virtual_balance = 10000.0;

    accounts_.push_back(local);
    active_account_id_ = local.id;
}

bool TradingAccountManager::add_account(
    const TradingAccount& account
) {
    if (account.id.empty()) {
        return false;
    }

    if (get_account(account.id) != nullptr) {
        return false;
    }

    accounts_.push_back(account);
    return true;
}

bool TradingAccountManager::remove_account(
    const std::string& id
) {
    // Never remove the default local account.
    if (id == "local") {
        return false;
    }

    auto it = std::remove_if(
        accounts_.begin(),
        accounts_.end(),
        [&](const TradingAccount& account) {
            return account.id == id;
        }
    );

    if (it == accounts_.end()) {
        return false;
    }

    accounts_.erase(it, accounts_.end());

    if (active_account_id_ == id) {
        active_account_id_ = "local";
    }

    return true;
}

bool TradingAccountManager::set_active_account(
    const std::string& id
) {
    TradingAccount* account = get_account(id);

    if (account == nullptr) {
        return false;
    }

    active_account_id_ = id;
    return true;
}

TradingAccount* TradingAccountManager::get_active_account() {
    return get_account(active_account_id_);
}

const TradingAccount*
TradingAccountManager::get_active_account() const {
    for (const auto& account : accounts_) {
        if (account.id == active_account_id_) {
            return &account;
        }
    }

    return nullptr;
}

TradingAccount*
TradingAccountManager::get_account(
    const std::string& id
) {
    for (auto& account : accounts_) {
        if (account.id == id) {
            return &account;
        }
    }

    return nullptr;
}

const std::vector<TradingAccount>&
TradingAccountManager::get_accounts() const {
    return accounts_;
}

const char*
TradingAccountManager::mode_to_string(
    TradingMode mode
) {
    switch (mode) {
        case TradingMode::LOCAL:
            return "LOCAL";

        case TradingMode::SANDBOX:
            return "SANDBOX";

        case TradingMode::LIVE:
            return "LIVE";
    }

    return "UNKNOWN";
}

} 
