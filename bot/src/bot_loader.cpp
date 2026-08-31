#include "bot_loader.hpp"

namespace crytopz {
namespace bot {

BotLoader::BotLoader(
BotStorage& storage,
BotRegistry& registry
)
: storage_(storage),
registry_(registry)
{
}

bool BotLoader::load(
const std::string& id
)
{
if (isLoaded(id))
return false;


BotRecord* record = storage_.getBot(id);

if (record == 0)
    return false;

return true;


}

bool BotLoader::unload(
const std::string& id
)
{
return registry_.unregisterBot(id);
}

bool BotLoader::isLoaded(
const std::string& id
) const
{
return registry_.contains(id);
}

}
}
