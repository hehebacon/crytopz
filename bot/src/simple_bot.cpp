#include "simple_bot.hpp"

namespace crytopz::bot {

SimpleBot::SimpleBot()
    : id_("simple_bot"),
      name_("SimpleBot")
{
}

const std::string& SimpleBot::id() const
{
    return id_;
}

const std::string& SimpleBot::name() const
{
    return name_;
}

bool SimpleBot::start()
{
    if (running_)
        return false;

    running_ = true;
    return true;
}

void SimpleBot::stop()
{
    running_ = false;
}

bool SimpleBot::running() const
{
    return running_;
}

void SimpleBot::onMarketUpdate(
    const std::string& symbol,
    double price
)
{
    if (!running_)
        return;

    // Strategy logic will be added later.
    (void)symbol;
    (void)price;
}

}