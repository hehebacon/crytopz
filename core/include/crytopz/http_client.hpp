#pragma once

#include <string>

namespace crytopz {

struct HttpResponse
{
    bool success = false;

    int status_code = 0;

    std::string body;

    std::string error;
};


class HttpClient
{
public:

    virtual ~HttpClient() = default;

    virtual HttpResponse get(
        const std::string& url
    ) = 0;
};

}