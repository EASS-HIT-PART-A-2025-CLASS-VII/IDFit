# conftest.py
import sys
from pathlib import Path

# מוסיפים את התיקייה app (שם נמצא המודול app.main) ל־sys.path
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "app"))
