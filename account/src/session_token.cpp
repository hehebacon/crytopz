
#include "session_token.hpp"

#include <random>
#include <sstream>
#include <iomanip>

namespace crytopz::identity {

namespace {

std::string generateRandomToken()
{
    std::random_device rd;

    std::mt19937_64 generator(
        rd()
    );

    std::stringstream stream;

    for (int i = 0; i < 4; ++i)
    {
        stream
            << std::hex
            << std::setw(16)
            << std::setfill('0')
            << generator();
    }

    return stream.str();
}

}

SessionToken SessionToken::generate(
    const std::string& account_id
)
{
    SessionToken session;

    if (account_id.empty())
    {
        return session;
    }

    session.token_ =
        generateRandomToken();

    session.account_id_ =
        account_id;

    // Session lifetime: 24 hours.
    session.expires_at_ =
        std::chrono::system_clock::now()
        + std::chrono::hours(24);

    session.valid_ = true;

    return session;
}


bool SessionToken::valid() const
{
    if (!valid_)
    {
        return false;
    }

    if (token_.empty())
    {
        return false;
    }

    if (account_id_.empty())
    {
        return false;
    }

    return
        std::chrono::system_clock::now()
        < expires_at_;
}


const std::string&
SessionToken::value() const
{
    return token_;
}


const std::string&
SessionToken::accountId() const
{
    return account_id_;
}


void SessionToken::invalidate()
{
    valid_ = false;

    token_.clear();
    account_id_.clear();

    expires_at_ =
        std::chrono::system_clock::time_point{};
}

}

