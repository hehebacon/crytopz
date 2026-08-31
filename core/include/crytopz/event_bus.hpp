#pragma once

#include "event.hpp"

#include <functional>
#include <vector>


namespace crytopz {


class EventBus
{

public:


    using Callback =
        std::function<void(const Event&)>;



    void subscribe(
        Callback callback
    );


    void emit(
        const Event& event
    );


private:

    std::vector<Callback> listeners_;

};


}