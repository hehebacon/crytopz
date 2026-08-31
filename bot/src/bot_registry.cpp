#include "bot_registry.hpp"
#include "bot.hpp"

namespace crytopz {
namespace bot {

bool BotRegistry::registerBot(
Bot* bot
)
{
if (bot == 0)
return false;


if (contains(bot->id()))
    return false;

bots_.push_back(bot);

return true;


}

bool BotRegistry::unregisterBot(
const std::string& id
)
{
for (auto it = bots_.begin(); it != bots_.end(); ++it)
{
if ((*it)->id() == id)
{
bots_.erase(it);
return true;
}
}


return false;


}

Bot* BotRegistry::getBot(
const std::string& id
)
{
for (auto* bot : bots_)
{
if (bot != 0 && bot->id() == id)
return bot;
}


return 0;


}

const Bot* BotRegistry::getBot(
const std::string& id
) const
{
for (const auto* bot : bots_)
{
if (bot != 0 && bot->id() == id)
return bot;
}


return 0;


}

bool BotRegistry::contains(
const std::string& id
) const
{
return getBot(id) != 0;
}

std::size_t BotRegistry::size() const
{
return bots_.size();
}

void BotRegistry::clear()
{
bots_.clear();
}

const std::vector<Bot*>&
BotRegistry::bots() const
{
return bots_;
}

}
}
