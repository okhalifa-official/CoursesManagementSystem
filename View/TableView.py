import tkinter as tk
from tkinter import ttk
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Controller'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
from Model import DataModel,DB
from Controller import DataController
from View import AddDialogViewController as AddDialog
from Model.Query import delete

# ------------------ Main App ------------------
class CoursesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Window Info
        self.title("Courses Management System")
        self.geometry("1000x600")

        # Create Tabs
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        # Tables Definitions
        self.tables = {}
        # import definition object from Model
        self.table_definitions = DataModel.model

        for table_name, col_name in self.table_definitions.items():
            # Add a tab for each table
            tab = ttk.Frame(self.tabs)
            self.tabs.add(tab, text=table_name)
            
            # Create Table View
            tree = ttk.Treeview(tab, columns=col_name, show="headings")
            tree.pack(fill="both", expand=True)

            # Fill records for the table
            for col_data in col_name:
                tree.heading(col_data, text=col_data)
                tree.column(col_data, width=120)

            # Add the data to the table
            self.tables[table_name] = tree

            # Build frame for buttons inside the Tab View
            btn_frame = ttk.Frame(tab)
            btn_frame.pack(fill="x")

            # Create Add Button (When pressed, open add button Dialog from Controller)
            add_btn = ttk.Button(btn_frame, text=f"Add {table_name[:-1]}",
                                 command=lambda t=table_name, f=col_name
                                 : self.add_item(t, f))
            
            # Create Delete Button (deletes selected record by calling delete_selected from Controller)
            del_btn = ttk.Button(btn_frame, text="Delete Selected",
                                 command=lambda t=table_name:
                                   self.delete_selected(t))
            
            # Style Buttons
            add_btn.pack(side="left", padx=5, pady=5)
            del_btn.pack(side="left", padx=5, pady=5)

        self.load_all_data()

    def clear_table(self, table_name):
        tree = self.tables[table_name]
        for row in tree.get_children():
            tree.delete(row)

    def load_all_data(self):
        # Load data from Controller
        for table_name in self.tables:
            self.load_data(table_name)

    def load_data(self, table):
        rows = DataController.load_data(table)
        if rows:
            # Clear table before fetching results
            self.clear_table(table)
            # Fetch results to the table view
            for r in rows:
                self.tables[table].insert("", "end", values=r)

    def add_item(self, table, fields):
        AddDialog.AddDialog(self, table, lambda: self.load_data(table))
    
    def delete_selected(self, table):
        tree = self.tables[table]
        selected = tree.selection()
        if not selected:
            print("Warning", " No row selected")
            #messagebox.showwarning("Warning", "No row selected")
            return
        record_id = tree.item(selected[0])["values"][0]
        delete.delete(DB.db(), table, [record_id])
        self.load_data(table)