#include <iostream>

#include "crytopz/engine.hpp"
#include "crytopz/bot_api.hpp"


using namespace crytopz;


int main()
{

    std::cout 
        << "=== crytopz Bot API Test ===\n";


    TradingEngine engine(
        100000.0
    );


    Symbol btc(
        "BTCUSDT"
    );


    engine.update_market(
        btc,
        99900,
        100000,
        99950,
        1
    );


    BotAPI api(
        engine
    );


    std::cout
        << "BTC Price: "
        << api.price(btc)
        << "\n";


    auto buy =
        api.buy(
            btc,
            0.1
        );


    std::cout
        << "BUY ID: "
        << buy
        << "\n";


    std::cout
        << "Balance: "
        << api.balance()
        << "\n";


    auto sell =
        api.sell(
            btc,
            0.1
        );


    std::cout
        << "SELL ID: "
        << sell
        << "\n";


    std::cout
        << "Final Balance: "
        << api.balance()
        << "\n";


    return 0;
}
