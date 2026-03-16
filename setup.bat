@echo off
echo ===========================================
echo Spam Email Detector - Setup
echo ===========================================

REM Navigate to project directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
echo Python is not installed! Please install Python first.
pause
exit /b
)

REM Create virtual environment if not exists
if not exist "venv" (
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created!
) else (
echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

REM Check if model files exist
if not exist "spam_model.pkl" (
echo.
echo Creating model files using quick_setup.py...
python quick_setup.py
echo Model files created!
) else (
echo Model files already exist!
)

echo.
echo ===========================================
echo Setup Completed Successfully!
echo ===========================================
echo.
echo To run the application:
echo   run.bat
echo.
echo Open browser: http://localhost:5000
echo.

pause
