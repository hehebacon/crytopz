#include "crytopz/core_bridge.hpp"
#include "crytopz/market.hpp"


namespace crytopz {


CoreBridge::CoreBridge()
{
}



double CoreBridge::get_price(
    const std::string& symbol
) const
{
    MarketData market;

    return market.get_price(symbol);
}


}
