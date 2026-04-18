@echo off
echo ========================================
echo Restarting Spy Game Bot
echo ========================================

echo.
echo Stopping existing processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *spy_game_bot*" 2>nul

echo.
echo Starting Flask server...
start "Spy Game Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate && python admin/app.py"

timeout /t 5 /nobreak >nul

echo.
echo Starting Telegram bot...
start "Spy Game Bot" cmd /k "cd /d %~dp0 && venv\Scripts\activate && python bot/main.py"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo Bots started successfully!
echo ========================================
echo.
echo Press any key to run test scenario...
pause >nul

echo.
echo Running test bots...
cd /d %~dp0
call venv\Scripts\activate
python test_bots.py

pause
