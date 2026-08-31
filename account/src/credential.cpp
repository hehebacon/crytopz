#include "credential.hpp"

#include <array>
#include <cstdint>
#include <iomanip>
#include <random>
#include <sstream>

namespace crytopz::identity {

namespace {

std::string random_salt()
{
    std::random_device rd;

    std::array<std::uint8_t, 16> bytes{};

    for (auto& byte : bytes) {
        byte = static_cast<std::uint8_t>(rd());
    }

    std::ostringstream out;

    for (const auto byte : bytes) {
        out
            << std::hex
            << std::setw(2)
            << std::setfill('0')
            << static_cast<int>(byte);
    }

    return out.str();
}


// NOTE:
// Đây chỉ là placeholder verifier cho Core MVP.
// Không dùng để bảo vệ production credentials.
// Production sẽ chuyển sang Argon2id/bcrypt/PBKDF2
// ở Auth/Web layer.

std::string make_verifier(
    const std::string& password,
    const std::string& salt
)
{
    std::hash<std::string> hasher;

    const auto value =
        hasher(
            salt +
            ":" +
            password
        );

    std::ostringstream out;

    out
        << std::hex
        << value;

    return out.str();
}

}


Credential Credential::create(
    const std::string& password
)
{
    Credential credential;

    if (password.empty()) {
        return credential;
    }

    credential.salt_ =
        random_salt();

    credential.verifier_ =
        make_verifier(
            password,
            credential.salt_
        );

    return credential;
}


bool Credential::verify(
    const std::string& password
) const
{
    if (!valid() || password.empty()) {
        return false;
    }

    return make_verifier(
        password,
        salt_
    ) == verifier_;
}


bool Credential::valid() const
{
    return
        !salt_.empty() &&
        !verifier_.empty();
}


const std::string&
Credential::salt() const
{
    return salt_;
}


const std::string&
Credential::verifier() const
{
    return verifier_;
}

}