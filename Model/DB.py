import os
import time
import sys
import sqlite3
from dotenv import load_dotenv # type: ignore
import tkinter
from tkinter import messagebox

# Get absolute path to the assets folder (relative to project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

message = ""
title = ""
def show_error(message: str, flag=0):
    if flag == 0:
        messagebox.showerror(
                "Database Report",
                message
        )
    else:
        messagebox.showinfo(
                "Database Report",
                message
        )

# Load the .env file
env_path = os.path.join(ASSETS_DIR, ".env")
if not os.path.exists(env_path):
    message = f"⚠️ Database not found (-2)"
    # show_error(message)
else:
    load_dotenv(env_path)

# Read the DB name from .env
DB_NAME = os.getenv("DB_NAME") or "database.db"
if not DB_NAME:
    message = "⚠️ Database not found (-1)"
    # show_error(message)
else:
    message = f"✅ Loaded Database Successfully (0000)"
    # show_error(message)

# Build full database path
DB_PATH = os.path.join(ASSETS_DIR, DB_NAME)

class db:
    def terminate(self):
        try:
            self.close()
        except Exception as error:
            message = f"Failed terminating session: {error}"
            show_error(message)

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
            message = f"Failed to fetch all rows: {error}"
            show_error(message)
            return None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            trials = 10
            while trials > 0:
                try:
                    cls._instance = sqlite3.connect(DB_PATH)
                    message = f"✅ Loaded Database Successfully (0000)"
                    show_error(message,1)
                    break
                except Exception as error:
                    message = f"Database connection failed: {error}. Retrying in 5 seconds..."
                    show_error(message)
                    time.sleep(5)
                trials -= 1
            if cls._instance is None:
                message = "Failed to establish database connection after multiple attempts."
                show_error(message)
                raise Exception(message)
        return cls._instance
        