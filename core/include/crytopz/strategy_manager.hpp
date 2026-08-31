#pragma once

#include "strategy.hpp"
#include "execution.hpp"

#include <vector>
#include <memory>


namespace crytopz {


class StrategyManager
{

public:

    explicit StrategyManager(
        ExecutionEngine& execution
    );


    void add_strategy(
        std::unique_ptr<Strategy> strategy
    );


    void on_price(
        const Ticker& ticker
    );


private:

    ExecutionEngine& execution_;


    std::vector<
        std::unique_ptr<Strategy>
    > strategies_;

};


}