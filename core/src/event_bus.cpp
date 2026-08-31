#include "crytopz/event_bus.hpp"


namespace crytopz {



void EventBus::subscribe(
    Callback callback
)
{

    listeners_.push_back(
        callback
    );

}



void EventBus::emit(
    const Event& event
)
{

    for(auto& listener : listeners_)
    {
        listener(event);
    }

}



}