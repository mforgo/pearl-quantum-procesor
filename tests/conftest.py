# tests/conftest.py
import sys
import os

# Insert the project's src directory at the front of sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
