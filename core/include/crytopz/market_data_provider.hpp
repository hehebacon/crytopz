#pragma once

#include "market.hpp"

#include <cstdint>
#include <functional>
#include <string>

namespace crytopz {

class MarketDataProvider
{
public:

    using UpdateCallback =
        std::function<void(
            const Symbol& symbol,
            Price bid,
            Price ask,
            Price last,
            std::uint64_t timestamp
        )>;

    virtual ~MarketDataProvider() = default;

    // ========================================================
    // LIFECYCLE
    // ========================================================

    virtual bool start() = 0;

    virtual void stop() = 0;

    virtual bool running() const = 0;

    // ========================================================
    // PROVIDER
    // ========================================================

    virtual const char* name() const = 0;

    // ========================================================
    // CALLBACK
    // ========================================================

    void set_update_callback(
        UpdateCallback callback
    )
    {
        callback_ =
            std::move(callback);
    }

protected:

    void publish(
        const Symbol& symbol,
        Price bid,
        Price ask,
        Price last,
        std::uint64_t timestamp
    )
    {
        if (!callback_)
            return;

        callback_(
            symbol,
            bid,
            ask,
            last,
            timestamp
        );
    }

private:

    UpdateCallback callback_;
};

} // namespace crytopz