import tkinter as tk
from tkinter import ttk
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Controller'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Router'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Students'))
from Model import DataModel,DB
from Controller import DataController
from Model.Query import delete
from Router import route as _r

# ------------------ Main App ------------------
class CoursesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window Info
        self.title("Courses Management System")
        self.geometry("1000x600")

        # Create Tabs
        self.topbar_frame = ttk.Frame(self)
        self.topbar_frame.pack(side="top", fill='x', padx=15, pady=(10,0))
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        # Tables Definitions
        self.tables = {}
        self.action_btns_frame = {}
        self.tail_frame = {}
        self.tail_left = {}
        self.tail_right = {}
        self.edit_btn = {}
        self.search_var = {}
        self.search_entry = {}
        self.search_btn = {}
        self.report_btn = {}

        def settings_btn_pressed():
            from View.Settings.SettingsViewController import SettingsView
            _r.route(current=self, to=SettingsView(self))

        self.settings_btn = ttk.Button(self.topbar_frame, text="Settings", command=settings_btn_pressed)
        # self.settings_btn.pack(side='left')
        
        # import definition object from Model
        self.table_definitions = DataModel.model

        # selected row in table
        self.selected_obj = {}
        
    def load(self):
        for table_name, col_name in self.table_definitions.items():
            # Add a tab for each table
            tab = ttk.Frame(self.tabs)
            self.tabs.add(tab, text=table_name)

            # Create frame
            filter_frame = ttk.Frame(tab)
            filter_frame.pack(fill="x", padx=5, pady=5)

            self.action_btns_frame[table_name] = ttk.Frame(filter_frame)
            self.action_btns_frame[table_name].pack(side="left", fill="x", expand=True, padx=5)

            # Add Action Buttons
            current = table_name
            create_btn = ttk.Button(self.action_btns_frame[current],
                                    text=f"Create New {current}",
                                    command= lambda t=current: self.create_btn_pressed(t))
            create_btn.pack(side="left", padx=5)

            self.edit_btn[table_name] = ttk.Button(self.action_btns_frame[current],
                                    text=f"Edit {current}",
                                    command= lambda t=current: self.edit_btn_pressed(t))
            

            # Add search bar
            self.search_var[table_name] = tk.StringVar(self)
            self.search_entry[table_name] = ttk.Entry(filter_frame, textvariable=self.search_var[table_name])
            self.search_entry[table_name].pack(side="left", fill="x", expand=True, padx=5)
            self.search_btn[table_name] = ttk.Button(filter_frame, text="Search",
                                    command=lambda t=table_name, sv=self.search_var[table_name]: self.search_table(t, sv.get()))
            self.search_btn[table_name].pack(side="left", padx=5)
            # Refresh Button
            refresh_btn = ttk.Button(filter_frame, text='Refresh', command=self.reload)
            refresh_btn.pack(side='left', padx=5)

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
            self.tail_frame[table_name] = ttk.Frame(tab)
            self.tail_frame[table_name].pack(fill="x")

            self.tail_left[table_name] = ttk.Frame(self.tail_frame[table_name])
            self.tail_left[table_name].pack(side='left', fill="x", expand=True, padx=5, pady=5)

            # Temp frame (empty space) => divide to 3 portions
            center_frame = ttk.Frame(self.tail_frame[table_name])
            center_frame.pack(side='left', fill="x", expand=True, padx=5, pady=5)

            self.tail_right[table_name] = ttk.Frame(self.tail_frame[table_name])
            self.tail_right[table_name].pack(side='right', fill="x", expand=True, padx=5, pady=5)

            # Create Add Button (When pressed, open add button Dialog from Controller)
            self.report_btn[table_name] = ttk.Button(self.tail_right[table_name], text=f"Report",
                                 command=lambda t=table_name
                                 : self.report_pressed(t))
            

        self.payment_btn = ttk.Button(self.action_btns_frame['students'],
                                text=f"Add Payment",
                                command=lambda t='students': self.payment_btn_pressed(t))
        self.withdraw_btn = ttk.Button(self.action_btns_frame['doctors'],
                                text=f"Withdraw",
                                command=lambda t='doctors': self.withdraw_btn_pressed(t))
        self.attendance_btn = ttk.Button(self.tail_left['courses'],
                                text=f"Record Attendance",
                                command=lambda t='courses': self.attendance_btn_pressed(t))
        self.search_student_entry = ttk.Entry(self.tail_left['courses'])
        self.report_btn['courses'].pack(side="right")


        # Bind tab change event to update current_node
        self.tabs.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        for table_name in self.tables:
            self.tables[table_name].bind('<<TreeviewSelect>>', self.on_row_select)

        self.load_all_data()
        self.view()

    
    def on_tab_changed(self, event):
        selected_tab = event.widget.select()
        tab_index = event.widget.index(selected_tab)
        table_name = list(self.table_definitions.keys())[tab_index]
        self.current_node = table_name

    def on_row_select(self, event):
        tree = event.widget
        table_name = None
        for name, t in self.tables.items():
            if t == tree:
                table_name = name
                break
        selected = tree.selection()
        if selected:
            self.edit_btn[table_name].config(command=lambda t=table_name: self.edit_btn_pressed(t))
            self.edit_btn[table_name].pack(side="left", padx=5)
            row_data = tree.item(selected[0])["values"]
            # print(row_data)
            if table_name == 'students':
                self.payment_btn.config(command=lambda t='students': self.payment_btn_pressed(t))
                self.payment_btn.pack(side='left', padx=5)
                self.report_btn[table_name].pack(side="right")
                self.selected_obj[table_name] = DataModel.Student(row_data[0])
                if not self.selected_obj[table_name]:
                    self.payment_btn.pack_forget()
                    self.report_btn[table_name].pack_forget()
            elif table_name == 'doctors':
                self.selected_obj[table_name] = DataModel.Doctor(row_data[0])
                self.withdraw_btn.config(command=lambda t='doctors': self.withdraw_btn_pressed(t))
                self.withdraw_btn.pack(side='left', padx=5)
                if not self.selected_obj[table_name]:
                    self.withdraw_btn.pack_forget()
            elif table_name == 'courses':
                # self.search_student_entry.pack(side="left", padx=(0,15), fill="x", expand=True)
                # self.attendance_btn.config(command=lambda t='courses': self.attendance_btn_pressed(t))
                # self.attendance_btn.pack(side='left')
                self.selected_obj[table_name] = DataModel.Course(row_data[0])
            if not self.selected_obj[table_name]:
                    self.edit_btn[table_name].pack_forget()
                    self.reload()
        else:
            self.edit_btn[table_name].pack_forget()
            if table_name == 'students':
                self.report_btn[table_name].pack_forget()
                self.payment_btn.pack_forget()
            elif table_name == 'doctors':
                self.withdraw_btn.pack_forget()

    def clear_table(self, table_name):
        tree = self.tables[table_name]
        for row in tree.get_children():
            tree.delete(row)

    def load_all_data(self):
        # Load data from Controller
        for table_name in self.tables:
            self.load_data(table_name)

    def load_data(self, table):
        # Clear table before fetching results
        self.clear_table(table)
        rows = DataController.load_data(table)
        if rows:
            # Fetch results to the table view
            for r in rows:
                self.tables[table].insert("", "end", values=r)
    
    def delete_selected(self, table):
        tree = self.tables[table]
        selected = tree.selection()
        if not selected:
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
    
    def create_btn_pressed(self, table_name):
        if table_name == 'students':
            from View.Students.student_add_view import StudentAddView
            new_student_view = StudentAddView(self)
            _r.route(current=self, to=new_student_view)
        elif table_name == 'courses':
            from View.Courses.course_add_view import CourseAddView
            new_course_view = CourseAddView(self)
            _r.route(current=self, to=new_course_view)
        elif table_name == 'doctors':
            from View.Doctors.doctor_add_view import DoctorAddView
            new_doctor_view = DoctorAddView(self)
            _r.route(current=self, to=new_doctor_view)


    def edit_btn_pressed(self, table_name):
        if table_name == 'students':
            from View.Students.student_edit_view import StudentEditView
            new_student_view = StudentEditView(self,self.selected_obj[table_name])
            _r.route(current=self, to=new_student_view)
        elif table_name == 'courses':
            from View.Courses.course_edit_view import CourseEditView
            new_course_view = CourseEditView(self,self.selected_obj[table_name])
            _r.route(current=self, to=new_course_view)
        elif table_name == 'doctors':
            from View.Doctors.doctor_edit_view import DoctorEditView
            new_doctor_view = DoctorEditView(self,self.selected_obj[table_name])
            _r.route(current=self, to=new_doctor_view)


    def payment_btn_pressed(self, table_name):
        from View.Students.student_payment_view import StudentPaymentView
        new_student_view = StudentPaymentView(self,self.selected_obj[table_name])
        _r.route(current=self, to=new_student_view)

    def withdraw_btn_pressed(self, table_name):
        return
        # from View.Doctors.doctor_withdraw_view import DoctorWithdrawView
        # new_doctor_view = DoctorWithdrawView(self,self.selected_obj[table_name])
        # _r.route(current=self, to=new_doctor_view)

    # def attendance_btn_pressed(self, table_name):
    #     print("attendance pressed")

    def report_pressed(self, table_name):
        if table_name == "students":
            from View.Students.student_report_view import StudentReportView
            new_student_view = StudentReportView(self,self.selected_obj[table_name])
            _r.route(current=self, to=new_student_view)
        elif table_name == 'courses':
            from View.Courses.course_report_view import CourseReportView
            new_course_view = CourseReportView(self)
            _r.route(current=self, to=new_course_view)


    def view(self):
        self.load_all_data()
        self.lift()           # Bring window to front
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode


        