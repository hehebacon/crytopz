
cmake_minimum_required(VERSION 3.20)

project(crytopz
    VERSION 0.1.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


# ============================================================
# THIRD PARTY
# ============================================================

set(NLOHMANN_JSON_INCLUDE
    "${CMAKE_CURRENT_SOURCE_DIR}/third_party/nlohmann_json/include"
)


# ============================================================
# CRYTOPZ CORE
# ============================================================

add_library(crytopz_core

    core/src/market.cpp
    core/src/account.cpp
    core/src/simulator_feed.cpp
    core/src/engine.cpp
    core/src/order_manager.cpp
    core/src/event_bus.cpp
    core/src/simple_bot.cpp
    core/src/strategy_manager.cpp
    core/src/execution.cpp
    core/src/bot.cpp
    core/src/bot_manager.cpp
    core/src/bot_snapshot.cpp
    core/src/core_bridge.cpp
    core/src/bot_api.cpp
    core/src/bot_context.cpp
    core/src/risk_manager.cpp
    core/src/bot_executor.cpp
    core/src/pnl.cpp
    core/src/live_market_scheduler.cpp

    core/src/crypto_market_provider.cpp
    core/src/winhttp_client.cpp
    core/src/live_market_feed.cpp

    core/src/asset_registry.cpp
    core/src/default_assets.cpp

    core/src/core_api.cpp

    core/src/trading_account.cpp
    core/src/execution_router.cpp

    account/src/account.cpp
    account/src/account_manager.cpp
    account/src/account_storage.cpp
    account/src/session_manager.cpp
    account/src/credential.cpp
    account/src/session_token.cpp
)


target_include_directories(crytopz_core
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
        "${CMAKE_CURRENT_SOURCE_DIR}/account/include"
        "${NLOHMANN_JSON_INCLUDE}"
)


if(WIN32)
    target_link_libraries(crytopz_core
        PUBLIC
            winhttp
    )
endif()


# ============================================================
# BOT PLUGIN SYSTEM
# ============================================================

add_library(crytopz_bot

    bot/src/bot.cpp
    bot/src/simple_bot.cpp
    bot/src/bot_manager.cpp
    bot/src/bot_storage.cpp
    bot/src/bot_registry.cpp
    bot/src/bot_loader.cpp
    bot/src/bot_factory.cpp
    bot/src/bot_manifest.cpp
    bot/src/bot_validator.cpp
    bot/src/bot_runtime.cpp
    bot/src/bot_controller.cpp
    bot/src/bot_system.cpp
)


target_include_directories(crytopz_bot
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/bot/include"
)


target_link_libraries(crytopz_bot
    PUBLIC
        crytopz_core
)


# ============================================================
# SIMULATOR
# ============================================================

add_executable(crytopz_simulator
    simulator/main.cpp
)


target_link_libraries(crytopz_simulator
    PRIVATE
        crytopz_core
        crytopz_bot
)


# ============================================================
# BRIDGE DLL
# ============================================================

add_library(crytopz_bridge SHARED
    core/src/bridge.cpp
)


target_include_directories(crytopz_bridge
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
        "${CMAKE_CURRENT_SOURCE_DIR}/account/include"
        "${NLOHMANN_JSON_INCLUDE}"
)


target_link_libraries(crytopz_bridge
    PRIVATE
        crytopz_core
)


if(WIN32)
    target_compile_definitions(crytopz_bridge
        PRIVATE
            CRYTOPZ_BRIDGE_EXPORTS
    )
endif()


# ============================================================
# BRIDGE TEST
# ============================================================

add_executable(crytopz_bridge_test
    bridge/main.cpp
)


target_include_directories(crytopz_bridge_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
        "${CMAKE_CURRENT_SOURCE_DIR}/bridge/include"
        "${NLOHMANN_JSON_INCLUDE}"
)


target_link_libraries(crytopz_bridge_test
    PRIVATE
        crytopz_core
)


# ============================================================
# CORE TEST
# ============================================================

add_executable(crytopz_core_test
    core/test/test_core.cpp
)


target_include_directories(crytopz_core_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
        "${NLOHMANN_JSON_INCLUDE}"
)


target_link_libraries(crytopz_core_test
    PRIVATE
        crytopz_core
)


# ============================================================
# CORE API TEST
# ============================================================

add_executable(crytopz_core_api_test
    core/test/test_core_api.cpp
)


target_include_directories(crytopz_core_api_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
        "${NLOHMANN_JSON_INCLUDE}"
)


target_link_libraries(crytopz_core_api_test
    PRIVATE
        crytopz_core
)


# ============================================================
# CORE API REGRESSION TEST
# ============================================================

add_executable(crytopz_core_api_regression_test
    core/test/test_core_api_regression.cpp
)


target_include_directories(crytopz_core_api_regression_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
        "${NLOHMANN_JSON_INCLUDE}"
)


target_link_libraries(crytopz_core_api_regression_test
    PRIVATE
        crytopz_core
)


# ============================================================
# MARKET DATA TEST
# ============================================================

add_executable(crytopz_market_data_test
    core/test/test_market_data.cpp
)


target_include_directories(crytopz_market_data_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
)


target_link_libraries(crytopz_market_data_test
    PRIVATE
        crytopz_core
)


# ============================================================
# CRYPTO PROVIDER TEST
# ============================================================

add_executable(crytopz_crypto_provider_test
    core/test/test_crypto_market_provider.cpp
)


target_include_directories(crytopz_crypto_provider_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
)


target_link_libraries(crytopz_crypto_provider_test
    PRIVATE
        crytopz_core
)


# ============================================================
# ASSET REGISTRY TEST
# ============================================================

add_executable(crytopz_asset_registry_test
    core/test/test_asset_registry.cpp
)


target_include_directories(crytopz_asset_registry_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
)


target_link_libraries(crytopz_asset_registry_test
    PRIVATE
        crytopz_core
)


# ============================================================
# JSON TEST
# ============================================================

add_executable(crytopz_json_test
    core/test/test_json.cpp
)


target_include_directories(crytopz_json_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
        "${NLOHMANN_JSON_INCLUDE}"
)


target_link_libraries(crytopz_json_test
    PRIVATE
        crytopz_core
)


# ============================================================
# LIVE CRYPTO TEST
# ============================================================

add_executable(crytopz_live_crypto_test
    core/test/test_live_crypto.cpp
)


target_include_directories(crytopz_live_crypto_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
)


target_link_libraries(crytopz_live_crypto_test
    PRIVATE
        crytopz_core
)


# ============================================================
# LIVE MARKET FEED TEST
# ============================================================

add_executable(crytopz_live_market_feed_test
    core/test/test_live_market_feed.cpp
)


target_include_directories(crytopz_live_market_feed_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
)


target_link_libraries(crytopz_live_market_feed_test
    PRIVATE
        crytopz_core
)


# ============================================================
# LIVE MARKET SCHEDULER TEST
# ============================================================

add_executable(crytopz_live_market_scheduler_test
    core/test/test_live_market_scheduler.cpp
)


target_include_directories(crytopz_live_market_scheduler_test
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/core/include"
)


target_link_libraries(crytopz_live_market_scheduler_test
    PRIVATE
        crytopz_core
)


# ============================================================
# OUTPUT DIRECTORIES
# ============================================================

set(CRYTOPZ_BIN_DIR
    "${CMAKE_BINARY_DIR}/bin"
)


set(CRYTOPZ_RUNTIME_TARGETS

    crytopz_simulator
    crytopz_bridge
    crytopz_bridge_test

    crytopz_core_test
    crytopz_core_api_test
    crytopz_core_api_regression_test

    crytopz_market_data_test
    crytopz_crypto_provider_test
    crytopz_asset_registry_test
    crytopz_json_test

    crytopz_live_crypto_test
    crytopz_live_market_feed_test
    crytopz_live_market_scheduler_test
)


set_target_properties(
    ${CRYTOPZ_RUNTIME_TARGETS}

    PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY
        "${CRYTOPZ_BIN_DIR}"
)


set_target_properties(
    crytopz_bridge

    PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY
        "${CRYTOPZ_BIN_DIR}"
)


# ============================================================
# BUILD INFORMATION
# ============================================================

message(STATUS "Crytopz configuration")
message(STATUS "C++ standard: C++20")
message(STATUS "Core source: core/src")
message(STATUS "Bridge source: core/src/bridge.cpp")
message(STATUS "Bridge header: core/include/crytopz/bridge.hpp")
message(STATUS "Binary directory: ${CRYTOPZ_BIN_DIR}")


