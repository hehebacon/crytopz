#pragma once

#include "crytopz/bot_manager.hpp"

#include <string>
#include <vector>


namespace crytopz {


struct BotSnapshot
{
    std::string name;

    bool running = false;

    int trades = 0;

    double profit = 0.0;

    std::string last_action;

    std::vector<std::string> logs;
};



class BotSnapshotService
{

public:

    explicit BotSnapshotService(
        const BotManager& manager
    );


    std::vector<BotSnapshot> snapshot() const;


    BotSnapshot* find(
        const std::string& name
    );


private:

    const BotManager& manager_;

};


}