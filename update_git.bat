@echo off
setlocal EnableDelayedExpansion
title CRYTOPZ ^| Git Update Terminal

:: ============================================================
:: CRYTOPZ GIT UPDATE TERMINAL
:: Windows / CMD
:: ============================================================

:: Move to the folder containing this .bat
cd /d "%~dp0"

:: ---------- COLORS ----------
set "RESET="
set "GREEN=[92m"
set "CYAN=[96m"
set "BLUE=[94m"
set "YELLOW=[93m"
set "RED=[91m"
set "WHITE=[97m"
set "GRAY=[90m"

:: Enable ANSI colors on modern Windows
for /f "tokens=2 delims==" %%A in ('"prompt $E & for %%B in (1) do rem"') do set "ESC=%%A"
if not defined ESC set "ESC="

set "GREEN=%ESC%[92m"
set "CYAN=%ESC%[96m"
set "BLUE=%ESC%[94m"
set "YELLOW=%ESC%[93m"
set "RED=%ESC%[91m"
set "WHITE=%ESC%[97m"
set "GRAY=%ESC%[90m"
set "RESET=%ESC%[0m"

cls

echo.
echo %CYAN%   ██████╗██████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ ███████╗%RESET%
echo %CYAN%  ██╔════╝██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔═══██╗██╔══██╗╚══███╔╝%RESET%
echo %CYAN%  ██║     ██████╔╝ ╚████╔╝    ██║   ██║   ██║██████╔╝  ███╔╝ %RESET%
echo %CYAN%  ██║     ██╔══██╗  ╚██╔╝     ██║   ██║   ██║██╔═══╝  ███╔╝  %RESET%
echo %CYAN%  ╚██████╗██║  ██║   ██║      ██║   ╚██████╔╝██║     ███████╗%RESET%
echo %CYAN%   ╚═════╝╚═╝  ╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═╝     ╚══════╝%RESET%
echo.
echo %GRAY%  ============================================================%RESET%
echo %WHITE%                 GIT UPDATE TERMINAL%RESET%
echo %GRAY%  ============================================================%RESET%
echo.

:: ============================================================
:: STEP 1 - CHECK GIT
:: ============================================================

echo %CYAN%[1/5]%RESET% Checking Git installation...

git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo %RED%[ERROR] Git was not found in PATH.%RESET%
    echo %YELLOW%Install Git for Windows, then reopen this terminal.%RESET%
    echo.
    pause
    exit /b 1
)

for /f "delims=" %%G in ('git --version') do echo %GREEN%      %%G%RESET%

echo %GREEN%      [OK]%RESET%
call :progress
echo.

:: ============================================================
:: STEP 2 - CHECK REPOSITORY
:: ============================================================

echo %CYAN%[2/5]%RESET% Checking Crytopz repository...

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo.
    echo %RED%[ERROR] This folder is not a Git repository.%RESET%
    echo %GRAY%Folder: %CD%%RESET%
    echo.
    pause
    exit /b 1
)

for /f "delims=" %%B in ('git branch --show-current') do set "BRANCH=%%B"
if not defined BRANCH set "BRANCH=unknown"

echo %GREEN%      [OK] Branch: %BRANCH%%RESET%
echo %GRAY%      Remote:%RESET%
git remote -v
call :progress
echo.

:: ============================================================
:: STEP 3 - ADD ALL CHANGES
:: ============================================================

echo %CYAN%[3/5]%RESET% Staging all Crytopz changes...
echo.

git status --short

echo.
git add .
if errorlevel 1 (
    echo.
    echo %RED%[ERROR] git add failed.%RESET%
    pause
    exit /b 1
)

echo %GREEN%      [OK] All changes staged.%RESET%
call :progress
echo.

:: ============================================================
:: STEP 4 - COMMIT
:: ============================================================

echo %CYAN%[4/5]%RESET% Creating commit...

set "COMMIT_MSG=Crytopz update %date% %time%"

git diff --cached --quiet
if errorlevel 1 (
    git commit -m "%COMMIT_MSG%"
    if errorlevel 1 (
        echo.
        echo %RED%[ERROR] Commit failed.%RESET%
        pause
        exit /b 1
    )
    echo %GREEN%      [OK] Commit created.%RESET%
) else (
    echo %YELLOW%      [INFO] No new changes to commit.%RESET%
)

call :progress
echo.

:: ============================================================
:: STEP 5 - PUSH
:: ============================================================

echo %CYAN%[5/5]%RESET% Pushing to GitHub...
echo.

git push
if errorlevel 1 (
    echo.
    echo %RED%[ERROR] Push failed.%RESET%
    echo.
    echo %YELLOW%Possible causes:%RESET%
    echo   - GitHub authentication
    echo   - Remote configuration
    echo   - Network connection
    echo.
    echo %GRAY%Remote information:%RESET%
    git remote -v
    echo.
    pause
    exit /b 1
)

call :progress
echo.

:: ============================================================
:: DONE
:: ============================================================

echo %GREEN%  ============================================================%RESET%
echo %GREEN%                 CRYTOPZ UPDATE COMPLETE%RESET%
echo %GREEN%  ============================================================%RESET%
echo.
echo %WHITE%  Branch : %BRANCH%%RESET%
echo %WHITE%  Remote : GitHub%RESET%
echo %WHITE%  Status : PUSHED SUCCESSFULLY%RESET%
echo.
echo %CYAN%  Latest repository status:%RESET%
echo.
git status --short

echo.
echo %GREEN%  [████████████████████████████████████████] 100%%%RESET%
echo.
echo %GRAY%  Crytopz repository is up to date. 🚀%RESET%
echo.
pause
exit /b 0


:: ============================================================
:: PROGRESS BAR
:: ============================================================

:progress
set "bar="
for /l %%P in (1,1,20) do (
    set "bar=!bar!█"
    <nul set /p "=."
    ping -n 1 -w 35 127.0.0.1 >nul
)
echo  %GREEN%[████████████████████] 100%%%RESET%
exit /b 0
