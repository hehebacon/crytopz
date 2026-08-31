#pragma once

#include <string>
#include <vector>

namespace crytopz {

enum class TradingMode {
    LOCAL,
    SANDBOX,
    LIVE
};

struct TradingAccount {
    std::string id;
    std::string name;

    TradingMode mode = TradingMode::LOCAL;

    // Empty when using LOCAL.
    std::string broker;

    bool connected = false;

    // Used by LOCAL / SANDBOX.
    double virtual_balance = 10000.0;
};

class TradingAccountManager {
public:
    TradingAccountManager();

    bool add_account(const TradingAccount& account);
    bool remove_account(const std::string& id);

    bool set_active_account(const std::string& id);

    TradingAccount* get_active_account();
    const TradingAccount* get_active_account() const;

    TradingAccount* get_account(const std::string& id);

    const std::vector<TradingAccount>& get_accounts() const;

    static const char* mode_to_string(TradingMode mode);

private:
    std::vector<TradingAccount> accounts_;
    std::string active_account_id_;
};

} // namespace crytopz