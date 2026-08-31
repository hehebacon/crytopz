#pragma once

#include "crytopz/bot.hpp"

#include <vector>
#include <memory>
#include <string>
#include <cstddef>


namespace crytopz {


class BotManager
{

public:

    // Add a bot.
    // Returns false if the bot is null
    // or another bot has the same name.
    bool add_bot(
        std::unique_ptr<Bot> bot
    );


    // Remove bot by name.
    // Returns true if removed.
    bool remove_bot(
        const std::string& name
    );


    // Start / stop one bot.
    bool start_bot(
        const std::string& name
    );


    bool stop_bot(
        const std::string& name
    );


    // Start / stop all bots.
    void start_all();

    void stop_all();


    // Find bot.
    Bot* get_bot(
        const std::string& name
    );


    const Bot* get_bot(
        const std::string& name
    ) const;


    // Access all bots.
    const std::vector<
        std::unique_ptr<Bot>
    >& bots() const;


    // Number of registered bots.
    std::size_t count() const;


private:

    std::vector<
        std::unique_ptr<Bot>
    > bots_;

};


}