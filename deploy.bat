@echo off

REM Windows deployment script for Legal Clerk RAG Agent

echo 🏛️  Legal Clerk RAG Agent Deployment
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Check environment variables
if exist ".env" (
    echo ✅ .env file found
    
    REM Check if API key is set (basic check)
    findstr /c:"OPENAI_API_KEY=sk-" .env >nul
    if errorlevel 1 (
        echo ⚠️  Warning: OpenAI API key may not be properly configured
        echo    Please update your .env file with a valid API key
    ) else (
        echo ✅ OpenAI API key appears to be configured
    )
) else (
    echo ❌ .env file not found. Please create it with your OpenAI API key.
    pause
    exit /b 1
)

REM Test the solution
echo 🧪 Running tests...
python test_agent.py

echo ✅ Setup complete!

REM Start the server
echo.
echo 🚀 Starting the server...
echo    Server will run on http://localhost:8100
echo    API documentation: http://localhost:8100/docs
echo.
echo 🌐 To expose publicly:
echo    1. Keep this server running
echo    2. In another terminal: ngrok http 8100
echo    3. Submit: https://xyz.ngrok-free.app/solve
echo.
echo Press Ctrl+C to stop the server
echo.

python server.py --port 8100