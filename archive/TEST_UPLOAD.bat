@echo off
echo Starting Fast API...
start cmd /k "python fast_api.py"
timeout /t 3 /nobreak >nul
echo Opening test page...
start test_upload.html
echo.
echo Test the upload with PDF/DOCX files
pause
