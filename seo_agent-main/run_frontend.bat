@echo off
REM Run Frontend Server for SEO Agent

echo.
echo ============================================================
echo  SEO Agent Frontend Server
echo ============================================================
echo.

cd frontend

echo Starting frontend server on port 8001...
echo.
echo 🌐 Frontend will be available at: http://localhost:8001
echo 🛑 Press Ctrl+C to stop the server
echo.
echo Make sure the backend is running first!
echo (Run run_backend.bat in another terminal)
echo.

python -m http.server 8001

pause
