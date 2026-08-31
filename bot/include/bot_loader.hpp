#pragma once

#include <string>

#include "bot_storage.hpp"
#include "bot_registry.hpp"

namespace crytopz {
namespace bot {

class BotLoader {
public:
BotLoader(
BotStorage& storage,
BotRegistry& registry
);


bool load(
    const std::string& id
);

bool unload(
    const std::string& id
);

bool isLoaded(
    const std::string& id
) const;


private:
BotStorage& storage_;
BotRegistry& registry_;
};

}
}
