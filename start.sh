#!/bin/bash

# Add the ngrok authtoken
 ngrok authtoken 2hQxB1ZLybpRWy9xcLaHVnXZtw0_5r1v1e2FWMZsXmCWPYSdL

# Start ngrok in the background
ngrok http 8000 > /dev/null &

#ngrok http http://localhost:8000

# Give ngrok some time to start and retrieve the URL
 sleep 5

# Print the ngrok public URL
# curl --silent --max-time 10 --connect-timeout 5 --retry 2 http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url'

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000

