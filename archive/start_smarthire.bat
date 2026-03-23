@echo off
echo ============================================
echo Starting SmartHire.AI Platform
echo ============================================

echo.
echo [1/2] Starting Backend API Server...
start "SmartHire API" cmd /k "python api_server.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting Streamlit Dashboard...
start "SmartHire Dashboard" cmd /k "streamlit run app.py"
timeout /t 3 /nobreak >nul

echo.
echo ============================================
echo SmartHire.AI is running!
echo ============================================
echo.
echo Backend API: http://localhost:5000
echo Dashboard:   http://localhost:8501
echo Login Page:  auth/landing.html
echo.
echo Press any key to open login page...
pause >nul
start auth\landing.html
