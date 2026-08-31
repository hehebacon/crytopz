#include "crytopz/bot_api.hpp"


namespace crytopz {


BotAPI::BotAPI(
    TradingEngine& engine
)
    :
    engine_(engine)
{
}



Price BotAPI::price(
    const Symbol& symbol
)
{
    return engine_
        .market()
        .get_ticker(symbol)
        .last;
}



std::uint64_t BotAPI::buy(
    const Symbol& symbol,
    Quantity quantity
)
{
    return engine_
        .place_market_order(
            symbol,
            Side::Buy,
            quantity
        );
}



std::uint64_t BotAPI::sell(
    const Symbol& symbol,
    Quantity quantity
)
{
    return engine_
        .place_market_order(
            symbol,
            Side::Sell,
            quantity
        );
}



Money BotAPI::balance()
{
    return engine_
        .account()
        .balance();
}


}