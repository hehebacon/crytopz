#pragma once

#include <string>

#include "bot_loader.hpp"
#include "bot_runtime.hpp"

namespace crytopz {
namespace bot {

class BotController {
public:
BotController(
BotLoader& loader,
BotRuntime& runtime
);


bool start(
    const std::string& id
);

bool stop(
    const std::string& id
);

bool unload(
    const std::string& id
);

bool running(
    const std::string& id
) const;


private:
BotLoader& loader_;
BotRuntime& runtime_;
};

}
}
