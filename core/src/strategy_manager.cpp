#include "crytopz/strategy_manager.hpp"


namespace crytopz {


StrategyManager::StrategyManager(
    ExecutionEngine& execution
)
:
execution_(execution)
{

}



void StrategyManager::add_strategy(
    std::unique_ptr<Strategy> strategy
)
{

    strategies_.push_back(
        std::move(strategy)
    );

}



void StrategyManager::on_price(
    const Ticker& ticker
)
{

    for(auto& strategy : strategies_)
    {

        auto signal =
            strategy->on_price(
                ticker
            );


        if(
            signal.type != SignalType::Hold
        )
        {

            execution_.execute(
                signal
            );

        }

    }

}


}
