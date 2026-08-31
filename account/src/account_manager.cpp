
#include "account_manager.hpp"

#include <utility>

namespace crytopz::identity {


// ============================================================
// CREATE ACCOUNT
// ============================================================

bool AccountManager::createAccount(
    const std::string& id,
    const std::string& username
)
{
    if (id.empty() || username.empty())
    {
        return false;
    }

    if (accountExists(id))
    {
        return false;
    }

    accounts_.emplace(
        id,
        std::make_unique<Account>(
            id,
            username
        )
    );

    return true;
}


bool AccountManager::createAccount(
    const std::string& id,
    const std::string& username,
    const std::string& password
)
{
    if (id.empty() ||
        username.empty() ||
        password.empty())
    {
        return false;
    }

    if (accountExists(id))
    {
        return false;
    }

    auto account =
        std::make_unique<Account>(
            id,
            username
        );

    account->setCredential(
        Credential::create(password)
    );

    accounts_.emplace(
        id,
        std::move(account)
    );

    return true;
}


// ============================================================
// DELETE ACCOUNT
// ============================================================

bool AccountManager::deleteAccount(
    const std::string& id
)
{
    if (id.empty())
    {
        return false;
    }

    return accounts_.erase(id) > 0;
}


// ============================================================
// ACCOUNT LOOKUP
// ============================================================

Account*
AccountManager::getAccount(
    const std::string& id
)
{
    auto it =
        accounts_.find(id);

    if (it == accounts_.end())
    {
        return nullptr;
    }

    return it->second.get();
}


const Account*
AccountManager::getAccount(
    const std::string& id
) const
{
    auto it =
        accounts_.find(id);

    if (it == accounts_.end())
    {
        return nullptr;
    }

    return it->second.get();
}


bool AccountManager::accountExists(
    const std::string& id
) const
{
    if (id.empty())
    {
        return false;
    }

    return accounts_.find(id)
        != accounts_.end();
}


// ============================================================
// ACCOUNT COLLECTION
// ============================================================

std::size_t
AccountManager::accountCount() const
{
    return accounts_.size();
}


std::vector<const Account*>
AccountManager::getAccounts() const
{
    std::vector<const Account*> result;

    result.reserve(
        accounts_.size()
    );

    for (const auto& entry : accounts_)
    {
        result.push_back(
            entry.second.get()
        );
    }

    return result;
}


// ============================================================
// CLEAR
// ============================================================

void AccountManager::clear()
{
    accounts_.clear();
}

}

