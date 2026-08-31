#pragma once

#include <string>
#include <vector>
#include <functional>


namespace crytopz {


struct BotEvent
{
    std::string bot_name;

    std::string message;
};



class BotEventBus
{

public:


    using Callback =
        std::function<void(
            const BotEvent&
        )>;



    void subscribe(
        Callback callback
    )
    {
        listeners_.push_back(
            callback
        );
    }



    void emit(
        const std::string& bot_name,
        const std::string& message
    )
    {

        BotEvent event;

        event.bot_name =
            bot_name;

        event.message =
            message;



        for(auto& listener : listeners_)
        {
            listener(event);
        }

    }



private:

    std::vector<Callback> listeners_;

};


}