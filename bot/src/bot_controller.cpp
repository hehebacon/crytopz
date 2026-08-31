#include "bot_controller.hpp"

namespace crytopz {
namespace bot {

BotController::BotController(
BotLoader& loader,
BotRuntime& runtime
)
: loader_(loader),
runtime_(runtime)
{
}

bool BotController::start(
const std::string& id
)
{
if (!loader_.isLoaded(id))
{
if (!loader_.load(id))
return false;
}


return true;


}

bool BotController::stop(
const std::string& id
)
{
return false;
}

bool BotController::unload(
const std::string& id
)
{
return loader_.unload(id);
}

bool BotController::running(
const std::string& id
) const
{
return false;
}

}
}
