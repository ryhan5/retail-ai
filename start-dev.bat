@echo off
echo 🚀 Starting Retail AI Sales Assistant in Development Mode...
echo.

echo 📦 Installing React dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo 🌐 Starting React development server...
echo React app will be available at: http://localhost:3000
echo Flask API will be available at: http://localhost:5000
echo.
start cmd /k "cd .. && python app.py"
call npm start

pause
