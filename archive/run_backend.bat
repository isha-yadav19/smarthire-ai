@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting SmartHire.AI Backend Server
echo ============================================================
echo.
python api_server.py
pause
