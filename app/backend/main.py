"""
Legacy main.py - Use app.py instead for the new application factory pattern
This file is kept for backward compatibility and manual running
"""

# Import the app instance directly from app.py
from app import app

if __name__ == '__main__':
    app.run(debug=True)
