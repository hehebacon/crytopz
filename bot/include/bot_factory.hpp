#pragma once

#include <memory>
#include <string>

#include "bot.hpp"

namespace crytopz {
namespace bot {

class BotFactory {
public:
BotFactory() = default;


std::unique_ptr<Bot> create(
    const std::string& type
) const;


};

}
}
