#include "bot_runtime.hpp"

namespace crytopz {
namespace bot {

bool BotRuntime::start(Bot& bot)
{
if (bot.is_running())
return false;


bot.start();

return bot.is_running();

}

bool BotRuntime::stop(Bot& bot)
{
if (!bot.is_running())
return false;


bot.stop();

return !bot.is_running();


}

bool BotRuntime::running(const Bot& bot) const
{
return bot.is_running();
}

}
}

