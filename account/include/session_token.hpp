
#pragma once

#include <string>
#include <chrono>

namespace crytopz::identity {

class SessionToken {
public:
    SessionToken() = default;

    static SessionToken generate(
        const std::string& account_id
    );

    bool valid() const;

    const std::string& value() const;
    const std::string& accountId() const;

    void invalidate();

private:
    std::string token_;
    std::string account_id_;

    std::chrono::system_clock::time_point expires_at_{};

    bool valid_ = false;
};

}
