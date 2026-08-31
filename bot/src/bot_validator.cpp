#include "bot_validator.hpp"

namespace crytopz {
namespace bot {

bool BotValidator::validate(
const BotManifest& manifest
) const
{
if (!manifest.valid())
return false;


if (manifest.type != "simple")
    return false;

return true;


}

}
}
