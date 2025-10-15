import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Controller'))
from DataModel import Student
import DataArchitecture as DataArch
import Router.route as _r
from Query import select, insert, delete
import DB
from Controller import DataController,PopupHandler
from datetime import datetime


class StudentReportView(tk.Toplevel):
    def __init__(self, parent, student: Student):
        super().__init__(parent)

        # Window Info
        self.title("Student Report")
        self.geometry("1000x600")
        self.student = student

    def load(self):
        student = self.student
        self.entry = {}
        self.courses_table = None
        self.payments_table = None
        self.search_var = tk.StringVar()
        self.pay_search_var = tk.StringVar()

        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        left_stack = ttk.Frame(self)
        left_stack.pack(side="left", fill="both", expand=True, pady=(30,50), padx=(25,20))

        right_stack = ttk.Frame(self)
        right_stack.pack(side="right", fill="both", expand=True, pady=(30,50), padx=(10,25))

        profile_frame = tk.Frame(left_stack)
        profile_frame.pack(side="top", fill="x")

        courses_table_frame = ttk.Labelframe(left_stack, text="Enrolled Courses")
        courses_table_frame.pack(side="top", fill="both", expand=True, pady=(30,0))


        #---------------- Student Profile
        student_card_pfp = tk.Frame(profile_frame)
        student_card_pfp.pack(side="left", fill=None, expand=False, padx=(10,5))
    

        student_card_details_frame = tk.Frame(profile_frame)
        vertical_stack = tk.Frame(student_card_details_frame)

        vertical_stack.pack(side="left", expand=True, fill="x", padx=(15,0))

        student_card_details_frame.pack(side="left", fill="x", expand=True, padx=(10,5))
        self.entry['Student Image'] = None
        self.img_preview = tk.Label(student_card_pfp, text="No Image", width=20, height=8, bg="#eee", relief="ridge")
        self.img_preview.pack(side="top")

        # Load existing image
        if student._student_data['Image']:
            path = student._student_data['Image']
            # Show image in label
            img = Image.open(path)
            # Calculate new size to ensure min width/height 100
            w, h = img.size
            scale = max(100/w, 100/h)
            new_w, new_h = int(w*scale), int(h*scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            # Center crop to 100x100 if needed
            if new_w > 100 or new_h > 100:
                left = (new_w - 100) // 2
                top = (new_h - 100) // 2
                img = img.crop((left, top, left+100, top+100))
            self.img_tk = ImageTk.PhotoImage(img)
            self.img_preview.config(image=self.img_tk, text="", width=100, height=100)
        
        #--------------- Student Details

        name_label = ttk.Label(vertical_stack, text=f"Name: {student._student_data[student._student_columns[1]]} {student._student_data[student._student_columns[2]]}")
        name_label.grid(pady=(5,0), row=0, column=0, sticky="w", padx=(0,20))
        email_label = ttk.Label(vertical_stack, text=f"Email: {student._student_data[student._student_columns[7]]}")
        email_label.grid(pady=(5,0), row=0, column=1, sticky="w", padx=(50,0))
        phone_label = ttk.Label(vertical_stack, text=f"Phone number: {student._student_data[student._student_columns[4]]} {student._student_data[student._student_columns[5]]}")
        phone_label.grid(pady=(5,0), row=1, column=0, sticky="w")
        address_label = ttk.Label(vertical_stack, text=f"Address: {student._student_data[student._student_columns[6]]}")
        address_label.grid(pady=(5,0), row=1, column=1, sticky="w", padx=(50,0))
        university_label = ttk.Label(vertical_stack, text=f"University: {student._student_data[student._student_columns[8]]}")
        university_label.grid(pady=(5,0), row=2, column=0, sticky="w", padx=(0,20))
        barcode_label = ttk.Label(vertical_stack, text=f"Barcode: {student._student_data[student._student_columns[9]]}")
        barcode_label.grid(pady=(5,5), row=3, column=0, sticky="w", padx=(0,20))

        # ==========================   COURSES TABLE VIEW
        filter_frame = ttk.Frame(courses_table_frame)
        filter_frame.pack(fill="x", pady=(10,5), padx=(10,10))
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True)
        search_btn = ttk.Button(filter_frame, text="Search")
        search_btn.pack(side="left", padx=(10,0))
        
        self.course_columns = ["Course Name", "Price", "Paid", "Remaining", "Date"]
        self.courses_table = ttk.Treeview(courses_table_frame, columns=self.course_columns, show="headings")
        self.courses_table.heading('Course Name', text='Course Name')
        self.courses_table.column('Course Name', width=150)
        self.courses_table.heading('Price', text='Price')
        self.courses_table.column('Price', width=80)
        self.courses_table.heading('Paid', text='Paid')
        self.courses_table.column('Paid', width=80)
        self.courses_table.heading('Remaining', text='Remaining')
        self.courses_table.column('Remaining', width=80)
        self.courses_table.heading('Date', text='Enrolled At')
        self.courses_table.column('Date', width=130)
        self.courses_table.pack(fill="both", expand=True, padx=(10,10), pady=(0,5))

        # insert enrolled courses records
        def reload_enrollment_table():
            self.search_table('student_course', query='')
        
        reload_enrollment_table()

        # export_btn = ttk.Button(courses_table_frame, text='Export')
        # export_btn.pack(side="right", padx=(10,10), pady=(0,5))

        # ==========================   TRANSACTION TABLE VIEW
        payments_table_frame = ttk.Labelframe(right_stack, text="Transactions")
        payments_table_frame.pack(side="top", fill="both", expand=True, pady=(20,0))
        
        payment_filter_frame = ttk.Frame(payments_table_frame)
        payment_filter_frame.pack(fill="x", pady=(10,5), padx=(10,10))
        paymen_search_entry = ttk.Entry(payment_filter_frame, textvariable=self.pay_search_var)
        paymen_search_entry.pack(side="left", fill="x", expand=True)
        payment_search_btn = ttk.Button(payment_filter_frame, text="Search")
        payment_search_btn.pack(side="left", padx=(10,0))

        self.payments_columns = ['ID', 'Course Name', 'Amount Paid', 'Payment Type', 'Total', 'Transaction Date']
        self.payments_table = ttk.Treeview(payments_table_frame, columns=['ID', 'Course Name' ,'Amount Paid', 'Payment Type', 'Total', 'Transaction Date'], show="headings")
        self.payments_table.heading('ID', text='ID')
        self.payments_table.column('ID', width=30)
        self.payments_table.heading('Course Name', text='Course Name')
        self.payments_table.column('Course Name', width=150)
        self.payments_table.heading('Amount Paid', text='Amount Paid')
        self.payments_table.column('Amount Paid', width=80)
        self.payments_table.heading('Payment Type', text='Payment Type')
        self.payments_table.column('Payment Type', width=120)
        self.payments_table.heading('Total', text='Total')
        self.payments_table.column('Total', width=80)
        self.payments_table.heading('Transaction Date', text='Transaction Date')
        self.payments_table.column('Transaction Date', width=130)
        self.payments_table.pack(fill="both", expand=True, padx=(10,10), pady=(0,10))

        def reload_transaction():
            self.search_table('payments', query='')
        
        reload_transaction()

        search_btn.config(command=lambda: self.search_table('student_course', query=self.search_var.get()))
        payment_search_btn.config(command=lambda: self.search_table('payments', query=self.pay_search_var.get()))
        


    def search_table(self, table_name, query):
        print(query)
        # Get all rows
        # Clear table
        self.clear_table(table_name)
        # Filter and insert matching rows
        if table_name == 'payments':
            columns = [
                "p.id AS ID",
                "sc.course_name AS 'Course Name'",
                "p.amount_paid || ' EGP' AS 'Amount Paid'",
                "p.payment_type AS 'Payment Type'",
                "sc.course_price || ' EGP' AS 'Total'",
                "p.payment_date AS 'Transaction Date'"
            ]
            all_rows = DataController.load_data_with_args(From=['student_course sc', 'students s', 'payments p'], Where=['s.id', 'p.student_course_id', 's.id'], Value=['sc.student_id', 'sc.id', self.student._student_data[self.student._student_columns[0]]], Columns=columns)
            for r in all_rows:
                if any(query.lower() in str(cell).lower() for cell in r):
                    self.payments_table.insert("", "end", values=r)
        elif table_name == 'student_course':
            columns = [
                "c.course_name AS 'Course Name'",

                "c.course_price || ' EGP' AS 'Price'",

                """(SELECT SUM(p.amount_paid)
                FROM payments p
                WHERE p.student_course_id = c.id) || ' EGP' AS Paid""",

                """(c.course_price - IFNULL((
                SELECT SUM(p.amount_paid)
                FROM payments p
                WHERE p.student_course_id = c.id
                ), 0)) || ' EGP' AS Remaining""",

                "c.enrollment_date AS 'Enrolled At'"
            ]
            where = [
                     'c.student_id'
                    ]
            all_rows = DataController.load_data_with_args(From=['student_course c'], Where=where, Value=[self.student._student_data[self.student._student_columns[0]]], Operations=[' = '], Columns=columns)
            for r in all_rows:
                if any(query.lower() in str(cell).lower() for cell in r):
                    self.courses_table.insert("", "end", values=r)
        

    def clear_table(self, table_name):
        if table_name == 'payments':
            for row in self.payments_table.get_children():
                self.payments_table.delete(row)
        elif table_name == 'student_course':
            for row in self.courses_table.get_children():
                self.courses_table.delete(row)
                 

    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

    
