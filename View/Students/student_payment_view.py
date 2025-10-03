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
from Query import select, insert
import DB
from Controller import DataController


class StudentPaymentView(tk.Toplevel):
    def __init__(self, parent, student: Student):
        super().__init__(parent)

        # Window Info
        self.title("Add Payment")
        self.geometry("1000x600")
        self.student = student

    def load(self):
        student = self.student
        self.entry = {}

        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        left_stack = ttk.Frame(self)
        left_stack.pack(side="left", fill="both", expand=True, pady=(30,50), padx=(25,20))

        right_stack = ttk.Frame(self)
        right_stack.pack(side="right", fill="both", expand=True, pady=(30,50), padx=(10,25))

        profile_frame = ttk.Frame(left_stack)
        profile_frame.pack(side="top", fill="x", anchor="n")

        courses_table_frame = ttk.Labelframe(left_stack, text="Enrolled Courses")
        courses_table_frame.pack(side="top", fill="both", expand=True, pady=(30,0), anchor="n")


        #---------------- Student Profile
        student_card_pfp = tk.Frame(profile_frame)
        student_card_pfp.pack(side="left", fill=None, expand=False, padx=(10,5), anchor="n")
    

        student_card_details_frame = tk.Frame(profile_frame)
        vertical_stack = tk.Frame(student_card_details_frame)

        vertical_stack.pack(side="left", expand=True, fill="x", anchor="n", padx=(15,0))

        student_card_details_frame.pack(side="left", fill="x", expand=True, padx=(10,5), anchor="n")
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
        search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=search_var)
        search_entry.pack(side="left", fill="x", expand=True)
        search_btn = ttk.Button(filter_frame, text="Search")
                                # ,command=lambda t=table_name, sv=search_var: self.search_table(t, sv.get()))
        search_btn.pack(side="left", padx=(10,0))
        
        courses_table = ttk.Treeview(courses_table_frame, columns=['Course Name','Remaining','Date'], show="headings")
        courses_table.heading('Course Name', text='Name')
        courses_table.heading('Remaining', text='Remaining')
        courses_table.heading('Date', text='Enrolled At')
        courses_table.pack(fill="both", expand=True, padx=(10,10), pady=(0,5))

        # insert enrolled courses records
        def reload_enrollment_table():
            courses_table.delete(*courses_table.get_children())
            course_vals = select.select_for_course_payment_table(DB.db(), student._student_data[student._student_columns[0]]).fetchall()
            for record in course_vals:
                courses_table.insert("", "end", values=record)
        
        reload_enrollment_table()

        enroll_new_course_btn = ttk.Button(courses_table_frame, text='Enroll in new course')
        enroll_new_course_btn.pack(side="right", padx=(10,10), pady=(0,5))

        # ==========================   PAYMENT TABLE VIEW
        payment_operation_table = ttk.Labelframe(right_stack, text="Payment Details")
        payment_operation_table.pack(side="top", fill="both", expand=True, pady=(5,0))
        
        payment_operation_elements_frame = ttk.Frame(payment_operation_table)
        payment_operation_elements_frame.pack(fill="both", expand=True)
        payment_operation_elements_frame.grid_columnconfigure(0, weight=1)
        payment_operation_elements_frame.grid_columnconfigure(1, weight=1)

        element_frame = []
        for _ in range(5):
            element_frame.append(ttk.Frame(payment_operation_elements_frame))

        element_frame[0].grid(row=0, column=0, padx=10, pady=(20,0), ipadx=70, sticky="new")
        element_frame[1].grid(row=0, column=1, padx=10, pady=(20,0), ipadx=70, sticky="new")
        element_frame[2].grid(row=1, column=0, padx=10, pady=(30,0), ipadx=70, sticky="new")
        element_frame[3].grid(row=1, column=1, padx=10, pady=(30,0), ipadx=70, sticky="new")
        element_frame[4].grid(row=2, column=0, padx=10, pady=(20,20), ipadx=70, sticky="new")

        label = []
        label.append(ttk.Label(element_frame[0], text='Course name: '))
        label.append(ttk.Label(element_frame[1], text='Remaining amount: '))
        label.append(ttk.Label(element_frame[2], text='Payment type'))
        label.append(ttk.Label(element_frame[3], text='Paid amount'))
        label.append(ttk.Label(element_frame[4], text='Transaction date'))
        for lbl in label:
            lbl.pack(anchor="center", pady=5)

        payment_entries = []
        payment_entries.append(ttk.Labelframe(element_frame[0]))
        payment_entries.append(ttk.Labelframe(element_frame[1]))
        payment_entries.append(ttk.Combobox(element_frame[2], textvariable="Cash", values=["Cash", "Vodafone Cash", "Instapay", "Visa"], state="readonly"))
        payment_entries.append(ttk.Entry(element_frame[3]))
        date_entry = DateEntry(element_frame[4], state="readonly", foreground="white", background="grey", bordercolor="black", headersbackground="white", headersforeground="grey", normalbackground="white", normalforeground="white", weekendbackground="grey", weekendforeground="white", selectbackground="black", selectforeground="yellow")
        payment_entries.append(date_entry)

        for ent in payment_entries:
            ent.pack(fill="x")
        
        self.cname = ttk.Label(payment_entries[0], text="---")
        self.remAmount = ttk.Label(payment_entries[1], text="---")
        self.cname.pack(anchor="center")
        self.remAmount.pack(anchor="center")

        confirm_payment_btn = ttk.Button(payment_operation_table, text="Confirm Payment")
        confirm_payment_btn.pack(anchor="center", pady=10)

        # ==========================   TRANSACTION TABLE VIEW
        payments_table_frame = ttk.Labelframe(right_stack, text="Transactions")
        payments_table_frame.pack(side="bottom", fill="both", expand=True, pady=(20,0))
        
        payment_filter_frame = ttk.Frame(payments_table_frame)
        payment_filter_frame.pack(fill="x", pady=(10,5), padx=(10,10))
        payment_search_var = tk.StringVar()
        paymen_search_entry = ttk.Entry(payment_filter_frame, textvariable=payment_search_var)
        paymen_search_entry.pack(side="left", fill="x", expand=True)
        payment_search_btn = ttk.Button(payment_filter_frame, text="Search")
                                # ,command=lambda t=table_name, sv=payment_search_var: self.search_table(t, sv.get()))
        payment_search_btn.pack(side="left", padx=(10,0))

        payments_table = ttk.Treeview(payments_table_frame, columns=['Course Name' ,'Amount Paid', 'Payment Type', 'Total', 'Transaction Date'], show="headings")
        payments_table.heading('Course Name', text='Course Name')
        payments_table.column('Course Name', width=150)
        payments_table.heading('Amount Paid', text='Amount Paid')
        payments_table.column('Amount Paid', width=80)
        payments_table.heading('Payment Type', text='Payment Type')
        payments_table.column('Payment Type', width=80)
        payments_table.heading('Total', text='Total')
        payments_table.column('Total', width=80)
        payments_table.heading('Transaction Date', text='Transaction Date')
        payments_table.column('Transaction Date', width=130)
        payments_table.pack(fill="both", expand=True, padx=(10,10), pady=(0,10))

        def reload_transaction():
            transaction_vals = select.select_for_student_transactions(DB.db(), student._student_data[student._student_columns[0]]).fetchall()
            payments_table.delete(*payments_table.get_children())
            for record in transaction_vals:
                payments_table.insert("", "end", values=record)
        
        reload_transaction()
        
        payment_operation_table.pack_forget()
        # ==========================   SHOW/HIDE Animation
        def show_payment_operation_table():
            print("SHOW payment_operation_table")
            payment_operation_table.pack(side="top", fill="both", expand=True, pady=(5,0))
        
        def hide_payment_operation_table():
            print("HIDE payment_operation_table")
            payment_operation_table.pack_forget()

        def did_select_course(event):
            update_payment_with_selected(event)

        def update_payment_with_selected(event):
            selected = courses_table.selection()
            if selected:
                course_details = courses_table.item(selected[0], "values")
                show_payment_operation_table()
                self.cname.destroy()
                self.remAmount.destroy()
                self.cname = ttk.Label(payment_entries[0], text=course_details[0])
                self.remAmount = ttk.Label(payment_entries[1], text=course_details[1])
                self.cname.pack(anchor="center")
                self.remAmount.pack(anchor="center")

        def on_course_combobox_selected(event):
            selected_course = self.cname.get()
            course_name_only = selected_course.split(' - ')[0]
            # Do something with selected_course, e.g., update remaining amount, etc.
            print("Selected course:", course_name_only)
            try:
                price_str = selected_course.split('-')[-1].strip()  # e.g., "4000 EGP"
            except Exception:
                price_str = "---"
            self.remAmount.destroy()
            self.remAmount = ttk.Label(payment_entries[1], text=price_str)
            self.remAmount.pack(anchor="center")
            # remove price from course name
            self.cname.set(course_name_only)

        def change_course_to_combobox():
            show_payment_operation_table()
            self.cname.destroy()
            unregistered_courses = select.select_unregistered_courses(DB.db(), student._student_data[student._student_columns[0]]).fetchall()
            unregistered_course_names = [c[0]+" - "+str(c[1])+" EGP" for c in unregistered_courses]
            self.cname = ttk.Combobox(payment_entries[0], textvariable="Course", values=unregistered_course_names, state="readonly")
            self.cname.pack(anchor="center", fill="x")
            self.cname.bind("<<ComboboxSelected>>", on_course_combobox_selected)

        def confirm_payment():
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
            transaction_date = payment_entries[4].get_date()
            self.entry['Transaction Date'] = transaction_date.strftime("%Y-%m-%d")

            # You can now use self.entry to insert the payment into the database or further processing
            print("Payment Entry:", self.entry)
            sID = student._student_data[student._student_columns[0]]
            cName = self.entry['Course Name']
            paid = self.entry['Paid Amount']
            pay_type = self.entry['Payment Type']
            tran_date = self.entry['Transaction Date']
            DataController.confirm_payment(sID, cName, paid, pay_type, tran_date)
            hide_payment_operation_table()
            reload_enrollment_table()
            reload_transaction()

        enroll_new_course_btn.config(command=change_course_to_combobox)
        confirm_payment_btn.config(command=confirm_payment)
        search_btn.config(command=hide_payment_operation_table)
        courses_table.bind("<<TreeviewSelect>>", did_select_course)

    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

    
