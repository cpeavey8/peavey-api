"""
Wrapper to support both import styles:
- from main import app
- from api_root.main import app
"""
from api_root.main import app

__all__ = ['app']
