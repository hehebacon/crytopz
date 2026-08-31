
#pragma once

#include <string>
#include <memory>

#include "account_manager.hpp"
#include "session_token.hpp"

namespace crytopz::identity {

class SessionManager {
public:
    explicit SessionManager(
        AccountManager& manager
    );

    bool login(
        const std::string& account_id,
        const std::string& password
    );

    void logout();

    bool isLoggedIn() const;

    Account* currentAccount();

    const Account* currentAccount() const;

    const std::string& currentAccountId() const;

    const SessionToken* sessionToken() const;

    const std::string& sessionTokenValue() const;

    bool validateToken(
        const std::string& token
    ) const;

    Account* accountFromToken(
        const std::string& token
    );

private:
    AccountManager& manager_;

    std::unique_ptr<SessionToken> session_;
};

}
