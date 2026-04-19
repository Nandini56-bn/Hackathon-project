@echo off
REM SEO Agent Setup Script for Windows

echo.
echo ============================================================
echo  SEO Agent Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo ✅ Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo ✅ .env file created
    echo.
    echo 📝 IMPORTANT: Edit .env and add your Groq API key
    echo Get one at: https://console.groq.com
    echo.
)

REM Create data directories
echo.
echo Creating data directories...
if not exist "data\memory" mkdir data\memory
echo ✅ Data directories created

echo.
echo ============================================================
echo  Setup Complete! 🎉
echo ============================================================
echo.
echo Next steps:
echo.
echo 1. Edit .env file in this directory
echo    Add your Groq API key: GROQ_API_KEY=your_key_here
echo.
echo 2. Start the backend server:
echo    Run: run_backend.bat
echo.
echo 3. Open the frontend:
echo    Open this file in your browser: frontend\index.html
echo    OR Run: python -m http.server 8001 (in frontend folder)
echo.
echo 4. The frontend will connect to: http://localhost:8000
echo.
echo ============================================================
echo.
pause
