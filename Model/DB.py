import os
import time
import sys
import sqlite3
from dotenv import load_dotenv # type: ignore
import tkinter
from tkinter import messagebox

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

APP_NAME = "CoursesManagementSystem"
USER_DATA_DIR = os.path.join(os.path.expanduser("~"), f".{APP_NAME}")

# Ensure persistent directory exists
os.makedirs(USER_DATA_DIR, exist_ok=True)

# Load environment file from assets (project structure)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
env_path = os.path.join(ASSETS_DIR, ".env")
load_dotenv(env_path)

DB_NAME = os.getenv("DB_NAME") or "database.db"
SOURCE_DB_PATH = os.path.join(ASSETS_DIR, DB_NAME)
TARGET_DB_PATH = os.path.join(USER_DATA_DIR, DB_NAME)

# Copy if not exists
if not os.path.exists(TARGET_DB_PATH):
    import shutil
    shutil.copy2(SOURCE_DB_PATH, TARGET_DB_PATH)

# Use the persistent database
DB_PATH = TARGET_DB_PATH
# show_error(f"Database Path: {DB_PATH}", 1)

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
                    cls._instance = sqlite3.connect(os.path.abspath(DB_PATH))
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
        