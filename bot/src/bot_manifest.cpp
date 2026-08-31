#include "bot_manifest.hpp"

namespace crytopz {
namespace bot {

bool BotManifest::valid() const
{
if (id.empty())
return false;


if (name.empty())
    return false;

if (version.empty())
    return false;

if (type.empty())
    return false;

return true;


}

}
}
