
#include "crytopz/live_market_scheduler.hpp"

#include <thread>

namespace crytopz {

class LiveMarketScheduler::Impl
{
public:
    std::thread worker;
};

LiveMarketScheduler::LiveMarketScheduler(
    LiveMarketFeed& feed,
    std::chrono::milliseconds interval
)
    : feed_(feed),
      interval_(interval),
      running_(false),
      impl_(new Impl())
{
    if (interval_ <= std::chrono::milliseconds::zero()) {
        interval_ = std::chrono::seconds(5);
    }
}

LiveMarketScheduler::~LiveMarketScheduler()
{
    stop();

    delete impl_;
    impl_ = nullptr;
}

bool LiveMarketScheduler::start()
{
    if (running_) {
        return false;
    }

    if (impl_ == nullptr) {
        impl_ = new Impl();
    }

    if (impl_->worker.joinable()) {
        impl_->worker.join();
    }

    // Start the live market feed first.
    if (!feed_.start()) {
        return false;
    }

    running_ = true;

    try {
        impl_->worker = std::thread(
            &LiveMarketScheduler::run,
            this
        );
    }
    catch (...) {
        running_ = false;
        feed_.stop();
        return false;
    }

    return true;
}

void LiveMarketScheduler::stop()
{
    running_ = false;

    if (impl_ != nullptr && impl_->worker.joinable()) {
        if (impl_->worker.get_id() == std::this_thread::get_id()) {
            impl_->worker.detach();
        }
        else {
            impl_->worker.join();
        }
    }

    feed_.stop();
}

bool LiveMarketScheduler::running() const
{
    return running_;
}

void LiveMarketScheduler::tick()
{
    if (!feed_.running()) {
        return;
    }

    feed_.update();
}

std::size_t LiveMarketScheduler::interval_ms() const
{
    return static_cast<std::size_t>(interval_.count());
}

void LiveMarketScheduler::run()
{
    while (running_) {
        tick();

        if (!running_) {
            break;
        }

        std::this_thread::sleep_for(interval_);
    }
}

} // namespace crytopz

