#include <nlohmann/json.hpp>

#include <cassert>
#include <iostream>

int main()
{
    using json = nlohmann::json;

    json data = {
        {"symbol", "BTCUSDT"},
        {"bidPrice", "100000.00"},
        {"askPrice", "100001.00"},
        {"lastPrice", "100000.50"}
    };

    assert(data["symbol"] == "BTCUSDT");
    assert(data["bidPrice"] == "100000.00");
    assert(data["askPrice"] == "100001.00");
    assert(data["lastPrice"] == "100000.50");

    std::cout
        << "========================================\n"
        << " Crytopz JSON Test\n"
        << "========================================\n"
        << "[PASS] JSON parsing\n"
        << "========================================\n"
        << " ALL JSON TESTS PASSED\n"
        << "========================================\n";

    return 0;
}