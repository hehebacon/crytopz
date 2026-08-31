#include "crytopz/winhttp_client.hpp"

#ifdef _WIN32

#include <windows.h>
#include <winhttp.h>

#include <string>

#pragma comment(lib, "winhttp.lib")

namespace crytopz {

HttpResponse WinHttpClient::get(
    const std::string& url
)
{
    HttpResponse response;

    // --------------------------------------------------------
    // Parse URL
    // --------------------------------------------------------

    std::wstring wide_url(
        url.begin(),
        url.end()
    );

    URL_COMPONENTS components{};
    components.dwStructSize =
        sizeof(components);

    wchar_t host[256]{};
    wchar_t path[2048]{};

    components.lpszHostName = host;
    components.dwHostNameLength =
        sizeof(host) / sizeof(wchar_t);

    components.lpszUrlPath = path;
    components.dwUrlPathLength =
        sizeof(path) / sizeof(wchar_t);

    if (!WinHttpCrackUrl(
        wide_url.c_str(),
        0,
        0,
        &components
    ))
    {
        response.error =
            "WinHttpCrackUrl failed";

        return response;
    }

    // --------------------------------------------------------
    // Open session
    // --------------------------------------------------------

    HINTERNET session =
        WinHttpOpen(
            L"crytopz/0.1",
            WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
            WINHTTP_NO_PROXY_NAME,
            WINHTTP_NO_PROXY_BYPASS,
            0
        );

    if (!session)
    {
        response.error =
            "WinHttpOpen failed";

        return response;
    }

    // --------------------------------------------------------
    // Connect
    // --------------------------------------------------------

    HINTERNET connection =
        WinHttpConnect(
            session,
            host,
            components.nPort,
            0
        );

    if (!connection)
    {
        response.error =
            "WinHttpConnect failed";

        WinHttpCloseHandle(session);

        return response;
    }

    // --------------------------------------------------------
    // Request flags
    // --------------------------------------------------------

    DWORD flags = 0;

    if (components.nScheme == INTERNET_SCHEME_HTTPS)
    {
        flags |=
            WINHTTP_FLAG_SECURE;
    }

    // --------------------------------------------------------
    // Open GET request
    // --------------------------------------------------------

    HINTERNET request =
        WinHttpOpenRequest(
            connection,
            L"GET",
            path,
            nullptr,
            WINHTTP_NO_REFERER,
            WINHTTP_DEFAULT_ACCEPT_TYPES,
            flags
        );

    if (!request)
    {
        response.error =
            "WinHttpOpenRequest failed";

        WinHttpCloseHandle(connection);
        WinHttpCloseHandle(session);

        return response;
    }

    // --------------------------------------------------------
    // Send request
    // --------------------------------------------------------

    BOOL sent =
        WinHttpSendRequest(
            request,
            WINHTTP_NO_ADDITIONAL_HEADERS,
            0,
            WINHTTP_NO_REQUEST_DATA,
            0,
            0,
            0
        );

    if (!sent)
    {
        response.error =
            "WinHttpSendRequest failed";

        WinHttpCloseHandle(request);
        WinHttpCloseHandle(connection);
        WinHttpCloseHandle(session);

        return response;
    }

    // --------------------------------------------------------
    // Receive response
    // --------------------------------------------------------

    if (!WinHttpReceiveResponse(
        request,
        nullptr
    ))
    {
        response.error =
            "WinHttpReceiveResponse failed";

        WinHttpCloseHandle(request);
        WinHttpCloseHandle(connection);
        WinHttpCloseHandle(session);

        return response;
    }

    // --------------------------------------------------------
    // HTTP status code
    // --------------------------------------------------------

    DWORD status_code = 0;
    DWORD status_size =
        sizeof(status_code);

    WinHttpQueryHeaders(
        request,
        WINHTTP_QUERY_STATUS_CODE |
        WINHTTP_QUERY_FLAG_NUMBER,
        WINHTTP_HEADER_NAME_BY_INDEX,
        &status_code,
        &status_size,
        WINHTTP_NO_HEADER_INDEX
    );

    response.status_code =
        static_cast<int>(status_code);

    // --------------------------------------------------------
    // Read body
    // --------------------------------------------------------

    while (true)
    {
        DWORD available = 0;

        if (!WinHttpQueryDataAvailable(
            request,
            &available
        ))
        {
            response.error =
                "WinHttpQueryDataAvailable failed";

            break;
        }

        if (available == 0)
        {
            break;
        }

        std::string buffer(
            available,
            '\0'
        );

        DWORD downloaded = 0;

        if (!WinHttpReadData(
            request,
            buffer.data(),
            available,
            &downloaded
        ))
        {
            response.error =
                "WinHttpReadData failed";

            break;
        }

        buffer.resize(
            downloaded
        );

        response.body +=
            buffer;
    }

    // --------------------------------------------------------
    // Success
    // --------------------------------------------------------

    if (response.status_code >= 200 &&
        response.status_code < 300 &&
        response.error.empty())
    {
        response.success = true;
    }

    // --------------------------------------------------------
    // Cleanup
    // --------------------------------------------------------

    WinHttpCloseHandle(request);
    WinHttpCloseHandle(connection);
    WinHttpCloseHandle(session);

    return response;
}

} // namespace crytopz

#endif
