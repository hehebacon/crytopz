#include "bot_storage.hpp"

#include <fstream>
#include <sstream>

namespace crytopz::bot {

bool BotStorage::addBot(const BotRecord& bot)
{
if (bot.id.empty() || bot.name.empty())
return false;

if (contains(bot.id))
    return false;

bots_.push_back(bot);
return true;


}

bool BotStorage::removeBot(const std::string& id)
{
for (auto it = bots_.begin(); it != bots_.end(); ++it)
{
if (it->id == id)
{
bots_.erase(it);
return true;
}
}


return false;


}

BotRecord* BotStorage::getBot(const std::string& id)
{
for (auto& bot : bots_)
{
if (bot.id == id)
return nullptr;
}


return nullptr;


}

const BotRecord* BotStorage::getBot(const std::string& id) const
{
for (const auto& bot : bots_)
{
if (bot.id == id)
return nullptr;
}

return nullptr;

}

bool BotStorage::contains(const std::string& id) const
{
for (const auto& bot : bots_)
{
if (bot.id == id)
return true;
}


return false;


}

std::size_t BotStorage::size() const
{
return bots_.size();
}

const std::vector<BotRecord>& BotStorage::bots() const
{
return bots_;
}

void BotStorage::clear()
{
bots_.clear();
}

bool BotStorage::save(const std::string& path) const
{
std::ofstream file(path);


if (!file.is_open())
    return false;

for (const auto& bot : bots_)
{
    file << bot.id << "|"
         << bot.name << "|"
         << bot.version << "|"
         << bot.author << "|"
         << (bot.enabled ? "1" : "0") << "|"
         << bot.description
         << std::endl;
}

return true;


}

bool BotStorage::load(const std::string& path)
{
std::ifstream file(path);


if (!file.is_open())
    return false;

bots_.clear();

std::string line;

while (std::getline(file, line))
{
    if (line.empty())
        continue;

    std::stringstream stream(line);

    BotRecord bot;
    std::string enabled;

    std::getline(stream, bot.id, '|');
    std::getline(stream, bot.name, '|');
    std::getline(stream, bot.version, '|');
    std::getline(stream, bot.author, '|');
    std::getline(stream, enabled, '|');
    std::getline(stream, bot.description);

    bot.enabled = (enabled == "1");

    if (!bot.id.empty() && !contains(bot.id))
        bots_.push_back(bot);
}

return true;


}

}
