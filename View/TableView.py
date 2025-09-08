import tkinter as tk
from tkinter import ttk
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Controller'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
from Model import DataModel,DB,TableJoin
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
        self.join_frame = {}
        
        # import definition object from Model
        self.table_definitions = DataModel.model

        self.join_graph = TableJoin.Graph()
        self.current_node = list(self.table_definitions.keys())[0]
        self.join_graph.visited[self.current_node] = []
        self.join_graph.visited[self.current_node].append(self.current_node)

        for table_name, col_name in self.table_definitions.items():
            # Add a tab for each table
            tab = ttk.Frame(self.tabs)
            self.tabs.add(tab, text=table_name)

            # Create frame
            filter_frame = ttk.Frame(tab)
            filter_frame.pack(fill="x", padx=5, pady=5)
            
            # if table_name not in self.join_frame:
            #     self.join_frame[table_name] = 
            self.join_frame[table_name] = ttk.Frame(filter_frame)
            self.join_frame[table_name].pack(side="left", fill="x", expand=True, padx=5)

            # Add Join Tables
            current = table_name
            for nei in self.join_graph.g[current]:
                join_table_btn = ttk.Button(self.join_frame[current], text=f"Join {nei}")
                join_table_btn.config(command=lambda t=table_name, n=nei, btn=join_table_btn: self.join_table(t, n, btn))
                join_table_btn.pack(side="left", padx=5)

            # Add search bar
            search_var = tk.StringVar()
            search_entry = ttk.Entry(filter_frame, textvariable=search_var)
            search_entry.pack(side="left", fill="x", expand=True, padx=5)
            search_btn = ttk.Button(filter_frame, text="Search",
                                    command=lambda t=table_name, sv=search_var: self.search_table(t, sv.get()))
            search_btn.pack(side="left", padx=5)

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


        # Bind tab change event to update current_node
        self.tabs.bind('<<NotebookTabChanged>>', self.on_tab_changed)

        self.load_all_data()

    def on_tab_changed(self, event):
        selected_tab = event.widget.select()
        tab_index = event.widget.index(selected_tab)
        table_name = list(self.table_definitions.keys())[tab_index]
        self.current_node = table_name

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
        AddDialog.AddDialog(self, table, lambda: self.load_all_data())
    
    def delete_selected(self, table):
        tree = self.tables[table]
        selected = tree.selection()
        if not selected:
            print("Warning", " No row selected")
            #messagebox.showwarning("Warning", "No row selected")
            return
        record_id = tree.item(selected[0])["values"][0]
        delete.delete(DB.db(), table, [record_id])
        self.reload()

    def reload(self):
        self.load_all_data()

    def search_table(self, table_name, query):
        # Get all rows
        all_rows = DataController.load_data(table_name)
        # Clear table
        self.clear_table(table_name)
        # Filter and insert matching rows
        for r in all_rows:
            if any(query.lower() in str(cell).lower() for cell in r):
                self.tables[table_name].insert("", "end", values=r)
    
    def join_table(self, table_name, merge_with, btn):
        # Remove pressed join button
        btn.destroy()

        print(f"join {self.current_node} with {merge_with}")
        self.current_node = merge_with
        if table_name not in self.join_graph.visited:
            self.join_graph.visited[table_name] = []
        self.join_graph.visited[table_name].append(merge_with)

        self.update_join_buttons(table_name)

    def update_join_buttons(self, table_name):

        # Add Join Tables
        current = self.current_node
        for nei in self.join_graph.g[current]:
            if nei in self.join_graph.visited[table_name]:
                state = 'Disjoin'
            else:
                state = 'Join'
            join_table_btn = ttk.Button(self.join_frame[table_name], text=f"{state} {nei}")
            join_table_btn.config(command=lambda t=table_name, n=nei, btn=join_table_btn: self.join_table(t, n, btn))
            join_table_btn.pack(side="left", padx=5)
        