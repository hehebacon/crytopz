#pragma once

#include <string>

namespace crytopz {
namespace bot {

struct BotManifest {
std::string id;
std::string name;
std::string version;
std::string author;
std::string type;
std::string description;


bool valid() const;


};

}
}
