@echo off
REM Run Backend + Frontend for SEO Agent - Windows Only

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  SEO AGENT - STARTING BACKEND + FRONTEND
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ ERROR: Virtual environment not found!
    echo Please run: setup.bat
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo ❌ ERROR: .env file not found!
    echo Please run: setup.bat
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo 📍 Starting Backend Server...
echo    🔗 Backend: http://127.0.0.1:8000
echo    📚 API Docs: http://127.0.0.1:8000/docs
echo.

REM Start Backend in new window
start "SEO Agent Backend" cmd /k "python backend/main.py"

REM Wait for backend to start
echo    ⏳ Waiting for backend to start...
timeout /t 3 /nobreak

echo.
echo 🌐 Starting Frontend Server...
echo    🔗 Frontend: http://localhost:8080
echo.

REM Start Frontend in new window
start "SEO Agent Frontend" cmd /k "python -m http.server 8080 --directory frontend"

echo.
echo ============================================================
echo ✅ BOTH SERVERS ARE RUNNING!
echo ============================================================
echo.
echo 📌 OPEN IN BROWSER: http://localhost:8080
echo.
echo To stop: Close the terminal windows or press Ctrl+C
echo.
echo ============================================================
echo.

pause
