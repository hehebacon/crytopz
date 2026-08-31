#pragma once

#include "crytopz/strategy.hpp"
#include "crytopz/bot_event.hpp"

#include <string>
#include <vector>


namespace crytopz {


// =========================================================
// BOT LOG
// =========================================================

struct BotLog
{
    std::string message;
};


// =========================================================
// BOT STATE
// =========================================================

struct BotState
{
    bool running = false;

    int trades = 0;

    double profit = 0.0;

    std::string last_action;

    std::vector<BotLog> logs;
};


// =========================================================
// BOT
// =========================================================

class Bot
{

public:

    Bot(
        const std::string& name,
        Strategy* strategy,
        BotEventBus& events
    );


    // -----------------------------------------------------
    // LIFECYCLE
    // -----------------------------------------------------

    void start();

    void stop();

    bool is_running() const;


    // -----------------------------------------------------
    // INFO
    // -----------------------------------------------------

    const std::string& name() const;


    // -----------------------------------------------------
    // STATE
    // -----------------------------------------------------

    BotState& state();

    const BotState& state() const;


    // -----------------------------------------------------
    // STRATEGY
    // -----------------------------------------------------

    Signal on_price(
        const Ticker& ticker
    );


private:

    std::string name_;

    Strategy* strategy_;

    BotState state_;

    BotEventBus& events_;

};

}
