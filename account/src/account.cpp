
#include "account.hpp"

#include <utility>

namespace crytopz::identity {

Account::Account(
    std::string id,
    std::string username
)
    : id_(std::move(id)),
      username_(std::move(username))
{
}


// ============================================================
// BASIC IDENTITY
// ============================================================

const std::string&
Account::id() const
{
    return id_;
}

const std::string&
Account::username() const
{
    return username_;
}


// ============================================================
// SETTINGS
// ============================================================

AccountSettings&
Account::settings()
{
    return settings_;
}

const AccountSettings&
Account::settings() const
{
    return settings_;
}


// ============================================================
// LINKED ACCOUNTS
// ============================================================

void Account::addLinkedAccount(
    const LinkedAccount& account
)
{
    linkedAccounts_.push_back(account);
}

const std::vector<LinkedAccount>&
Account::linkedAccounts() const
{
    return linkedAccounts_;
}


// ============================================================
// CREDENTIAL
// ============================================================

void Account::setCredential(
    const Credential& credential
)
{
    credential_ = credential;
}

bool Account::hasCredential() const
{
    return credential_.valid();
}

bool Account::verifyPassword(
    const std::string& password
) const
{
    if (!hasCredential())
    {
        return false;
    }

    return credential_.verify(password);
}

const Credential&
Account::credential() const
{
    return credential_;
}

}

