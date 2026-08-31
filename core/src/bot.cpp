#include "crytopz/bot.hpp"

namespace crytopz {

Bot::Bot(
const std::string& name,
Strategy* strategy,
BotEventBus& events
)
: name_(name),
strategy_(strategy),
events_(events)
{
}

void Bot::start()
{
if (state_.running)
return;


state_.running = true;
state_.last_action = "started";

events_.emit(
    name_,
    "started"
);


}

void Bot::stop()
{
if (!state_.running)
return;


state_.running = false;
state_.last_action = "stopped";

events_.emit(
    name_,
    "stopped"
);


}

bool Bot::is_running() const
{
return state_.running;
}

const std::string& Bot::name() const
{
return name_;
}

BotState& Bot::state()
{
return state_;
}

const BotState& Bot::state() const
{
return state_;
}

Signal Bot::on_price(
const Ticker& ticker
)
{
if (!state_.running)
{
return Signal{
SignalType::Hold,
ticker.symbol,
0
};
}


if (!strategy_)
{
    return Signal{
        SignalType::Hold,
        ticker.symbol,
        0
    };
}

Signal signal =
    strategy_->on_price(ticker);

if (signal.type != SignalType::Hold)
{
    state_.trades++;

    if (signal.type == SignalType::Buy)
        state_.last_action = "buy";
    else if (signal.type == SignalType::Sell)
        state_.last_action = "sell";
}

return signal;


}

}

