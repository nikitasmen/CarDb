#!/usr/bin/env python3
"""
CarDb Mobile App Entry Point
Optimized for mobile deployment with Flet
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from interfaces import run_flet_app

# This is the entry point for the Flet mobile app
if __name__ == "__main__":
    print("Starting CarDb Mobile App...")
    run_flet_app()
