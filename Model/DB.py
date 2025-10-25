import os
import time
import sys
import sqlite3
from dotenv import load_dotenv # type: ignore

# Get absolute path to the assets folder (relative to project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Load the .env file
env_path = os.path.join(ASSETS_DIR, ".env")
if not os.path.exists(env_path):
    print(f"⚠️ .env not found at {env_path}")
else:
    load_dotenv(env_path)

# Read the DB name from .env
DB_NAME = os.getenv("DB_NAME")
if not DB_NAME:
    print("⚠️ DB_NAME not found in .env")
else:
    print(f"✅ Loaded DB_NAME = {DB_NAME}")

# Build full database path
DB_PATH = os.path.join(ASSETS_DIR, DB_NAME)
print(f"✅ Using database path: {DB_PATH}")

class db:
    def terminate(self):
        try:
            self.close()
        except Exception as error:
            print(f"Failed terminating session: {error}")

    def is_connected(self):
        try:
            self.execute("SELECT 1")
            return True
        except Exception:
            return False

    def fetchall(self):
        try:
            return self._cursor.fetchall()
        except Exception as error:
            print(f"Failed to fetch all rows: {error}")
            return None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            trials = 10
            while trials > 0:
                try:
                    cls._instance = sqlite3.connect(DB_PATH)
                    break
                except Exception as error:
                    print(f"Database connection failed: {error}. Retrying in 5 seconds...")
                    time.sleep(5)
                trials -= 1
            if cls._instance is None:
                raise Exception("Failed to establish database connection after multiple attempts.")
        return cls._instance
        