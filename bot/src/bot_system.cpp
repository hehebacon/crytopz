#include "bot_system.hpp"

namespace crytopz {
namespace bot {

BotSystem::BotSystem()
: loader_(storage_, registry_),
controller_(loader_, runtime_)
{
}

BotStorage& BotSystem::storage()
{
return storage_;
}

BotRegistry& BotSystem::registry()
{
return registry_;
}

BotLoader& BotSystem::loader()
{
return loader_;
}

BotFactory& BotSystem::factory()
{
return factory_;
}

BotValidator& BotSystem::validator()
{
return validator_;
}

BotRuntime& BotSystem::runtime()
{
return runtime_;
}

BotController& BotSystem::controller()
{
return controller_;
}

}
}
