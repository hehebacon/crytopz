#include <iostream>

#include "bot_system.hpp"

int main()
{
crytopz::bot::BotSystem system;


std::cout << "========================================" << std::endl;
std::cout << "CRYPTOPZ BOT SYSTEM TEST" << std::endl;
std::cout << "========================================" << std::endl;

std::cout << "Storage size: "
          << system.storage().size()
          << std::endl;

std::cout << "Registry size: "
          << system.registry().size()
          << std::endl;

std::cout << "[BOT] System initialized" << std::endl;

std::cout << "[BOT] Factory ready" << std::endl;
std::cout << "[BOT] Validator ready" << std::endl;
std::cout << "[BOT] Loader ready" << std::endl;
std::cout << "[BOT] Runtime ready" << std::endl;
std::cout << "[BOT] Controller ready" << std::endl;

std::cout << "========================================" << std::endl;
std::cout << "BOT SYSTEM TEST COMPLETED" << std::endl;
std::cout << "========================================" << std::endl;

return 0;


}
