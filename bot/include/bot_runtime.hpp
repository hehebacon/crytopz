#pragma once

#include "crytopz/bot.hpp"

namespace crytopz {
namespace bot {

class BotRuntime {
public:
BotRuntime() = default;


bool start(
    Bot& bot
);

bool stop(
    Bot& bot
);

bool running(
    const Bot& bot
) const;


};

}
}
