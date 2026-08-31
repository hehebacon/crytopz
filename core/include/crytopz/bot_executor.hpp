#pragma once

#include "bot.hpp"
#include "execution.hpp"

namespace crytopz {

class BotExecutor
{
public:
explicit BotExecutor(
ExecutionEngine& execution
);


void process(
    Bot& bot,
    const Ticker& ticker
);


private:
ExecutionEngine& execution_;
};

}
