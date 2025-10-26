import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk #type: ignore
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Controller'))
from Model.DataModel import Student
import Model.DataArchitecture as DataArch
import Router.route as _r
from Model.Query import select, insert, delete
import Model.DB as DB
from Controller import DataController,PopupHandler
from datetime import datetime
from lib.DateModule import DatePicker

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller extracts files here
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class StudentPaymentView(tk.Toplevel):
    def __init__(self, parent, student: Student):
        super().__init__(parent)

        # Window Info
        self.title("Add Payment")
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

        # Registered Courses with Installments Frame
        courses_table_frame = ttk.Labelframe(left_stack, text="Registered with Installments")
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
                                 ,command=lambda t='student_course', sv=search_var: self.search_table(t, sv.get()))
        search_btn.pack(side="left", padx=(10,0))

        self.course_columns = ['Course Name', 'Remaining', 'Date']
        # Registered Courses with Installments Table
        self.courses_table = ttk.Treeview(courses_table_frame, columns=self.course_columns, show="headings")
        for col in self.course_columns:
            self.courses_table.heading(col, text=col)
        self.courses_table.pack(fill="both", expand=True, padx=(10,10), pady=(0,5))

        # load registered courses with installments records
        def reload_enrollment_table():
            self.search_table('student_course')
        
        reload_enrollment_table()

        # Enroll in new course button
        enroll_new_course_btn = ttk.Button(courses_table_frame, text='Enroll in new course')
        enroll_new_course_btn.pack(side="right", padx=(10,10), pady=(0,5))


        # ==========================   PAYMENT TABLE VIEW
        # Payment details for selected course
        payment_operation_table = ttk.Labelframe(right_stack, text="Payment Details")
        payment_operation_table.pack(side="top", fill="both", expand=True, pady=(5,0))
        
        payment_operation_elements_frame = ttk.Frame(payment_operation_table)
        payment_operation_elements_frame.pack(fill="both", expand=True)
        payment_operation_elements_frame.grid_columnconfigure(0, weight=1)
        payment_operation_elements_frame.grid_columnconfigure(1, weight=1)

        # Create element frames (entry objects holders)
        element_frame = []
        for _ in range(5):
            element_frame.append(ttk.Frame(payment_operation_elements_frame))

        element_frame[0].grid(row=0, column=0, padx=10, pady=(20,0), ipadx=70, sticky="new")
        element_frame[1].grid(row=0, column=1, padx=10, pady=(20,0), ipadx=70, sticky="new")
        element_frame[2].grid(row=1, column=0, padx=10, pady=(30,0), ipadx=70, sticky="new")
        element_frame[3].grid(row=1, column=1, padx=10, pady=(30,0), ipadx=70, sticky="new")
        element_frame[4].grid(row=2, column=0, padx=10, pady=(20,20), ipadx=70, sticky="new")

        # Create labels for each entry
        label = []
        label.append(ttk.Label(element_frame[0], text='Course name: '))
        label.append(ttk.Label(element_frame[1], text='Remaining amount: '))
        label.append(ttk.Label(element_frame[2], text='Payment type'))
        label.append(ttk.Label(element_frame[3], text='Paid amount'))
        label.append(ttk.Label(element_frame[4], text='Transaction date'))
        for lbl in label:
            lbl.pack(anchor="center", pady=5)

        # Create entry widgets for each element
        payment_entries = []
        payment_entries.append(ttk.Labelframe(element_frame[0]))
        payment_entries.append(ttk.Labelframe(element_frame[1]))
        payment_entries.append(ttk.Combobox(element_frame[2], textvariable="Cash", values=["Cash", "Vodafone Cash", "Instapay", "Visa"], state="readonly"))
        payment_entries.append(ttk.Entry(element_frame[3]))

        # Custom DatePicker instead of DateEntry
        init_date = None
        try:
            # Default to today's date
            init_date = datetime.today().date()
        except Exception:
            init_date = None

        # Create DatePicker for transaction date
        datepicker = DatePicker(
            element_frame[4],
            date_pattern="yyyy-mm-dd",
            initial_date=init_date
        )

        payment_entries.append(datepicker)

        # resize and pack entries
        for ent in payment_entries:
            ent.pack(fill="x")
        
        # Initialize course name label
        self.cname = ttk.Label(payment_entries[0], text="---")
        self.cname.pack(anchor="center")
        # Initialize remaining amount label
        self.remAmount = ttk.Label(payment_entries[1], text="---")
        self.remAmount.pack(anchor="center")

        # Action Buttons Frame
        btn_frame = ttk.Frame(payment_operation_table)
        btn_frame.pack(anchor="center", pady=10)


        delete_trns_btn = tk.Button(
            btn_frame,
            text="Delete",
            fg='red'
        )
        confirm_payment_btn = ttk.Button(btn_frame, text="Confirm Payment")
        confirm_payment_btn.grid(row=0, column=1, sticky="w")


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
        
        # Initially hide payment operation table
        payment_operation_table.pack_forget()

        # ==========================   SHOW/HIDE Animation
        # Functions to show/hide payment operation table
        def show_payment_operation_table():
            payment_operation_table.pack(side="top", fill="both", expand=True, pady=(5,0))
        
        def hide_payment_operation_table():
            payment_operation_table.pack_forget()

        # ==========================   SHOW/HIDE DELETE BUTTON & CONFIRM/EDIT ACTIONS
        def show_delete():
            if not self.isEditingTransaction:
                delete_trns_btn.grid(row=0, column=0, sticky="w")
            confirm_payment_btn.config(text="Save Changes", command=lambda ac="update":on_confirm_payment(ac))
            self.isEditingTransaction = True
        
        def hide_delete():
            if self.isEditingTransaction: 
                delete_trns_btn.grid_forget()
            confirm_payment_btn.config(text="Confirm Payment", command=lambda ac="confirm":on_confirm_payment(ac))
            self.isEditingTransaction = False

        # ==========================   TABLE SELECTION HANDLING
        def did_select_course(event):
            hide_delete()
            def update_payment_with_selected_course(event):
                selected = self.courses_table.selection()
                if selected:
                    # Get course details
                    course_details = self.courses_table.item(selected[0], "values")
                    # Update payment operation table with course details
                    show_payment_operation_table()
                    # Update labels
                    self.cname.destroy()
                    self.remAmount.destroy()
                    self.cname = ttk.Label(payment_entries[0], text=course_details[0])
                    self.remAmount = ttk.Label(payment_entries[1], text=course_details[1])
                    self.cname.pack(anchor="center")
                    self.remAmount.pack(anchor="center")
                    # Reset other payment entries
                    payment_entries[2].set("")
                    payment_entries[3].delete(0, tk.END)

                    # --- Replace date with custom DatePicker ---
                    date_str = datetime.today().date().strftime("%Y-%m-%d")
                    try:
                        init_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    except Exception:
                        init_date = None

                    # Destroy old date entry if exists
                    try:
                        payment_entries[4].destroy()
                    except Exception:
                        pass

                    # Create custom DatePicker instead of DateEntry
                    payment_entries[4] = DatePicker(payment_entries[4].master, date_pattern="yyyy-mm-dd", initial_date=init_date)
                    payment_entries[4].pack(anchor="center")

            update_payment_with_selected_course(event)

        def did_select_payment(event):
            # Enter Edit Mode
            show_delete()
            selected = self.payments_table.selection()
            if selected:
                # Get Transaction Details
                payment_details = self.payments_table.item(selected[0], "values")
                self.paymentID = payment_details[0]
                
                show_payment_operation_table()
                
                # Update payment operation table with payment details
                self.cname.destroy()
                self.remAmount.destroy()

                # Update labels
                self.cname = ttk.Label(payment_entries[0], text=payment_details[1])
                self.remAmount = ttk.Label(payment_entries[1], text="---")

                # Update payment method and amount
                payment_entries[2].set(payment_details[3])
                payment_entries[3].delete(0, tk.END)
                payment_entries[3].insert(0, payment_details[2].split()[0])

                # --- Replace date with custom DatePicker ---
                date_str = payment_details[5]
                try:
                    init_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except Exception:
                    init_date = None

                # Destroy old date entry if exists
                try:
                    payment_entries[4].destroy()
                except Exception:
                    pass

                # Create custom DatePicker instead of DateEntry
                payment_entries[4] = DatePicker(payment_entries[4].master, date_pattern="yyyy-mm-dd", initial_date=init_date)
                payment_entries[4].pack(anchor="center")

                # Repack labels
                self.cname.pack(anchor="center")
                self.remAmount.pack(anchor="center")

        self.courses_table.bind("<<TreeviewSelect>>", did_select_course)
        self.payments_table.bind("<<TreeviewSelect>>", did_select_payment)

        # ==========================   COMBOBOX HANDLING

        def on_course_combobox_selected(event):
            selected_course = self.cname.get()
            course_name_only = selected_course.split(' - ')[0]
            # Do something with selected_course, e.g., update remaining amount, etc.
            try:
                price_str = selected_course.split('-')[-1].strip()  # e.g., "4000 EGP"
            except Exception:
                price_str = "---"

            # Update remaining amount label
            self.remAmount.destroy()
            self.remAmount = ttk.Label(payment_entries[1], text=price_str)
            self.remAmount.pack(anchor="center")

            # remove price from course name
            self.cname.set(course_name_only)

        # Change course name label to combobox for enrolling in new course
        def change_course_to_combobox():
            hide_delete()
            show_payment_operation_table()
            
            self.cname.destroy()
            
            # Get unregistered courses for the student
            # ==============================================DATABASE QUERY HERE==============================================
            unregistered_courses = DataController.select_unregistered_courses(student._student_data[student._student_columns[0]])
            
            # Format course names with prices e.g., "Course A - 4000 EGP"
            unregistered_course_names = [c[0]+" - "+str(c[1])+" EGP" for c in unregistered_courses]
            
            # Update course name to combobox
            self.cname = ttk.Combobox(payment_entries[0], textvariable="Course", values=unregistered_course_names, state="readonly")
            self.cname.pack(anchor="center", fill="x")

            # on selection update remaining amount
            self.cname.bind("<<ComboboxSelected>>", on_course_combobox_selected)
            
        # Enroll Button Action
        enroll_new_course_btn.config(command=change_course_to_combobox)
        

        # ==========================   BUTTON ACTIONS (CONFIRM/EDIT)

        def set_entry_data():
            # Get selected course name from the combobox or label
            if isinstance(self.cname, ttk.Combobox):
                course_name = self.cname.get().split(' - ')[0]
            else:
                course_name = self.cname.cget("text")
            self.entry['Course Name'] = course_name

            # Get remaining amount from the label
            if isinstance(self.remAmount, ttk.Label):
                remaining_amount = self.remAmount.cget("text")
            else:
                remaining_amount = "---"
            self.entry['Remaining Amount'] = remaining_amount[:-4]

            # Get payment type from combobox
            payment_type = payment_entries[2].get()
            self.entry['Payment Type'] = payment_type

            # Get paid amount from entry
            paid_amount = payment_entries[3].get()
            self.entry['Paid Amount'] = paid_amount

            # Get transaction date from DateEntry
            try:
                date_text = payment_entries[4].entry.get().strip()
                if date_text:
                    transaction_date = datetime.strptime(date_text, "%Y-%m-%d").date()
                    self.entry['Transaction Date'] = transaction_date.strftime("%Y-%m-%d")
                else:
                    # No date selected
                    self.entry['Transaction Date'] = datetime.today().strftime("%Y-%m-%d")
            except Exception:
                # In case the calendar was closed without a date or widget got destroyed
                self.entry['Transaction Date'] = datetime.today().strftime("%Y-%m-%d")

        def on_confirm_payment(action="confirm"):
            # Set entry data from widgets
            set_entry_data()
            self.entry['Payment ID'] = self.paymentID
            # Confirm or update payment
            if action == "confirm":
                if not DataController.func_payment(func=DataController.confirm_payment,entry=self.entry):
                    return
            elif action == "update":
                if not DataController.func_payment(func=DataController.update_payment,entry=self.entry):
                    return

            # After successful operation, reset values and hide payment operation table
            hide_payment_operation_table()
            reload_data()

        def on_delete_transaction():
            if DataController.delete_payment(window=self, paymentID=self.paymentID):
                reload_data()

        delete_trns_btn.config(command=on_delete_transaction)

        def reload_data():
            reload_enrollment_table()
            reload_transaction()
            reset_values()

        def reset_values():
            for key in self.entry:
                if key != 'Student ID' and key != 'Payment ID':
                    self.entry[key] = ''

            if isinstance(self.cname, ttk.Label):
                self.cname.config(text="")
            elif isinstance(self.cname, ttk.Combobox):
                self.cname.set('')
            
            self.remAmount.config(text="---")
            payment_entries[2].set('')
            payment_entries[3].delete(0, tk.END)
            payment_entries[4]._set_date(datetime.now())

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
        elif table_name == 'student_course':
            for r in all_rows:
                # Check if any cell in the row matches the query
                if any(query.lower() in str(cell).lower() for cell in r):
                    self.courses_table.insert("", "end", values=r)
        

    def clear_table(self, table_name):
        if table_name == 'payments':
            # Clear payments table
            for row in self.payments_table.get_children():
                self.payments_table.delete(row)
        elif table_name == 'student_course':
            # Clear courses table
            for row in self.courses_table.get_children():
                self.courses_table.delete(row)
                 

    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

    
