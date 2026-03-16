@echo off
echo ===========================================
echo Spam Email Detector - Starting Server
echo ===========================================

REM Navigate to project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install --upgrade pip
    pip install Flask scikit-learn pandas numpy joblib
)

REM Check if model files exist
if not exist "spam_model.pkl" (
    echo.
    echo ===========================================
    echo Creating model files...
    echo ===========================================
    python quick_setup.py
    echo Model files created!
)

REM Check if model files exist
if not exist "spam_model.pkl" (
    echo.
    echo ERROR: Failed to create model files!
    echo Please run: python quick_setup.py
    echo.
    pause
    exit /b 1
)

REM Run the application
echo.
echo ===========================================
echo Starting Flask server...
echo ===========================================
echo Open browser: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause