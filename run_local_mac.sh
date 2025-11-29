#!/bin/bash

# --- Configuration ---
# Exit script on error (except where we handle it)
set -e

# --- Helper Functions ---
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo "📦 Installing $1..."
        brew install $1
    else
        echo "✅ $1 is already installed."
    fi
}

cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    # Kill the background jobs (Dotnet & Python)
    kill $(jobs -p) 2>/dev/null
    echo "✅ Cleanup complete. RabbitMQ service remains running (manage via 'brew services')."
}

# Trap Ctrl+C (SIGINT) and Exit to run cleanup
trap cleanup SIGINT EXIT

echo "🚀 Starting Local Development Environment (macOS)..."

# 1. RabbitMQ Setup
echo "------------------------------------------------"
echo "🐰 Configuring RabbitMQ..."
check_dependency "rabbitmq"

# Check if RabbitMQ service is running, if not, start it
if ! brew services list | grep -q "rabbitmq.*started"; then
    echo "   Starting RabbitMQ Service..."
    brew services start rabbitmq
    # Give it a moment to wake up
    sleep 5
else
    echo "   RabbitMQ is already running."
fi

# Enable Management Plugin (Web UI)
# Note: On Apple Silicon paths may vary, try to locate rabbitmq-plugins
if command -v rabbitmq-plugins &> /dev/null; then
    rabbitmq-plugins enable rabbitmq_management || echo "   (Plugin might already be active)"
else
    # Fallback for Homebrew path if not in global PATH
    BREW_PREFIX=$(brew --prefix)
    "$BREW_PREFIX/sbin/rabbitmq-plugins" enable rabbitmq_management || true
fi
echo "   RabbitMQ WebUI should be available at http://localhost:15672"

# 2. Backend (Dotnet) Setup
echo "------------------------------------------------"
echo "🔷 Configuring Backend (Dotnet)..."
if ! command -v dotnet &> /dev/null; then
    echo "📦 Installing .NET SDK..."
    brew install --cask dotnet-sdk
fi

echo "   Starting WebAPI in background..."
cd ./backend/FoodVenikWebApi
# Run in background (&) and save output to a log file to keep console clean, or let it print
dotnet run &
DOTNET_PID=$!
cd ../.. # Return to root

# 3. Agent (Python/UV) Setup
echo "------------------------------------------------"
echo "🐍 Configuring Agent (Python/UV)..."
check_dependency "uv"

cd ./backend/sample-agent

# Env File Check
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating one..."
    touch .env
    echo "# Add your keys here" >> .env
fi

# Check for API Key
if ! grep -q "OPENAI_API_KEY" .env; then
    echo "⚠️  WARNING: OPEN_API_KEY is missing in ./backend/sample-agent/.env"
    echo "   Please add it manually for the agent to function correctly."
fi

echo "   Starting Agent in background..."
# uv automatically manages python versions and venvs
uv run main.py & 
AGENT_PID=$!
cd ../..

# 4. Frontend Setup
echo "------------------------------------------------"
echo "⚛️  Configuring Frontend..."

cd ./frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Frontend dependencies (npm install)..."
    npm install
fi

echo "   Starting Frontend (this will take over the console)..."
echo "   PRESS CTRL+C TO STOP ALL SERVICES"
echo "------------------------------------------------"

# Run npm start in foreground. When this stops (Ctrl+C), the 'trap' function triggers.
npm start