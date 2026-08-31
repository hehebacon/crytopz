@echo off
setlocal

title CRYTOPZ ^| Git Update
cd /d "%~dp0"

echo.
echo  ============================================================
echo       CRYTOPZ - GIT UPDATE
echo  ============================================================
echo.
echo  [1/5] Checking repository...
git status --short

echo.
echo  [2/5] Adding all changes...
git add .

if errorlevel 1 (
    echo.
    echo  [ERROR] git add failed.
    pause
    exit /b 1
)

echo.
echo  [3/5] Creating commit...
set "COMMIT_MSG=Crytopz update %date% %time%"
git commit -m "%COMMIT_MSG%"

if errorlevel 1 (
    echo.
    echo  [INFO] Nothing new to commit, or commit failed.
)

echo.
echo  [4/5] Pushing to GitHub...
git push

if errorlevel 1 (
    echo.
    echo  [ERROR] Push failed.
    echo.
    echo  Check your GitHub login / remote:
    echo  git remote -v
    pause
    exit /b 1
)

echo.
echo  [5/5] DONE!
echo.
echo  ============================================================
echo       CRYTOPZ UPDATED SUCCESSFULLY
echo       GitHub is now up to date.
echo  ============================================================
echo.

git status

echo.
echo  Press any key to close...
pause >nul

endlocal