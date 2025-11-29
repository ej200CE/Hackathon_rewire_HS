#!/bin/bash

# --- Configuration ---
set -e

# --- Helper Functions ---
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    # Kill background jobs started by this script
    kill $(jobs -p) 2>/dev/null
    echo "✅ Cleanup complete."
}

# Trap Ctrl+C (SIGINT) and Exit
trap cleanup SIGINT EXIT

echo "🚀 Starting Local Development Environment (Ubuntu)..."

# 1. RabbitMQ Setup
echo "------------------------------------------------"
echo "🐰 Configuring RabbitMQ..."

if ! command -v rabbitmq-server &> /dev/null; then
    echo "📦 Installing RabbitMQ Server..."
    sudo apt-get install -y rabbitmq-server
fi

# Ensure service is running
if ! systemctl is-active --quiet rabbitmq-server; then
    echo "   Starting RabbitMQ Service..."
    sudo systemctl start rabbitmq-server
    # Enable on boot (optional)
    sudo systemctl enable rabbitmq-server
fi

# Enable Management Plugin
echo "   Enabling Management Plugin..."
sudo rabbitmq-plugins enable rabbitmq_management || true
echo "   RabbitMQ WebUI available at http://localhost:15672"

# 2. Backend (Dotnet) Setup
echo "------------------------------------------------"
echo "🔷 Configuring Backend (Dotnet)..."

if ! command -v dotnet &> /dev/null; then
    echo "📦 Installing .NET SDK..."
    sudo apt-get install -y wget apt-transport-https
    
    if [ ! -f /etc/apt/sources.list.d/dotnet.list ]; then
        wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
        sudo dpkg -i packages-microsoft-prod.deb
        rm packages-microsoft-prod.deb
        sudo apt-get update
    fi
    
    sudo apt-get install -y dotnet-sdk-8.0
fi

echo "   Starting WebAPI in background..."
cd ./backend/FoodVenikWebApi
dotnet run &
cd ../..

# 3. Agent (Python/UV) Setup
echo "------------------------------------------------"
echo "🐍 Configuring Agent (Python/UV)..."

if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv (Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
fi

cd ./backend/sample-agent

# Env File Check
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating one..."
    touch .env
fi

if ! grep -q "OPENAI_API_KEY" .env; then
    echo "⚠️  WARNING: OPENAI_API_KEY is missing in ./backend/sample-agent/.env"
    echo "   Please add it manually."
fi

echo "   Starting Agent in background..."
uv run main.py & 
cd ../..

# 4. Frontend Setup
echo "------------------------------------------------"
echo "⚛️  Configuring Frontend..."

# Check for Node/NPM
if ! command -v npm &> /dev/null; then
    echo "📦 Installing Node.js and NPM..."
    sudo apt-get install -y nodejs npm
fi

cd ./frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Frontend dependencies..."
    npm install
fi

echo "   Starting Frontend..."
echo "   PRESS CTRL+C TO STOP ALL SERVICES"
echo "------------------------------------------------"

npm start