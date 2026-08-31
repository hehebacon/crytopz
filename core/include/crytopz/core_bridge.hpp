#pragma once

#include <string>

namespace crytopz {

class CoreBridge
{
public:

    CoreBridge();

    double get_price(
        const std::string& symbol
    ) const;
};

}