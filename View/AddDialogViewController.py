import tkinter as tk
from tkinter import ttk
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
from Model import DataModel, DB
from Model.Query.select import select
from Model.Query.insert import insert

database = DB.db()

# ------------------ Add Dialog ------------------
class AddDialog(tk.Toplevel):
    def __init__(self, parent, table_name, refresh_callback):
        super().__init__(parent)
        self.title(f"Add to {table_name}")
        self.table = table_name

        fields = DataModel.model['table_name']
        self.fields = fields
        self.refresh_callback = refresh_callback
        self.entries = {}

        table_fk_list = DataModel.foreign_keys[self.table]
        for i, f in enumerate(fields):
            tk.Label(self, text=f).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            
            isRelation = False
            for fk_obj in table_fk_list:
                # if column is foreign key (for relation)
                if f == fk_obj[0]:
                    isRelation = True
                    
                    # load records in combobox
                    table_realtion = [{fk_obj[1], ''}]
                    db_res = select(database, table_realtion)
                    records = db_res.fetchall()

                    # build combobox with all records
                    entry = ttk.Combobox(self, values=[f"{rec[0]} - {rec[1]}" for rec in records], state="readonly")
                    entry.grid(row=i, column=1, padx=5, pady=5)
                    self.entries[f] = entry

            if not isRelation:
                # build textbox for entry
                entry = tk.Entry(self)
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries[f] = entry

        submit_btn = tk.Button(self, text="Add", command=self.submit)
        submit_btn.grid(row=len(fields), column=1, columnspan=2, pady=10)

        cancel_btn = tk.Button(self, text="Cancel", command=self.cancel)
        cancel_btn.grid(row=len(fields), column=2, columnspan=2, pady=10)

    def submit(self):
        values = []
        for f in self.fields:
            val = self.entries[f].get()
            if f == "course_id" and val:
                val = val.split(" - ")[0]  # Extract course ID
            values.append(val)

        if len(values) != len(self.fields):  # not all feilds are filled
            print("Warning", " All fields must be filled")
            #messagebox.showwarning("Warning", "All fields must be filled")
            return
        
        # insert values in the table
        table_definition = (self.table, self.fields)
        insert(database, table_definition, values)

        self.refresh_callback()  # Refresh the table
        self.destroy()

    def cancel(self):
        self.destroy()