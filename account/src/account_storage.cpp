#include "account_storage.hpp"

#include <fstream>
#include <string>

namespace crytopz::identity {

bool AccountStorage::save(
    const AccountManager& manager,
    const std::string& path
) {
    std::ofstream file(
        path,
        std::ios::out | std::ios::trunc
    );

    if (!file.is_open()) {
        return false;
    }

    file << "CRYPTOPZ_ACCOUNTS_V1\n";
    file << "COUNT "
         << manager.accountCount()
         << "\n";

    for (const Account* account :
         manager.getAccounts())
    {
        if (!account) {
            continue;
        }

        file << "ACCOUNT\n";
        file << "ID "
             << account->id()
             << "\n";

        file << "USERNAME "
             << account->username()
             << "\n";

        file << "LANGUAGE "
             << account->settings().language
             << "\n";

        file << "THEME "
             << account->settings().theme
             << "\n";

        file << "LINKED "
             << account->linkedAccounts().size()
             << "\n";

        for (const auto& linked :
             account->linkedAccounts())
        {
            file
                << linked.id << '\t'
                << linked.provider << '\t'
                << linked.type << '\t'
                << (linked.connected ? "1" : "0")
                << "\n";
        }

        file << "END_ACCOUNT\n";
    }

    return file.good();
}

bool AccountStorage::load(
    AccountManager& manager,
    const std::string& path
) {
    std::ifstream file(path);

    if (!file.is_open()) {
        return false;
    }

    std::string line;

    if (!std::getline(file, line)) {
        return false;
    }

    if (line != "CRYPTOPZ_ACCOUNTS_V1") {
        return false;
    }

    manager.clear();

    while (std::getline(file, line)) {

        if (line != "ACCOUNT") {
            continue;
        }

        std::string id;
        std::string username;
        std::string language = "vi";
        std::string theme = "dark";

        while (std::getline(file, line)) {

            if (line == "END_ACCOUNT") {
                break;
            }

            if (line.rfind("ID ", 0) == 0) {
                id = line.substr(3);
            }
            else if (
                line.rfind("USERNAME ", 0) == 0
            ) {
                username = line.substr(9);
            }
            else if (
                line.rfind("LANGUAGE ", 0) == 0
            ) {
                language = line.substr(9);
            }
            else if (
                line.rfind("THEME ", 0) == 0
            ) {
                theme = line.substr(6);
            }
            else if (
                line.rfind("LINKED ", 0) == 0
            ) {
                const int count =
                    std::stoi(line.substr(7));

                if (
                    id.empty() ||
                    username.empty()
                ) {
                    return false;
                }

                if (!manager.createAccount(
                    id,
                    username
                )) {
                    return false;
                }

                auto* account =
                    manager.getAccount(id);

                account->settings().language =
                    language;

                account->settings().theme =
                    theme;

                for (int i = 0; i < count; ++i) {

                    if (!std::getline(file, line)) {
                        return false;
                    }

                    const auto first =
                        line.find('\t');

                    const auto second =
                        line.find('\t', first + 1);

                    const auto third =
                        line.find('\t', second + 1);

                    if (
                        first == std::string::npos ||
                        second == std::string::npos ||
                        third == std::string::npos
                    ) {
                        return false;
                    }

                    LinkedAccount linked;

                    linked.id =
                        line.substr(0, first);

                    linked.provider =
                        line.substr(
                            first + 1,
                            second - first - 1
                        );

                    linked.type =
                        line.substr(
                            second + 1,
                            third - second - 1
                        );

                    linked.connected =
                        line.substr(third + 1)
                        == "1";

                    account->addLinkedAccount(
                        linked
                    );
                }
            }
        }
    }

    return true;
}

}
