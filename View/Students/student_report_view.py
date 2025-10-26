import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry #type: ignore
from PIL import Image, ImageTk  # type: ignore
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Controller'))
from Model.DataModel import Student
import Model.DataArchitecture as DataArch
import Router.route as _r
from Model.Query import select, insert, delete
import Model.DB
from Controller import DataController,PopupHandler
from datetime import datetime

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller extracts files here
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class StudentReportView(tk.Toplevel):
    def __init__(self, parent, student: Student):
        super().__init__(parent)

        # Window Info
        self.title("Student Report")
        self.geometry("1000x600")
        self.student = student

    def load(self):
        # load student payment view
        student = self.student
        # Initialize Entry Objects {element_name: widget}
        self.entry = {}
        self.paymentID = None
        self.entry['Student ID'] = student._student_data[student._student_columns[0]]
        self.entry['Payment ID'] = self.paymentID

        # isEditingTransaction flag
        self.isEditingTransaction = False
        self.paymentID = None

        # Initialize courses and payments entity holders
        self.courses_table = None
        self.payments_table = None

        # Back Button Handling
        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        # Main Stacks
        # Left Stack: Student Profile + Courses Table
        left_stack = ttk.Frame(self)
        left_stack.pack(side="left", fill="both", expand=True, pady=(30,50), padx=(25,20))

        # Right Stack: Payment Details + Transactions Table
        right_stack = ttk.Frame(self)
        right_stack.pack(side="right", fill="both", expand=True, pady=(30,50), padx=(10,25))

        #---------------- Left Stack
        # Student Profile Frame
        profile_frame = ttk.Frame(left_stack)
        profile_frame.pack(side="top", fill="x", anchor="n")

        # Enrolled Courses Frame
        courses_table_frame = ttk.Labelframe(left_stack, text="Enrolled Courses")
        courses_table_frame.pack(side="top", fill="both", expand=True, pady=(30,0), anchor="n")


        #---------------- Student Profile Frame
        student_card_pfp = tk.Frame(profile_frame)
        student_card_pfp.pack(side="left", fill=None, expand=False, padx=(10,5), anchor="n")

        # Student Card Details Frame
        student_card_details_frame = tk.Frame(profile_frame)
        student_card_details_frame.pack(side="left", fill="x", expand=True, padx=(10,5), anchor="n")

        # Vertical Stack for Student Textual Details
        vertical_stack = tk.Frame(student_card_details_frame)
        vertical_stack.pack(side="left", expand=True, fill="x", anchor="n", padx=(15,0))

        # Add picture box (image preview + select button)
        self.entry['Student Image'] = None
        self.img_preview = tk.Label(student_card_pfp, text="No Image", width=20, height=8, bg="#eee", relief="ridge")
        self.img_preview.pack(side="top")

        # Load existing image
        def open_student_image(path):
            try:
                if not path:
                    return None

                # Common image extensions to try
                extensions = ['.png', '.jpg', '.jpeg', '.gif']

                # Try exact path first
                possible_paths = [path]

                # If path has no extension, try all possible ones
                if not os.path.splitext(path)[1]:
                    possible_paths += [path + ext for ext in extensions]

                # Try opening each possible path
                for p in possible_paths:
                    if os.path.exists(p):
                        try:
                            img = Image.open(p)
                            return p
                        except Exception:
                            continue

                print("Error: No valid image found for the given path.")
                return None

            except Exception as e:
                print(f"Error loading student image: {e}")
                return None
            
        if student._student_data['Image']:
            path = student._student_data['Image']
            if path and not os.path.isabs(path):
                # Combine with the folder where images are stored
                path = resource_path(os.path.join("assets", "student_profile", os.path.basename(path)))
                
            # Show image in label
            valid_path = open_student_image(path)
            self.entry['Image'] = valid_path
            if valid_path is not None:
                img = Image.open(valid_path)
                # Calculate new size to ensure min width/height 160
                w, h = img.size
                scale = max(160/w, 160/h)
                new_w, new_h = int(w*scale), int(h*scale)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                # Center crop to 160x160 if needed
                if new_w > 160 or new_h > 160:
                    left = (new_w - 160) // 2
                    top = (new_h - 160) // 2
                    img = img.crop((left, top, left+160, top+160))
                self.img_tk = ImageTk.PhotoImage(img)
                self.img_preview.config(image=self.img_tk, text="", width=160, height=160)
        

        #--------------- Student Details
        # student details labels
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
        # Search bar
        filter_frame = ttk.Frame(courses_table_frame)
        filter_frame.pack(fill="x", pady=(10,5), padx=(10,10))

        search_var = tk.StringVar()

        search_entry = ttk.Entry(filter_frame, textvariable=search_var)
        search_entry.pack(side="left", fill="x", expand=True)

        search_btn = ttk.Button(filter_frame, text="Search"
                                 ,command=lambda t='student_course_all', sv=search_var: self.search_table(t, sv.get()))
        search_btn.pack(side="left", padx=(10,0))

        self.course_columns = ['Course Name', 'Price', 'Paid', 'Remaining', 'Date']
        # Courses Table
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

        # load enrolled courses records
        def reload_enrollment_table():
            self.search_table('student_course_all')
        
        reload_enrollment_table()

        # ==========================   TRANSACTION TABLE VIEW
        payments_table_frame = ttk.Labelframe(right_stack, text="Transactions")
        payments_table_frame.pack(side="bottom", fill="both", expand=True, pady=(20,0))

        # Payment Search Bar
        payment_filter_frame = ttk.Frame(payments_table_frame)
        payment_filter_frame.pack(fill="x", pady=(10,5), padx=(10,10))

        payment_search_var = tk.StringVar()

        payment_search_entry = ttk.Entry(payment_filter_frame, textvariable=payment_search_var)
        payment_search_entry.pack(side="left", fill="x", expand=True)

        payment_search_btn = ttk.Button(payment_filter_frame, text="Search"
                                 ,command=lambda t='payments', sv=payment_search_var: self.search_table(t, sv.get()))
        payment_search_btn.pack(side="left", padx=(10,0))

        
        self.payments_columns = ['ID', 'Course Name', 'Amount Paid', 'Payment Type', 'Total', 'Transaction Date']
        # Payments Table
        self.payments_table = ttk.Treeview(payments_table_frame, columns=self.payments_columns, show="headings")
        # Custom column widths
        self.payments_table.heading('ID', text='ID')
        self.payments_table.column('ID', width=30)
        self.payments_table.heading('Course Name', text='Course Name')
        self.payments_table.column('Course Name', width=150)
        self.payments_table.heading('Amount Paid', text='Amount Paid')
        self.payments_table.column('Amount Paid', width=80)
        self.payments_table.heading('Payment Type', text='Payment Type')
        self.payments_table.column('Payment Type', width=80)
        self.payments_table.heading('Total', text='Total')
        self.payments_table.column('Total', width=80)
        self.payments_table.heading('Transaction Date', text='Transaction Date')
        self.payments_table.column('Transaction Date', width=130)

        self.payments_table.pack(fill="both", expand=True, padx=(10,10), pady=(0,10))

        # load payments records
        def reload_transaction():
            self.search_table('payments')
        
        reload_transaction()

    # ==========================   TABLE SEARCH HANDLING
    def search_table(self, table_name, query=''):
        # Clear table
        self.clear_table(table_name)

        # Load all rows from the specified table
        all_rows = DataController.load_table(table_name, self.entry)

        # Filter and insert matching rows
        if table_name == 'payments':
            for r in all_rows:
                # Check if any cell in the row matches the query
                if any(query.lower() in str(cell).lower() for cell in r):
                    self.payments_table.insert("", "end", values=r)
        elif table_name == 'student_course_all':
            for r in all_rows:
                # Check if any cell in the row matches the query
                if any(query.lower() in str(cell).lower() for cell in r):
                    self.courses_table.insert("", "end", values=r)
        

    def clear_table(self, table_name):
        if table_name == 'payments':
            # Clear payments table
            for row in self.payments_table.get_children():
                self.payments_table.delete(row)
        elif table_name == 'student_course_all':
            # Clear courses table
            for row in self.courses_table.get_children():
                self.courses_table.delete(row)
                 

    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

    
