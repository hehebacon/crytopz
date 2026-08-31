#include "crytopz/simple_bot.hpp"

#include <iostream>

namespace crytopz {

Signal SimpleBot::on_price(
const Ticker& ticker
)
{
Signal signal;


signal.type = SignalType::Hold;
signal.symbol = ticker.symbol;
signal.quantity = 0.01;

if (!initialized_)
{
    last_price_ = ticker.last;
    initialized_ = true;
    return signal;
}

if (ticker.last > last_price_)
{
    signal.type = SignalType::Buy;

    std::cout
        << "[BOT SIGNAL] BUY "
        << ticker.symbol.value
        << " @ "
        << ticker.last
        << "\n";
}
else if (ticker.last < last_price_)
{
    signal.type = SignalType::Sell;

    std::cout
        << "[BOT SIGNAL] SELL "
        << ticker.symbol.value
        << " @ "
        << ticker.last
        << "\n";
}

last_price_ = ticker.last;

return signal;


}

}

