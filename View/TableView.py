import tkinter as tk
from tkinter import ttk
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Controller'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Router'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Students'))
from Model import DataModel,DB
from Controller import DataController
from View import AddDialogViewController as AddDialog
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
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        # Tables Definitions
        self.tables = {}
        self.action_btns_frame = {}
        
        # import definition object from Model
        self.table_definitions = DataModel.model
        

        for table_name, col_name in self.table_definitions.items():
            # Add a tab for each table
            tab = ttk.Frame(self.tabs)
            self.tabs.add(tab, text=table_name)

            # Create frame
            filter_frame = ttk.Frame(tab)
            filter_frame.pack(fill="x", padx=5, pady=5)
            
            # if table_name not in self.join_frame:
            #     self.join_frame[table_name] = 
            self.action_btns_frame[table_name] = ttk.Frame(filter_frame)
            self.action_btns_frame[table_name].pack(side="left", fill="x", expand=True, padx=5)

            # Add Action Buttons
            current = table_name
            create_btn = ttk.Button(self.action_btns_frame[current],
                                    text=f"Create New {current}",
                                    command= lambda t=current: self.create_btn_pressed(t))
            create_btn.pack(side="left", padx=5)

            edit_btn = ttk.Button(self.action_btns_frame[current],
                                    text=f"Edit {current}",
                                    command= lambda t=current: self.edit_btn_pressed(t))
            edit_btn.pack(side="left", padx=5)



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

        payment_btn = ttk.Button(self.action_btns_frame['Students'],
                                text=f"Add Payment",
                                command=lambda t='Students': self.payment_btn_pressed(t))
        payment_btn.pack(side="left", padx=5)


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
    
    def create_btn_pressed(self, table_name):
        print("create")
        if table_name == 'Students':
            print('student')
            from View.Students.student_add_view import StudentAddView
            new_student_view = StudentAddView(self)
            _r.route(current=self, to=new_student_view)
        elif table_name == 'Courses':
            print('course')
            from View.Courses.course_add_view import CourseAddView
            new_course_view = CourseAddView(self)
            _r.route(current=self, to=new_course_view)


    def edit_btn_pressed(self, table_name):
        print("edit")
        if table_name == 'Students':
            from Model.DataModel import Student
            student = Student()
            student.load_fake_data()
            from View.Students.student_edit_view import StudentEditView
            new_student_view = StudentEditView(self,student)
            _r.route(current=self, to=new_student_view)
        elif table_name == 'Courses':
            from Model.DataModel import Course
            course = Course()
            course.load_fake_data()
            from View.Courses.course_edit_view import CourseEditView
            new_course_view = CourseEditView(self,course)
            _r.route(current=self, to=new_course_view)


    def payment_btn_pressed(self, table_name):
        print("payment")
        from Model.DataModel import Student
        student = Student()
        student.load_fake_data()
        from View.Students.student_payment_view import StudentPaymentView
        new_student_view = StudentPaymentView(self,student)
        _r.route(current=self, to=new_student_view)
        #_r.route(table_name, to="edit")

    def view(self):
        self.lift()           # Bring window to front
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode


        