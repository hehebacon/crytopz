#pragma once

#include "bot.hpp"

namespace crytopz::bot {

class SimpleBot final : public Bot {
public:
    SimpleBot();

    const std::string& id() const override;
    const std::string& name() const override;

    bool start() override;
    void stop() override;

    bool running() const override;

    void onMarketUpdate(
        const std::string& symbol,
        double price
    ) override;

private:
    std::string id_;
    std::string name_;
    bool running_ = false;
};

}