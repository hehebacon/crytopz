#pragma once

#include "http_client.hpp"

namespace crytopz {

class WinHttpClient : public HttpClient
{
public:

    WinHttpClient() = default;

    ~WinHttpClient() override = default;

    HttpResponse get(
        const std::string& url
    ) override;
};

}