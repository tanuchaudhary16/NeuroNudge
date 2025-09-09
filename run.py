#!/usr/bin/env python3
"""
NeuroNudge Python Backend Runner
Simple script to start the Flask application
"""

from app import app, init_db

if __name__ == '__main__':
    print("Initializing NeuroNudge database...")
    init_db()
    print("Starting NeuroNudge Python backend server...")
    print("Server will be available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)