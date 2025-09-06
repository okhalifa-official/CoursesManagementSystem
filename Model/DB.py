import time
import sqlite3
from dotenv import load_dotenv # type: ignore
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '../', '.env'))
DB_NAME = os.getenv('DB_NAME')

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
            cursor = self.cursor()
            return cursor.fetchall()
        except Exception as error:
            print(f"Failed to fetch all rows: {error}")
            return None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            trials = 10
            while trials > 0:
                try:
                    cls._instance = sqlite3.connect(DB_NAME)
                    break
                except Exception as error:
                    print(f"Database connection failed: {error}. Retrying in 5 seconds...")
                    time.sleep(5)
                trials -= 1
            if cls._instance is None:
                raise Exception("Failed to establish database connection after multiple attempts.")
        return cls._instance
        