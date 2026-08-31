#pragma once

#include "bot_manifest.hpp"

namespace crytopz {
namespace bot {

class BotValidator {
public:
BotValidator() = default;


bool validate(
    const BotManifest& manifest
) const;


};

}
}
