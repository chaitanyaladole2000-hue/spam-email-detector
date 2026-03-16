@echo off
echo ===========================================
echo Spam Email Detector - Starting Server
echo ===========================================

cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo Installing dependencies...
pip install -r requirements.txt

if not exist "spam_model.pkl" (
    echo Creating model files...
    python quick_setup.py
)

echo Starting Flask server...
echo Open browser: http://localhost:5000

python app.py

pause