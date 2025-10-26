import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Controller'))
from Model.DataModel import Doctor
from Controller import DataController
from lib.DateModule import DatePicker
import Router.route as _r

class DoctorWithdrawView(tk.Toplevel):
    def __init__(self, parent, doctor):
        super().__init__(parent)

        # Window Info
        self.title("Doctor Withdraws")
        self.geometry("1000x600")
        self.doctor = doctor

    def load(self):
        doctor = self.doctor
        self.entry = {}
        self.entry['Doctor ID'] = doctor._doctor_data[doctor._doctor_columns[0]]
        self.entry['Withdraw ID'] = None
        self.withdraw_table = None
        self.isEditingWithdraw = False
        self.withdrawID = None

        # Back Button
        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back", command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        # Main layout
        left_stack = ttk.Frame(self)
        left_stack.pack(side="left", fill="both", expand=True, pady=(30,50), padx=(25,20))

        right_stack = ttk.Frame(self)
        right_stack.pack(side="right", fill="both", expand=True, pady=(30,50), padx=(10,25))

        # ==================== Left Stack ====================
        profile_frame = ttk.Labelframe(left_stack, text="Doctor Info")
        profile_frame.pack(side="top", fill="x", pady=(10, 0))

        ttk.Label(profile_frame, text=f"Name: {doctor._doctor_data[doctor._doctor_columns[1]]} {doctor._doctor_data[doctor._doctor_columns[2]]}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(profile_frame, text=f"Email: {doctor._doctor_data['Email']}").pack(anchor="w", padx=10, pady=5)
        ttk.Label(profile_frame, text=f"Phone: {doctor._doctor_data['Country Code']} {doctor._doctor_data['Phone Number']}").pack(anchor="w", padx=10, pady=5)
        # ttk.Label(profile_frame, text=f"Total Earnings: {doctor._doctor_data['Earnings']} EGP").pack(anchor="w", padx=10, pady=5)

        # Withdraw History Frame
        withdraw_history_frame = ttk.Labelframe(left_stack, text="Withdraw History")
        withdraw_history_frame.pack(side="top", fill="both", expand=True, pady=(30, 0))

        # Search bar
        filter_frame = ttk.Frame(withdraw_history_frame)
        filter_frame.pack(fill="x", pady=(10,5), padx=(10,10))

        search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=search_var)
        search_entry.pack(side="left", fill="x", expand=True)

        search_btn = ttk.Button(filter_frame, text="Search",
                                command=lambda: self.search_table(search_var.get()))
        search_btn.pack(side="left", padx=(10,0))

        # Table
        self.withdraw_columns = ['ID', 'Amount', 'Withdraw Method', 'Date']
        self.withdraw_table = ttk.Treeview(withdraw_history_frame, columns=self.withdraw_columns, show="headings")

        for col in self.withdraw_columns:
            self.withdraw_table.heading(col, text=col)
            self.withdraw_table.column(col, width=150)

        self.withdraw_table.pack(fill="both", expand=True, padx=(10,10), pady=(0,5))

        self.reload_withdraws()

        # ==================== Right Stack ====================
        withdraw_form_frame = ttk.Labelframe(right_stack, text="Add / Edit Withdraw")
        withdraw_form_frame.pack(side="top", fill="both", expand=True, pady=(5,0))

        form_frame = ttk.Frame(withdraw_form_frame)
        form_frame.pack(fill="both", expand=True)
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        # Amount
        ttk.Label(form_frame, text="Withdraw Amount").grid(row=0, column=0, pady=(20,10))
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=1, column=0, padx=20, sticky="ew")

        # Payment Method
        ttk.Label(form_frame, text="Withdraw Method").grid(row=0, column=1, pady=(20,10))
        self.method_entry = ttk.Combobox(form_frame, values=["Cash", "Bank Transfer", "Instapay", "Vodafone Cash"], state="readonly")
        self.method_entry.grid(row=1, column=1, padx=20, sticky="ew")

        # Date
        ttk.Label(form_frame, text="Date").grid(row=2, column=0, pady=(20,10))
        self.datepicker = DatePicker(form_frame, date_pattern="yyyy-mm-dd", initial_date=datetime.today().date())
        self.datepicker.grid(row=3, column=0, padx=20, sticky="ew")

        # Action buttons
        btn_frame = ttk.Frame(withdraw_form_frame)
        btn_frame.pack(pady=15)
        
        self.delete_btn = ttk.Button(btn_frame, text="Delete", style="Danger.TButton", command=self.delete_withdraw)
        self.delete_btn.grid(row=0, column=0, padx=5)
        self.delete_btn.grid_remove()

        self.confirm_btn = ttk.Button(btn_frame, text="Confirm Withdraw", command=self.confirm_withdraw)
        self.confirm_btn.grid(row=0, column=1, padx=5)

        # ==================== Selection Events ====================
        def select_withdraw(event):
            selected = self.withdraw_table.selection()
            if selected:
                withdraw_data = self.withdraw_table.item(selected[0], "values")
                self.withdrawID = withdraw_data[0]
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, withdraw_data[1].split()[0])
                self.method_entry.set(withdraw_data[2])

                try:
                    date_obj = datetime.strptime(withdraw_data[3], "%Y-%m-%d").date()
                except Exception:
                    date_obj = datetime.today().date()
                self.datepicker._set_date(date_obj)

                self.isEditingWithdraw = True
                self.delete_btn.grid()
                self.confirm_btn.config(text="Save Changes", command=self.update_withdraw)

        self.withdraw_table.bind("<<TreeviewSelect>>", select_withdraw)

    # ==================== Functions ====================
    def reload_withdraws(self):
        self.search_table()

    def clear_table(self):
        for row in self.withdraw_table.get_children():
            self.withdraw_table.delete(row)

    def search_table(self, query=""):
        self.clear_table()
        all_rows = DataController.load_table('doctor_withdraws', self.entry)
        for r in all_rows:
            if any(query.lower() in str(cell).lower() for cell in r):
                self.withdraw_table.insert("", "end", values=r)

    def confirm_withdraw(self):
        entry = {
            'Doctor ID': self.entry['Doctor ID'],
            'Amount': self.amount_entry.get(),
            'Payment Method': self.method_entry.get(),
            'Date': self.datepicker.entry.get()
        }
        if not entry['Amount'] or not entry['Payment Method']:
            messagebox.showerror("Error", "Please fill all required fields.")
            return
        if DataController.func_withdraw(func=DataController.confirm_withdraw, entry=entry):
            self.reload_withdraws()
            self.reset_form()

    def update_withdraw(self):
        entry = {
            'Withdraw ID': self.withdrawID,
            'Doctor ID': self.entry['Doctor ID'],
            'Amount': self.amount_entry.get(),
            'Payment Method': self.method_entry.get(),
            'Date': self.datepicker.entry.get(),
        }
        if DataController.func_withdraw(func=DataController.update_withdraw, entry=entry):
            self.reload_withdraws()
            self.reset_form()

    def delete_withdraw(self):
        if DataController.delete_withdraw(window=self, withdrawID=self.withdrawID):
            self.reload_withdraws()
            self.reset_form()

    def reset_form(self):
        self.amount_entry.delete(0, tk.END)
        self.method_entry.set('')
        self.datepicker._set_date(datetime.today())
        self.isEditingWithdraw = False
        self.withdrawID = None
        self.delete_btn.grid_remove()
        self.confirm_btn.config(text="Confirm Withdraw", command=self.confirm_withdraw)

    def view(self):
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        self.state('zoomed')
