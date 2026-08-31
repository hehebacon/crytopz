#pragma once

#include <string>

namespace crytopz::identity {

class Credential {
public:
    Credential() = default;

    static Credential create(
        const std::string& password
    );

    bool verify(
        const std::string& password
    ) const;

    bool valid() const;

    const std::string& salt() const;
    const std::string& verifier() const;

private:
    std::string salt_;
    std::string verifier_;
};

}