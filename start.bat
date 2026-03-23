@echo off
echo ========================================
echo  SmartHire.AI - Starting Local Server
echo ========================================
echo.

REM Single server - Flask serves everything
start "SmartHire" cmd /k "venv\Scripts\python.exe backend\api_server.py"

timeout /t 2 /nobreak >nul
start http://localhost:5000

echo.
echo  Open: http://localhost:5000
echo ========================================
pause >nul
