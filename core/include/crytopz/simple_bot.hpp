#pragma once

#include "strategy.hpp"

namespace crytopz {

class SimpleBot : public Strategy
{
public:
Signal on_price(
const Ticker& ticker
) override;

private:
double last_price_ = 0.0;
bool initialized_ = false;
};

}
