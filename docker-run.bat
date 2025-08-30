@echo off
REM GPAF Docker Run Script for Windows

echo 🐳 Starting GPAF Docker Container...

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or running. Please install Docker Desktop.
    pause
    exit /b 1
)

REM Clean up any existing containers
echo 🧹 Cleaning up existing containers...
docker-compose down --remove-orphans 2>nul

REM Build and start the container
echo 🔨 Building and starting Docker container...
docker-compose up --build -d

REM Check if container is running
timeout /t 5 /nobreak >nul
docker-compose ps

echo ✅ GPAF Container is starting!
echo.
echo 📋 Access Information:
echo Web UI: http://localhost:50001
echo Login: admin / gpaf123
echo SSH: ssh -p 55022 root@localhost (password: gpaf123)
echo.
echo 📊 View logs:
echo docker-compose logs -f gpaf
echo.
echo 🛑 Stop container:
echo docker-compose down
echo.
echo Press any key to view logs...
pause >nul
docker-compose logs -f gpaf