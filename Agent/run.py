#!/usr/bin/env python3
"""
GPAF - Main runner script
This is a convenience script to run GPAF UI from project root
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    # Import modules with correct paths
    from scripts.run_ui import run
    from python.helpers import runtime, dotenv
    
    runtime.initialize()
    dotenv.load_dotenv()
    run() 