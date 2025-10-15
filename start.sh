#!/bin/bash

# Start both backend and frontend servers

echo "Starting Receipt Itemizer..."

# Start Flask backend in background
echo "Starting Flask backend on port 5000..."
cd "$(dirname "$0")"
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start React frontend
echo "Starting React frontend on port 3000..."
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Servers started!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
