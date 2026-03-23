@echo off
echo ============================================================
echo SmartHire.AI - Authentication Pages
echo ============================================================
echo.
echo Select a page to open:
echo.
echo 1. Login Page
echo 2. Sign Up Page
echo 3. Forgot Password Page
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Opening Login Page...
    start "" "%~dp0auth\login.html"
) else if "%choice%"=="2" (
    echo Opening Sign Up Page...
    start "" "%~dp0auth\signup.html"
) else if "%choice%"=="3" (
    echo Opening Forgot Password Page...
    start "" "%~dp0auth\forgot-password.html"
) else if "%choice%"=="4" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice!
    pause
)
