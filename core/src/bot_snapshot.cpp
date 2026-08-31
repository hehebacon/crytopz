#include "crytopz/bot_snapshot.hpp"


namespace crytopz {



BotSnapshotService::BotSnapshotService(
    const BotManager& manager
)
:
manager_(manager)
{

}



std::vector<BotSnapshot>
BotSnapshotService::snapshot() const
{

    std::vector<BotSnapshot> result;


    for(const auto& bot_ptr : manager_.bots())
    {

        if(!bot_ptr)
        {
            continue;
        }


        const Bot& bot =
            *bot_ptr;


        const BotState& state =
            bot.state();


        BotSnapshot snapshot;


        snapshot.name =
            bot.name();


        snapshot.running =
            state.running;


        snapshot.trades =
            state.trades;


        snapshot.profit =
            state.profit;


        snapshot.last_action =
            state.last_action;



        for(const auto& log : state.logs)
        {
            snapshot.logs.push_back(
                log.message
            );
        }


        result.push_back(
            std::move(snapshot)
        );

    }


    return result;

}



BotSnapshot*
BotSnapshotService::find(
    const std::string& name
)
{

    for(const auto& bot_ptr : manager_.bots())
    {

        if(
            !bot_ptr
            ||
            bot_ptr->name() != name
        )
        {
            continue;
        }


        static BotSnapshot result;


        const BotState& state =
            bot_ptr->state();


        result.name =
            bot_ptr->name();


        result.running =
            state.running;


        result.trades =
            state.trades;


        result.profit =
            state.profit;


        result.last_action =
            state.last_action;


        result.logs.clear();


        for(const auto& log : state.logs)
        {
            result.logs.push_back(
                log.message
            );
        }


        return &result;

    }


    return nullptr;

}



}