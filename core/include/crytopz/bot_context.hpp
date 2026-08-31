#pragma once

#include "bot_api.hpp"


namespace crytopz {


class BotContext
{

public:

    explicit BotContext(
        BotAPI& api
    );


    BotAPI& api();


private:

    BotAPI& api_;

};


}