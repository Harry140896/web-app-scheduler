import sqlite3
from pathlib import Path

CURRENT_FOLDER = Path(__file__).resolve().parent 
PROJECT_ROOT = CURRENT_FOLDER.parent
DATABASE_FOLDER = PROJECT_ROOT / "database"


print(CURRENT_FOLDER)
print(PROJECT_ROOT)
print(DATABASE_FOLDER)  