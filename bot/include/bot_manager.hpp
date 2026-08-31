#pragma once

#include "bot.hpp"

#include <memory>
#include <string>
#include <vector>

namespace crytopz::bot {

class BotManager {
public:
    BotManager() = default;
    ~BotManager() = default;

    BotManager(const BotManager&) = delete;
    BotManager& operator=(const BotManager&) = delete;

    bool registerBot(
        std::unique_ptr<Bot> bot
    );

    bool unregisterBot(
        const std::string& id
    );

    Bot* getBot(
        const std::string& id
    );

    const Bot* getBot(
        const std::string& id
    ) const;

    bool startBot(
        const std::string& id
    );

    bool stopBot(
        const std::string& id
    );

    void stopAll();

    std::size_t count() const;

    std::vector<const Bot*> bots() const;

private:
    std::vector<std::unique_ptr<Bot>> bots_;
};

}