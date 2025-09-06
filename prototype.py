import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = ".db"

# ------------------ Database Setup ------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Courses
    c.execute("""
        CREATE TABLE IF NOT EXISTS Course(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            major TEXT,
            price REAL
        )
    """)

    # Instructors linked to course
    c.execute("""
        CREATE TABLE IF NOT EXISTS Instructors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            course_id INTEGER,
            city TEXT,
            salary REAL,
            FOREIGN KEY(course_id) REFERENCES Course(id)
        )
    """)

    # Candidates linked to course
    c.execute("""
        CREATE TABLE IF NOT EXISTS Candidates(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            course_id INTEGER,
            registration_date TEXT,
            paid_amount REAL,
            FOREIGN KEY(course_id) REFERENCES Course(id)
        )
    """)

    conn.commit()
    conn.close()

# ------------------ Add Dialog ------------------
class AddDialog(tk.Toplevel):
    def __init__(self, parent, table_name, fields, refresh_callback):
        super().__init__(parent)
        self.title(f"Add to {table_name}")
        self.table = table_name
        self.fields = fields
        self.refresh_callback = refresh_callback
        self.entries = {}

        for i, f in enumerate(fields):
            tk.Label(self, text=f).grid(row=i, column=0, padx=5, pady=5, sticky="e")

            if f == "course_id":
                courses = self.get_courses()
                entry = ttk.Combobox(self, values=[f"{c[0]} - {c[1]}" for c in courses], state="readonly")
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries[f] = entry
            else:
                entry = tk.Entry(self)
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries[f] = entry

        submit_btn = tk.Button(self, text="Add", command=self.submit)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def get_courses(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, name FROM Course")
        rows = c.fetchall()
        conn.close()
        return rows

    def submit(self):
        values = []
        for f in self.fields:
            val = self.entries[f].get()
            if f == "course_id" and val:
                val = val.split(" - ")[0]  # Extract course ID
            values.append(val)

        if not values[0]:  # name field is always first
            messagebox.showwarning("Warning", "First field cannot be empty")
            return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        placeholders = ",".join("?" * len(values))
        c.execute(f"INSERT INTO {self.table} ({','.join(self.fields)}) VALUES ({placeholders})", values)
        conn.commit()
        conn.close()
        self.refresh_callback()  # Refresh the table
        self.destroy()

# ------------------ Main App ------------------
class CoursesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Courses Management System")
        self.geometry("1000x600")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        self.tables = {}
        self.table_definitions = {
            "Candidates": ["name", "phone", "course_id", "registration_date", "paid_amount"],
            "Instructors": ["name", "phone", "course_id", "city", "salary"],
            "Course": ["name", "major", "price"]
        }

        for table_name, fields in self.table_definitions.items():
            tab = ttk.Frame(self.tabs)
            self.tabs.add(tab, text=table_name)
            tree = ttk.Treeview(tab, columns=["ID"] + fields, show="headings")
            tree.pack(fill="both", expand=True)

            for col in ["ID"] + fields:
                tree.heading(col, text=col)
                tree.column(col, width=120)

            self.tables[table_name] = tree

            btn_frame = ttk.Frame(tab)
            btn_frame.pack(fill="x")
            add_btn = ttk.Button(btn_frame, text=f"Add {table_name[:-1]}",
                                 command=lambda t=table_name, f=fields: self.add_item(t, f))
            del_btn = ttk.Button(btn_frame, text="Delete Selected",
                                 command=lambda t=table_name: self.delete_selected(t))
            add_btn.pack(side="left", padx=5, pady=5)
            del_btn.pack(side="left", padx=5, pady=5)

        self.load_all_data()

    # ------------------ Load Data ------------------
    def load_all_data(self):
        for table_name in self.tables:
            self.load_data(table_name)

    def load_data(self, table_name):
        tree = self.tables[table_name]
        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        if table_name == "Candidates":
            c.execute("""
                SELECT Candidates.id, Candidates.name, Candidates.phone, 
                       Course.name, Candidates.registration_date, Candidates.paid_amount
                FROM Candidates
                LEFT JOIN Course ON Candidates.course_id = Course.id
            """)
        elif table_name == "Instructors":
            c.execute("""
                SELECT Instructors.id, Instructors.name, Instructors.phone, 
                       Course.name, Instructors.city, Instructors.salary
                FROM Instructors
                LEFT JOIN Course ON Instructors.course_id = Course.id
            """)
        else:
            c.execute("SELECT * FROM Course")

        rows = c.fetchall()
        conn.close()

        for r in rows:
            tree.insert("", "end", values=r)

    # ------------------ Add/Delete ------------------
    def add_item(self, table, fields):
        AddDialog(self, table, fields, lambda: self.load_data(table))

    def delete_selected(self, table):
        tree = self.tables[table]
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No row selected")
            return
        record_id = tree.item(selected[0])["values"][0]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        self.load_data(table)

# ------------------ Run ------------------
if __name__ == "__main__":
    init_db()
    app = CoursesApp()
    app.mainloop()
