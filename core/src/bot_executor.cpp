#include "crytopz/bot_executor.hpp"

namespace crytopz {

BotExecutor::BotExecutor(
ExecutionEngine& execution
)
: execution_(execution)
{
}

void BotExecutor::process(
Bot& bot,
const Ticker& ticker
)
{
if (!bot.is_running())
return;


Signal signal =
    bot.on_price(ticker);

if (signal.type == SignalType::Hold)
    return;

execution_.execute(signal);


}

}
