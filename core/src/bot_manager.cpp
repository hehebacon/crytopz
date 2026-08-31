#include "crytopz/bot_manager.hpp"


namespace crytopz {


bool BotManager::add_bot(
    std::unique_ptr<Bot> bot
)
{

    if(!bot)
    {
        return false;
    }


    if(
        get_bot(
            bot->name()
        )
        != nullptr
    )
    {
        return false;
    }


    bots_.push_back(
        std::move(bot)
    );


    return true;
}



bool BotManager::remove_bot(
    const std::string& name
)
{

    for(auto it = bots_.begin();
        it != bots_.end();
        ++it)
    {

        if(
            (*it)->name()
            ==
            name
        )
        {

            bots_.erase(it);

            return true;
        }

    }


    return false;
}



bool BotManager::start_bot(
    const std::string& name
)
{

    Bot* bot =
        get_bot(name);


    if(!bot)
    {
        return false;
    }


    bot->start();

    return true;
}



bool BotManager::stop_bot(
    const std::string& name
)
{

    Bot* bot =
        get_bot(name);


    if(!bot)
    {
        return false;
    }


    bot->stop();

    return true;
}



void BotManager::start_all()
{

    for(auto& bot : bots_)
    {

        if(bot)
        {
            bot->start();
        }

    }

}



void BotManager::stop_all()
{

    for(auto& bot : bots_)
    {

        if(bot)
        {
            bot->stop();
        }

    }

}



Bot* BotManager::get_bot(
    const std::string& name
)
{

    for(auto& bot : bots_)
    {

        if(
            bot
            &&
            bot->name()
            ==
            name
        )
        {
            return bot.get();
        }

    }


    return nullptr;
}



const Bot* BotManager::get_bot(
    const std::string& name
) const
{

    for(const auto& bot : bots_)
    {

        if(
            bot
            &&
            bot->name()
            ==
            name
        )
        {
            return bot.get();
        }

    }


    return nullptr;
}



const std::vector<
    std::unique_ptr<Bot>
>& BotManager::bots() const
{
    return bots_;
}



std::size_t BotManager::count() const
{
    return bots_.size();
}


}
