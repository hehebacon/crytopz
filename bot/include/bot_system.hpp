#pragma once

#include "bot_storage.hpp"
#include "bot_registry.hpp"
#include "bot_loader.hpp"
#include "bot_factory.hpp"
#include "bot_validator.hpp"
#include "bot_runtime.hpp"
#include "bot_controller.hpp"

namespace crytopz {
namespace bot {

class BotSystem {
public:
BotSystem();


BotStorage& storage();
BotRegistry& registry();
BotLoader& loader();
BotFactory& factory();
BotValidator& validator();
BotRuntime& runtime();
BotController& controller();


private:
BotStorage storage_;
BotRegistry registry_;
BotFactory factory_;
BotValidator validator_;
BotRuntime runtime_;


BotLoader loader_;
BotController controller_;


};

}
}
