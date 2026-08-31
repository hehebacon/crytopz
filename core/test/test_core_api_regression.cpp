#include "crytopz/core_api.hpp"

#include <cassert>
#include <cmath>
#include <iostream>

using namespace crytopz;

namespace
{
bool near(double a, double b, double eps = 1e-9)
{
    return std::fabs(a - b) <= eps;
}
}

int main()
{
    std::cout
        << "========================================\n"
        << " Crytopz Core API Regression Test\n"
        << "========================================\n";

    // ========================================================
    // Create
    // ========================================================

    CoreAPI core(10000.0);

    assert(near(core.balance(), 10000.0));
    assert(near(core.equity(), 10000.0));
    assert(near(core.position_value(), 0.0));
    assert(near(core.realized_pnl(), 0.0));
    assert(near(core.unrealized_pnl(), 0.0));
    assert(near(core.total_pnl(), 0.0));
    assert(core.order_count() == 0);

    std::cout << "[PASS] Initial account state\n";


    // ========================================================
    // Market
    // ========================================================

    core.update_market(
        "BTCUSDT",
        100000.0,
        100010.0,
        100005.0,
        1
    );

    assert(
        near(
            core.get_price("BTCUSDT"),
            100005.0
        )
    );

    std::cout << "[PASS] Market update\n";


    // ========================================================
    // BUY
    // ========================================================

    const auto buy_id =
        core.buy(
            "BTCUSDT",
            0.01
        );

    assert(buy_id != 0);
    assert(core.order_count() == 1);

    auto position =
        core.position("BTCUSDT");

    assert(
        near(
            position.quantity,
            0.01
        )
    );

    assert(
        near(
            position.average_price,
            100010.0
        )
    );

    assert(
        near(
            core.balance(),
            8999.90
        )
    );

    std::cout << "[PASS] BUY\n";


    // ========================================================
    // Unrealized PnL
    // ========================================================

    core.update_market(
        "BTCUSDT",
        100095.0,
        100100.0,
        100095.0,
        2
    );

    assert(
        near(
            core.unrealized_pnl(),
            0.85
        )
    );

    assert(
        near(
            core.equity(),
            10000.85
        )
    );

    assert(
        near(
            core.total_pnl(),
            0.85
        )
    );

    std::cout << "[PASS] Unrealized PnL\n";


    // ========================================================
    // SELL
    // ========================================================

    const auto sell_id =
        core.sell(
            "BTCUSDT",
            0.01
        );

    assert(sell_id != 0);
    assert(core.order_count() == 2);

    position =
        core.position("BTCUSDT");

    assert(
        near(
            position.quantity,
            0.0
        )
    );

    std::cout << "[PASS] SELL\n";


    // ========================================================
    // Realized PnL
    // ========================================================

    assert(
        near(
            core.realized_pnl(),
            0.80
        )
    );

    assert(
        near(
            core.unrealized_pnl(),
            0.0
        )
    );

    assert(
        near(
            core.position_value(),
            0.0
        )
    );

    assert(
        near(
            core.equity(),
            10000.80
        )
    );

    assert(
        near(
            core.total_pnl(),
            0.80
        )
    );

    assert(
        near(
            core.balance(),
            10000.80
        )
    );

    std::cout << "[PASS] Realized PnL\n";


    // ========================================================
    // Final state
    // ========================================================

    assert(core.order_count() == 2);

    const Order* order0 =
        core.get_order(0);

    const Order* order1 =
        core.get_order(1);

    assert(order0 != nullptr);
    assert(order1 != nullptr);

    assert(order0->id == buy_id);
    assert(order1->id == sell_id);

    assert(order0->symbol.value == "BTCUSDT");
    assert(order1->symbol.value == "BTCUSDT");

    assert(order0->quantity == 0.01);
    assert(order1->quantity == 0.01);

    std::cout << "[PASS] Order history\n";


    std::cout
        << "========================================\n"
        << " ALL CORE API REGRESSION TESTS PASSED\n"
        << "========================================\n";

    return 0;
}