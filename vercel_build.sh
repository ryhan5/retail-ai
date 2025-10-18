#!/bin/bash

# Install frontend dependencies and build
cd frontend
npm install
npm run build
cd ..

# Install Python dependencies
pip install -r requirements.txt

# Create vercel_build directory
mkdir -p vercel_build/api

# Move frontend build files
cp -r frontend/build/* vercel_build/

# Create API endpoints
for endpoint in $(grep -r "@app.route" --include="*.py" . | grep -v "venv" | grep -oP "(?<=')[^']+(?=')" | grep "^/api/"); do
  mkdir -p "vercel_build$endpoint"
  echo 'from app import app' > "vercel_build$endpoint/index.py"
  echo 'from http.server import BaseHTTPRequestHandler' >> "vercel_build$endpoint/index.py"
  echo 'import json' >> "vercel_build$endpoint/index.py"
  echo 'from io import BytesIO' >> "vercel_build$endpoint/index.py"
  echo 'import sys' >> "vercel_build$endpoint/index.py"
  echo 'import os' >> "vercel_build$endpoint/index.py"
  echo 'sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))' >> "vercel_build$endpoint/index.py"
  echo 'def handler(event, context):' >> "vercel_build$endpoint/index.py"
  echo '    return app(event, context)' >> "vercel_build$endpoint/index.py"
done
