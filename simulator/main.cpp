#include <iostream>
#include <memory>
#include <string>

#include "crytopz/engine.hpp"
#include "crytopz/simulator_feed.hpp"
#include "crytopz/execution.hpp"
#include "crytopz/bot_executor.hpp"
#include "crytopz/strategy_manager.hpp"
#include "crytopz/simple_bot.hpp"
#include "crytopz/bot.hpp"
#include "crytopz/bot_manager.hpp"
#include "crytopz/bot_event.hpp"

#include "account_manager.hpp"
#include "account_storage.hpp"
#include "session_manager.hpp"
#include "credential.hpp"

using namespace crytopz;

void print_separator(const char* title)
{
std::cout
<< "\n========================================\n"
<< title
<< "\n========================================\n";
}

void print_account(
const TradingEngine& engine,
const Symbol& symbol
)
{
const auto position =
engine.account().get_position(symbol);


print_separator("TRADING ACCOUNT");

std::cout << "Balance: "
          << engine.account().balance()
          << "\n";

std::cout << "Position: "
          << position.quantity
          << "\n";

std::cout << "Average Price: "
          << position.average_price
          << "\n";


}

bool test_crytopz_accounts()
{
print_separator("CRYPTOPZ ACCOUNT SYSTEM");


crytopz::identity::AccountManager manager;

if (!manager.createAccount("user_001", "test_user"))
    return false;

auto* account = manager.getAccount("user_001");

if (!account)
    return false;

account->setCredential(
    crytopz::identity::Credential::create(
        "test_password"
    )
);

account->settings().language = "vi";
account->settings().theme = "dark";

account->addLinkedAccount({
    "linked_crypto_001",
    "demo_exchange",
    "crypto",
    true
});

account->addLinkedAccount({
    "linked_stock_001",
    "demo_broker",
    "stocks",
    true
});

std::cout << "Account ID: "
          << account->id()
          << "\n";

std::cout << "Username: "
          << account->username()
          << "\n";

std::cout << "Language: "
          << account->settings().language
          << "\n";

std::cout << "Theme: "
          << account->settings().theme
          << "\n";

std::cout << "Linked Accounts: "
          << account->linkedAccounts().size()
          << "\n";

const std::string storage_path = "accounts.dat";

if (!crytopz::identity::AccountStorage::save(
    manager,
    storage_path
))
    return false;

std::cout << "[ACCOUNT] Saved successfully\n";

manager.clear();

std::cout << "Accounts after clear: "
          << manager.accountCount()
          << "\n";

if (!crytopz::identity::AccountStorage::load(
    manager,
    storage_path
))
    return false;

auto* restored =
    manager.getAccount("user_001");

if (!restored)
    return false;

std::cout << "[ACCOUNT] Restored successfully\n";

std::cout << "Restored Username: "
          << restored->username()
          << "\n";

std::cout << "Restored Theme: "
          << restored->settings().theme
          << "\n";

std::cout << "Restored Linked Accounts: "
          << restored->linkedAccounts().size()
          << "\n";

return true;


}

bool test_session()
{
print_separator("SESSION SYSTEM");


crytopz::identity::AccountManager manager;

if (!manager.createAccount(
    "user_001",
    "test_user"
))
    return false;

auto* account =
    manager.getAccount("user_001");

if (!account)
    return false;

account->setCredential(
    crytopz::identity::Credential::create(
        "test_password"
    )
);

crytopz::identity::SessionManager session(
    manager
);

std::cout
    << "Before login: "
    << (session.isLoggedIn() ? "YES" : "NO")
    << "\n";

if (!session.login(
    "user_001",
    "test_password"
))
    return false;

std::cout
    << "Logged in: "
    << (session.isLoggedIn() ? "YES" : "NO")
    << "\n";

std::cout
    << "Current account: "
    << session.currentAccountId()
    << "\n";

std::string token;

if (session.sessionToken())
    token = session.sessionToken()->value();

std::cout
    << "Session token: "
    << token
    << "\n";

if (!session.validateToken(token))
    return false;

std::cout << "[SESSION] Token validated\n";

auto* token_account =
    session.accountFromToken(token);

if (!token_account)
    return false;

std::cout
    << "Token account: "
    << token_account->username()
    << "\n";

if (session.validateToken("invalid_token"))
    return false;

std::cout
    << "[SESSION] Invalid token rejected\n";

if (session.login(
    "user_001",
    "wrong_password"
))
    return false;

std::cout
    << "[SESSION] Wrong password rejected\n";

session.logout();

std::cout
    << "After logout: "
    << (session.isLoggedIn() ? "YES" : "NO")
    << "\n";

if (session.validateToken(token))
    return false;

std::cout
    << "[SESSION] Token invalidated after logout\n";

if (session.accountFromToken(token))
    return false;

std::cout
    << "[SESSION] Old token account access rejected\n";

return true;


}

int main()
{
if (!test_crytopz_accounts())
return 1;


if (!test_session())
    return 1;

TradingEngine engine(10'000.0);

Symbol btc{"BTCUSDT"};
Symbol eth{"ETHUSDT"};

ExecutionEngine execution(engine);

BotExecutor bot_executor(execution);

BotEventBus bot_events;

bot_events.subscribe(
    [](const BotEvent& event)
    {
        std::cout
            << "[BOT EVENT] "
            << event.message
            << "\n";
    }
);

BotManager bots;

auto bot =
    std::make_unique<Bot>(
        "SimpleBot",
        new SimpleBot(),
        bot_events
    );

bots.add_bot(std::move(bot));

bots.start_all();

engine.events().subscribe(
    [&](const Event& event)
    {
        if (event.type == EventType::PriceUpdated)
        {
            std::cout
                << "[PRICE] "
                << event.symbol.value
                << " "
                << event.price
                << "\n";

            const auto ticker =
                engine.market().get_ticker(
                    event.symbol
                );

            for (const auto& managed_bot : bots.bots())
            {
                if (
                    managed_bot &&
                    managed_bot->is_running()
                )
                {
                    bot_executor.process(
                        *managed_bot,
                        ticker
                    );
                }
            }
        }

        if (event.type == EventType::OrderFilled)
        {
            std::cout
                << "[FILLED] "
                << event.symbol.value
                << " "
                << event.quantity
                << " @ "
                << event.price
                << "\n";
        }
    }
);

print_separator("INITIAL MARKET");

engine.update_market(
    btc,
    100'000.0,
    100'010.0,
    100'005.0,
    1
);

engine.update_market(
    btc,
    100'010.0,
    100'020.0,
    100'015.0,
    2
);

engine.update_market(
    btc,
    100'000.0,
    100'005.0,
    100'002.0,
    3
);

engine.update_market(
    eth,
    4'500.0,
    4'501.0,
    4'500.5,
    10
);

engine.update_market(
    eth,
    4'510.0,
    4'511.0,
    4'510.5,
    11
);

print_separator("MANUAL ORDER");

const auto order_id =
    engine.place_market_order(
        btc,
        Side::Buy,
        0.01
    );

const auto position =
    engine.account().get_position(btc);

std::cout
    << "Order ID: "
    << order_id
    << "\n";

std::cout
    << "BTC Position: "
    << position.quantity
    << "\n";

std::cout
    << "Average Price: "
    << position.average_price
    << "\n";

std::cout
    << "Balance: "
    << engine.account().balance()
    << "\n";

print_separator("SIMULATOR FEED");

SimulatorFeed feed(engine);

feed.start();

for (int i = 0; i < 10; ++i)
    feed.tick();

feed.stop();

Bot* simple_bot =
    bots.get_bot("SimpleBot");

if (simple_bot)
{
    print_separator("BOT STATUS");

    std::cout
        << "Name: "
        << simple_bot->name()
        << "\n";

    std::cout
        << "Running: "
        << (simple_bot->is_running() ? "YES" : "NO")
        << "\n";

    std::cout
        << "Trades: "
        << simple_bot->state().trades
        << "\n";

    std::cout
        << "Profit: "
        << simple_bot->state().profit
        << "\n";

    std::cout
        << "Last Action: "
        << simple_bot->state().last_action
        << "\n";
}

print_account(engine, btc);

print_separator("FINAL MARKET");

const auto final_btc =
    engine.market().get_ticker(btc);

const auto final_eth =
    engine.market().get_ticker(eth);

std::cout
    << "BTCUSDT: "
    << final_btc.last
    << "\n";

std::cout
    << "ETHUSDT: "
    << final_eth.last
    << "\n";

bots.stop_all();

print_separator("CRYTOPZ CORE TEST COMPLETED");

return 0;


}

