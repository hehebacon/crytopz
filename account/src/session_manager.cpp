
#include "session_manager.hpp"

namespace crytopz::identity {

SessionManager::SessionManager(
    AccountManager& manager
)
    : manager_(manager)
{
}


// ============================================================
// LOGIN
// ============================================================

bool SessionManager::login(
    const std::string& account_id,
    const std::string& password
)
{
    // Remove any existing session.
    logout();

    Account* account =
        manager_.getAccount(account_id);

    if (!account)
    {
        return false;
    }

    if (!account->verifyPassword(password))
    {
        return false;
    }

    SessionToken token =
        SessionToken::generate(account_id);

    if (!token.valid())
    {
        return false;
    }

    session_ =
        std::make_unique<SessionToken>(
            std::move(token)
        );

    return true;
}


// ============================================================
// LOGOUT
// ============================================================

void SessionManager::logout()
{
    if (!session_)
    {
        return;
    }

    session_->invalidate();

    session_.reset();
}


// ============================================================
// SESSION STATE
// ============================================================

bool SessionManager::isLoggedIn() const
{
    return
        session_ &&
        session_->valid();
}


// ============================================================
// CURRENT ACCOUNT
// ============================================================

Account*
SessionManager::currentAccount()
{
    if (!isLoggedIn())
    {
        return nullptr;
    }

    return manager_.getAccount(
        session_->accountId()
    );
}


const Account*
SessionManager::currentAccount() const
{
    if (!isLoggedIn())
    {
        return nullptr;
    }

    return manager_.getAccount(
        session_->accountId()
    );
}


// ============================================================
// CURRENT ACCOUNT ID
// ============================================================

const std::string&
SessionManager::currentAccountId() const
{
    static const std::string empty;

    if (!isLoggedIn())
    {
        return empty;
    }

    return session_->accountId();
}


// ============================================================
// SESSION TOKEN
// ============================================================

const SessionToken*
SessionManager::sessionToken() const
{
    if (!isLoggedIn())
    {
        return nullptr;
    }

    return session_.get();
}


// ============================================================
// SESSION TOKEN VALUE
// ============================================================

const std::string&
SessionManager::sessionTokenValue() const
{
    static const std::string empty;

    if (!isLoggedIn())
    {
        return empty;
    }

    return session_->value();
}


// ============================================================
// TOKEN VALIDATION
// ============================================================

bool SessionManager::validateToken(
    const std::string& token
) const
{
    if (!isLoggedIn())
    {
        return false;
    }

    if (token.empty())
    {
        return false;
    }

    return
        session_->value() == token;
}


// ============================================================
// ACCOUNT FROM TOKEN
// ============================================================

Account*
SessionManager::accountFromToken(
    const std::string& token
)
{
    if (!validateToken(token))
    {
        return nullptr;
    }

    return manager_.getAccount(
        session_->accountId()
    );
}

}

