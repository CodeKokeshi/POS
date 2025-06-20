"""
Main entry point for the Printing Business POS System
"""

import sys
import os

# Add the current directory to Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.main_window import main

if __name__ == "__main__":
    sys.exit(main())
