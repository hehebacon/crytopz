@echo off
setlocal
title CRYTOPZ ^| Market Data Upgrade

cd /d "%~dp0"

echo.
echo  ============================================================
echo       CRYTOPZ - MARKET DATA UPGRADE
echo  ============================================================
echo.
echo  [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo  [ERROR] Python was not found.
    pause
    exit /b 1
)

echo.
echo  [2/3] Applying Trade + Markets upgrade...
python apply_market_upgrade.py
if errorlevel 1 (
    echo.
    echo  [ERROR] Upgrade failed.
    echo  Your *.market_backup files are kept.
    pause
    exit /b 1
)

echo.
echo  [3/3] COMPLETE
echo.
echo  Trade asset universe: UPDATED
echo  Markets asset universe: UPDATED
echo  External read-only prices: ENABLED
echo  Paper execution: UNCHANGED
echo.
echo  ============================================================
echo       CRYTOPZ MARKET UPGRADE COMPLETE
echo  ============================================================
echo.
pause
