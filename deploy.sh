#!/bin/bash

# Deployment script for Legal Clerk RAG Agent
# Run this to set up and deploy the solution

echo "🏛️  Legal Clerk RAG Agent Deployment"
echo "===================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check environment variables
if [ -f ".env" ]; then
    echo "✅ .env file found"
    
    # Check if API key is set
    if grep -q "OPENAI_API_KEY=sk-" .env; then
        echo "✅ OpenAI API key is configured"
    else
        echo "⚠️  Warning: OpenAI API key may not be properly configured"
        echo "   Please update your .env file with a valid API key"
    fi
else
    echo "❌ .env file not found. Please create it with your OpenAI API key."
    exit 1
fi

# Test the solution
echo "🧪 Running tests..."
python test_agent.py

if [ $? -eq 0 ]; then
    echo "✅ Tests passed!"
else
    echo "⚠️  Some tests may have failed. Check the output above."
fi

# Start the server
echo "🚀 Starting the server..."
echo "   Server will run on http://localhost:8100"
echo "   API documentation: http://localhost:8100/docs"
echo ""
echo "🌐 To expose publicly:"
echo "   1. Keep this server running"
echo "   2. In another terminal: ngrok http 8100"
echo "   3. Submit: https://xyz.ngrok-free.app/solve"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python server.py --port 8100