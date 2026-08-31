#pragma once

#include <string>
#include <vector>

namespace crytopz::bot {

struct BotRecord {
std::string id;
std::string name;
std::string version;
std::string author;
std::string description;
bool enabled = false;
};

class BotStorage {
public:
BotStorage() = default;

bool addBot(const BotRecord& bot);

bool removeBot(const std::string& id);

BotRecord* getBot(const std::string& id);

const BotRecord* getBot(const std::string& id) const;

bool contains(const std::string& id) const;

std::size_t size() const;

const std::vector<BotRecord>& bots() const;

void clear();

bool save(const std::string& path) const;

bool load(const std::string& path);

private:
std::vector<BotRecord> bots_;
};

}
