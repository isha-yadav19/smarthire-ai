@echo off
echo ============================================================
echo SmartHire.AI - Complete System Startup
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/Update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt
echo Dependencies ready!
echo.

REM Create necessary directories
if not exist "uploads\" mkdir uploads
if not exist "output\" mkdir output
echo Directories ready!
echo.

echo ============================================================
echo Starting Backend API Server...
echo ============================================================
start cmd /k "title SmartHire API Server && venv\Scripts\activate && python simple_api.py"

REM Wait for API to start
timeout /t 3 /nobreak >nul

echo.
echo ============================================================
echo Starting Streamlit Web Interface...
echo ============================================================
start cmd /k "title SmartHire Web App && venv\Scripts\activate && streamlit run app.py"

REM Wait for Streamlit to start
timeout /t 5 /nobreak >nul

echo.
echo ============================================================
echo System Started Successfully!
echo ============================================================
echo.
echo Backend API:     http://localhost:5000
echo Web Interface:   http://localhost:8501
echo.
echo Opening web browser...
timeout /t 3 /nobreak >nul
start http://localhost:8501

echo.
echo Press any key to stop all services...
pause >nul

REM Kill processes
taskkill /FI "WindowTitle eq SmartHire*" /F >nul 2>&1
echo.
echo All services stopped.
echo.
pause
