
#include "crytopz/core_api.hpp"

#include <cassert>
#include <cmath>
#include <iostream>

namespace
{

bool nearly_equal(
    double a,
    double b,
    double epsilon = 1e-9
)
{
    return std::abs(a - b) <= epsilon;
}

void test_initial_state()
{
    crytopz::CoreAPI core(10'000.0);

    assert(nearly_equal(
        core.balance(),
        10'000.0
    ));

    assert(nearly_equal(
        core.realized_pnl(),
        0.0
    ));

    assert(
        core.order_count() == 0
    );

    std::cout
        << "[PASS] Initial state\n";
}


void test_market()
{
    crytopz::CoreAPI core(10'000.0);

    core.update_market(
        "BTCUSDT",
        100'000.0,
        100'010.0,
        100'005.0,
        123456789
    );

    assert(nearly_equal(
        core.get_price("BTCUSDT"),
        100'005.0
    ));

    std::cout
        << "[PASS] Market update\n";
}


void test_buy()
{
    crytopz::CoreAPI core(10'000.0);

    core.update_market(
        "BTCUSDT",
        100'000.0,
        100'010.0,
        100'005.0,
        1
    );

    const auto order_id =
        core.buy(
            "BTCUSDT",
            0.01
        );

    assert(order_id != 0);

    assert(nearly_equal(
        core.balance(),
        8'999.9
    ));

    const auto position =
        core.position("BTCUSDT");

    assert(nearly_equal(
        position.quantity,
        0.01
    ));

    assert(nearly_equal(
        position.average_price,
        100'010.0
    ));

    assert(
        core.order_count() == 1
    );

    const auto* order =
        core.get_order(0);

    assert(order != nullptr);
    assert(order->id == order_id);
    assert(order->symbol.value == "BTCUSDT");
    assert(order->side == crytopz::Side::Buy);
    assert(order->quantity == 0.01);

    std::cout
        << "[PASS] Market buy\n";
}


void test_sell()
{
    crytopz::CoreAPI core(10'000.0);

    core.update_market(
        "BTCUSDT",
        100'000.0,
        100'010.0,
        100'005.0,
        1
    );

    const auto buy_id =
        core.buy(
            "BTCUSDT",
            0.01
        );

    assert(buy_id != 0);

    core.update_market(
        "BTCUSDT",
        100'100.0,
        100'110.0,
        100'105.0,
        2
    );

    const auto sell_id =
        core.sell(
            "BTCUSDT",
            0.01
        );

    assert(sell_id != 0);

    assert(nearly_equal(
        core.balance(),
        10'001.0
    ));

    const auto position =
        core.position("BTCUSDT");

    assert(nearly_equal(
        position.quantity,
        0.0
    ));

    assert(nearly_equal(
        position.average_price,
        0.0
    ));

    assert(nearly_equal(
        core.realized_pnl(),
        1.0
    ));

    assert(
        core.order_count() == 2
    );

    std::cout
        << "[PASS] Market sell + realized PnL\n";
}


void test_invalid_orders()
{
    crytopz::CoreAPI core(10'000.0);

    core.update_market(
        "BTCUSDT",
        100'000.0,
        100'010.0,
        100'005.0,
        1
    );

    // Invalid quantity
    assert(
        core.buy("BTCUSDT", 0.0) == 0
    );

    assert(
        core.buy("BTCUSDT", -1.0) == 0
    );

    // Not enough balance
    assert(
        core.buy("BTCUSDT", 1.0) == 0
    );

    // Cannot sell a position that does not exist
    assert(
        core.sell("BTCUSDT", 0.01) == 0
    );

    assert(
        core.order_count() == 0
    );

    std::cout
        << "[PASS] Invalid orders\n";
}


void test_order_history()
{
    crytopz::CoreAPI core(10'000.0);

    core.update_market(
        "ETHUSDT",
        3'000.0,
        3'001.0,
        3'000.5,
        1
    );

    const auto first =
        core.buy(
            "ETHUSDT",
            1.0
        );

    assert(first != 0);

    const auto second =
        core.sell(
            "ETHUSDT",
            0.5
        );

    assert(second != 0);

    assert(
        core.order_count() == 2
    );

    const auto* order0 =
        core.get_order(0);

    const auto* order1 =
        core.get_order(1);

    assert(order0 != nullptr);
    assert(order1 != nullptr);

    assert(order0->id == first);
    assert(order1->id == second);

    assert(
        order0->side == crytopz::Side::Buy
    );

    assert(
        order1->side == crytopz::Side::Sell
    );

    // Out of range must return nullptr.
    assert(
        core.get_order(2) == nullptr
    );

    std::cout
        << "[PASS] Order history\n";
}

}


int main()
{
    std::cout
        << "========================================\n"
        << " Crytopz Core Test Suite\n"
        << "========================================\n";

    test_initial_state();
    test_market();
    test_buy();
    test_sell();
    test_invalid_orders();
    test_order_history();

    std::cout
        << "========================================\n"
        << " ALL CORE TESTS PASSED\n"
        << "========================================\n";

    return 0;
}

