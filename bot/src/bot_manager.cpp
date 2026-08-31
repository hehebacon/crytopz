#include "bot_manager.hpp"

#include <algorithm>
#include <utility>

namespace crytopz::bot {

bool BotManager::registerBot(
    std::unique_ptr<Bot> bot
)
{
    if (!bot)
        return false;

    if (bot->id().empty())
        return false;

    if (getBot(bot->id()))
        return false;

    bots_.push_back(std::move(bot));

    return true;
}

bool BotManager::unregisterBot(
    const std::string& id
)
{
    auto it = std::find_if(
        bots_.begin(),
        bots_.end(),
        [&](const auto& bot)
        {
            return bot &&
                   bot->id() == id;
        }
    );

    if (it == bots_.end())
        return false;

    if ((*it)->running())
        (*it)->stop();

    bots_.erase(it);

    return true;
}

Bot* BotManager::getBot(
    const std::string& id
)
{
    for (auto& bot : bots_)
    {
        if (bot && bot->id() == id)
            return bot.get();
    }

    return nullptr;
}

const Bot* BotManager::getBot(
    const std::string& id
) const
{
    for (const auto& bot : bots_)
    {
        if (bot && bot->id() == id)
            return bot.get();
    }

    return nullptr;
}

bool BotManager::startBot(
    const std::string& id
)
{
    Bot* bot = getBot(id);

    if (!bot)
        return false;

    return bot->start();
}

bool BotManager::stopBot(
    const std::string& id
)
{
    Bot* bot = getBot(id);

    if (!bot)
        return false;

    if (!bot->running())
        return false;

    bot->stop();

    return true;
}

void BotManager::stopAll()
{
    for (auto& bot : bots_)
    {
        if (bot && bot->running())
            bot->stop();
    }
}

std::size_t BotManager::count() const
{
    return bots_.size();
}

std::vector<const Bot*> BotManager::bots() const
{
    std::vector<const Bot*> result;

    result.reserve(bots_.size());

    for (const auto& bot : bots_)
    {
        if (bot)
            result.push_back(bot.get());
    }

    return result;
}

}