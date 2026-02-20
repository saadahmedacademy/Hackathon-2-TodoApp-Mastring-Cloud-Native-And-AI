import sys
import os
import pytest

# Add the 'src' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

print(f"DEBUG: sys.path at conftest.py: {sys.path}") # Add this line for debugging