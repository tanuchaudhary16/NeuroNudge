#!/bin/bash

# NeuroNudge Startup Script
# This script starts both the Python backend and React frontend

echo "🧠 Starting NeuroNudge - Emotion-Aware Productivity Assistant"
echo "=================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.7+ and try again."
    exit 1
fi

# Check if Node.js is available  
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm is required but not installed."
    echo "Please install Node.js 18+ and try again."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo "🚀 Starting services..."

# Start Python backend in background
echo "🐍 Starting Python Flask backend..."
python3 run.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start React frontend
echo "⚛️  Starting React frontend..."
npm run dev &
FRONTEND_PID=$!

# Function to cleanup processes on exit
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup INT TERM

echo "✅ NeuroNudge is running!"
echo "🌐 Frontend: http://localhost:5173"  
echo "🔌 Backend API: http://localhost:5000"
echo "Press Ctrl+C to stop all services"

# Wait for processes
wait