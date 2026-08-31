#include "crytopz/bot_context.hpp"


namespace crytopz {


BotContext::BotContext(
    BotAPI& api
)
:
api_(api)
{
}



BotAPI& BotContext::api()
{
    return api_;
}


}