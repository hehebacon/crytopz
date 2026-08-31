#include "bot_factory.hpp"
#include "simple_bot.hpp"

namespace crytopz {
namespace bot {

std::unique_ptr<Bot>
BotFactory::create(
const std::string& type
) const
{
if (type == "simple")
{
return std::make_unique<SimpleBot>();
}


return std::unique_ptr<Bot>();


}

}
}
