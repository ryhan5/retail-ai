@echo off
echo 🚀 Starting Retail AI Sales Assistant with React Frontend...
echo.

echo 📦 Installing React dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo 🔨 Building React app...
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Failed to build React app
    pause
    exit /b 1
)

cd ..

echo 🐍 Starting Flask backend...
python app.py

pause
