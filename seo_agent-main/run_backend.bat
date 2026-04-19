@echo off
REM Run Backend Server for SEO Agent

echo.
echo ============================================================
echo  SEO Agent Backend Server
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run: setup.bat
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please run: setup.bat
    pause
    exit /b 1
)

echo ✅ Virtual environment activated
echo ✅ Configuration loaded
echo.

REM Navigate to backend directory
cd backend

echo Starting SEO Agent API Server...
echo.
echo 📍 API will be available at: http://127.0.0.1:8000
echo 📖 API Documentation: http://127.0.0.1:8000/docs
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Run the backend
python main.py

pause
