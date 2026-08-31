#pragma once

#include <string>
#include <vector>

namespace crytopz {
namespace bot {

class Bot;

class BotRegistry {
public:
BotRegistry() = default;

bool registerBot(
    Bot* bot
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

bool contains(
    const std::string& id
) const;

std::size_t size() const;

void clear();

const std::vector<Bot*>& bots() const;


private:
std::vector<Bot*> bots_;
};

}
}
