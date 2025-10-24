import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry # type: ignore
from PIL import Image, ImageTk # type: ignore
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Controller'))
from DataModel import Course
import Router.route as _r
from Controller import DataController,PopupHandler
from datetime import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore


class CourseReportView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Window Info
        self.title("Course Report")
        self.geometry("1000x600")

    def load(self):
        # load course report view
        self.courses_data = []

        # Back Button Handling
        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)


        # Initialize Visuals Frame
        self.visuals_frame = ttk.Frame(self)
        self.visuals_frame.pack(fill="both", pady=0, padx=25)

        # ==========================   REPORT VIEW

        # insert enrolled courses records
        def reload_visuals_data():
            self.reload_data()
        
        reload_visuals_data()
        self.visualize()
        

    def reload_data(self):
        # Load courses data with financials
        all_rows = DataController.load_table('courses_report')
        self.courses_data = []
        
        for r in all_rows:
            # Unpack row data
            rec = {}
            rec['Course Name'], rec['Doctor Name'], rec['Course Price'], rec['Start Date'], rec['End Date'], rec['No Enrolled Students'],rec['Total Amount Paid'],rec['Total Remaining'],rec['Total Expected'] = r
            self.courses_data.append(rec)


    def visualize(self):
        # ==========================   VISUALIZATIONS (REPORTS & CHARTS)
        # Clean Data
        courses = np.array([d['Course Name'] for d in self.courses_data])
        enrolled = np.array([d['No Enrolled Students'] for d in self.courses_data])
        paid = np.array([int(d['Total Amount Paid'].split()[0]) for d in self.courses_data])
        remaining = np.array([int(d['Total Remaining'].split()[0]) for d in self.courses_data])
        expected = np.array([int(d['Total Expected'].split()[0]) for d in self.courses_data])

        # Derived metrics
        paid_ratio = np.round((paid / expected) * 100, 1)  # percentage paid
        avg_paid = np.mean(paid)
        avg_expected = np.mean(expected)
        total_revenue = np.sum(paid)
        total_expected = np.sum(expected)

        # --- Helper function to add chart to frame ---
        def add_chart(frame, figure):
            canvas = FigureCanvasTkAgg(figure, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        # --- Create Notebook inside visuals_frame ---
        notebook = ttk.Notebook(self.visuals_frame)
        notebook.pack(fill="both", expand=True)


        # ==========================
        # Chart 1: Students with Remaining Balance
        # ==========================
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Students Remaining")

        search_frame = ttk.Frame(tab1)
        search_frame.pack(fill="x", pady=10, padx=15)

        # Search button and entry
        search_var = tk.StringVar()
        
        search_btn = ttk.Button(search_frame, text="Search")
        search_btn.pack(side="right", padx=(10, 10))
        
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side="right", padx=(0, 5))

        # Table frame
        table_frame = ttk.Frame(tab1)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal")

        # Treeview setup
        columns = ("Student Name", "Barcode", "Course Name", "Remaining Amount")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            height=15
        )

        # Scrollbars configuration
        y_scroll.config(command=tree.yview)
        x_scroll.config(command=tree.xview)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        tree.pack(fill="both", expand=True)

        # Reload table data based on search
        def reload_table():
            query = search_var.get().strip().lower()
            # Clear existing rows
            for row in tree.get_children():
                tree.delete(row)

            # Load only students with remaining amount > 0
            rows = DataController.load_table('students_with_remaining')
            # Filter only those with remaining > 0
            data = [r for r in rows if float(r[3]) > 0]

            # Insert matching rows
            for r in data:
                if any(query.lower() in str(cell).lower() for cell in r):
                    # Format amount neatly with "EGP"
                    formatted = (r[0], r[1], r[2], f"{float(r[3]):,.2f} EGP")
                    tree.insert("", "end", values=formatted)
        
        search_btn.config(command=lambda: reload_table())

        # Populate table
        remaining_rows = DataController.load_table('students_with_remaining')
        for r in remaining_rows:
            # Format amount neatly with "EGP"
            formatted = (r[0], r[1], r[2], f"{float(r[3]):,.2f} EGP")
            tree.insert("", "end", values=formatted)
        
        reload_table()

        # ==========================
        # Chart 2: Detailed Analysis
        # ==========================
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Detailed Analysis")
        self.view_analysis(tab2)

        # ==========================
        # Coming Soon!
        # ==========================
        tabx = ttk.Frame(notebook)
        notebook.add(tabx, text="Graphical Reports")

        # Informative text
        label_coming_soon = ttk.Label(
            tabx,
            text="📊 Graphical reports and visual insights will be added soon!",
            font=("Arial", 14, "bold")
        )
        label_coming_soon.pack(expand=True, pady=50)


    def view_analysis(self, master):
        # ==========================   COURSE ANALYSIS VIEW

        # Text box with scrollbar
        scrollbar = ttk.Scrollbar(master)
        scrollbar.pack(side="right", fill="y")

        text_box = tk.Text(
            master,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 13, "normal"),  # ⬅️ Increased font size
            relief="flat",
            padx=20,   # ⬅️ More padding for better readability
            pady=15,
            spacing1=6,  # ⬅️ Extra space above each line
            spacing2=3,  # ⬅️ Between lines
            spacing3=10  # ⬅️ After a paragraph
        )
        text_box.pack(fill="both", expand=True)

        scrollbar.config(command=text_box.yview)

        # Title
        analysis_lines = [
            "📊  DETAILED COURSE FINANCIAL & PERFORMANCE ANALYSIS\n",
            "══════════════════════════════════════════════════════\n\n"
        ]

        total_students, total_paid, total_expected, total_remaining = [], [], [], []
        total_courses = len(self.courses_data)

        for i, course in enumerate(self.courses_data):
            # Extract data safely
            course_name = course.get("Course Name", f"Course {i+1}")
            doctor_name = course.get("Doctor Name", "Unknown")
            price = float(course.get("Course Price", 0))
            sdate = course.get("Start Date", "N/A")
            edate = course.get("End Date", "N/A")
            enrolled = course.get("No Enrolled Students", 0)
            paid = float(course["Total Amount Paid"].replace(" EGP", ""))
            remaining = float(course["Total Remaining"].replace(" EGP", ""))
            expected = float(course["Total Expected"].replace(" EGP", ""))

            paid_ratio = np.round((paid / expected) * 100, 1) if expected > 0 else 0
            remaining_ratio = np.round((remaining / expected) * 100, 1) if expected > 0 else 0
            avg_payment_per_student = np.round(paid / enrolled, 2) if enrolled else 0

            total_students.append(enrolled)
            total_paid.append(paid)
            total_expected.append(expected)
            total_remaining.append(remaining)

            # === Per-course section ===
            analysis_lines.extend([
                f"🏷️  Course: {course_name}\n",
                f"👨‍⚕️  Doctor: {doctor_name}\n",
                f"💵  Price: {price:,.0f} EGP\n",
                f"🗓️  Duration: {sdate} → {edate}\n",
                f"👥  Enrolled Students: {enrolled}\n",
                f"💰  Expected Revenue: {expected:,.0f} EGP\n",
                f"✅  Paid: {paid:,.0f} EGP  ({paid_ratio}%)\n",
                f"⚠️  Remaining: {remaining:,.0f} EGP  ({remaining_ratio}%)\n",
                f"📈  Avg Payment per Student: {avg_payment_per_student:,.2f} EGP\n",
            ])

            # Interpretive insights
            if paid_ratio >= 90:
                analysis_lines.append("   🔵  Excellent collection — near full payment.\n")
            elif paid_ratio >= 70:
                analysis_lines.append("   🟡  Decent progress — follow-ups may help.\n")
            else:
                analysis_lines.append("   🔴  Low payment completion — needs urgent review.\n")

            if enrolled < 3:
                analysis_lines.append("   ⚠️  Low enrollment — consider stronger marketing.\n")
            elif enrolled > 5:
                analysis_lines.append("   ✅  Strong enrollment and engagement.\n")

            # Duration-based insight
            if sdate != "N/A" and edate != "N/A":
                analysis_lines.append(f"   📅  Duration Insight: From {sdate} to {edate}.\n")
            else:
                analysis_lines.append("   📅  Duration Insight: Dates missing — verify schedule.\n")

            # Price-performance insight
            if price > 0:
                price_efficiency = np.round(paid / price, 1)
                analysis_lines.append(f"   💹  Price-to-Collection Ratio: {price_efficiency}× course price.\n")

            if i<len(self.courses_data)-1:
                analysis_lines.append("\n───────────────────────────────────────────────\n\n")

        # === Overall Statistics ===
        total_paid_sum = sum(total_paid)
        total_expected_sum = sum(total_expected)
        total_remaining_sum = sum(total_remaining)
        total_students_sum = sum(total_students)

        avg_paid_ratio = np.round((total_paid_sum / total_expected_sum) * 100, 1) if total_expected_sum > 0 else 0
        avg_payment_per_student = np.round(total_paid_sum / total_students_sum, 2) if total_students_sum else 0

        analysis_lines.extend([
            "\n\n📈  OVERALL SUMMARY\n",
            "══════════════════════════════════════════════════════\n",
            f"📚  Total Courses Analyzed: {total_courses}\n",
            f"👥  Total Enrolled Students: {total_students_sum}\n",
            f"💰  Total Expected Revenue: {total_expected_sum:,.0f} EGP\n",
            f"✅  Total Collected: {total_paid_sum:,.0f} EGP  ({avg_paid_ratio}%)\n",
            f"⚠️  Total Remaining: {total_remaining_sum:,.0f} EGP\n",
            f"📊  Avg Payment per Student: {avg_payment_per_student:,.2f} EGP\n",
        ])

        if avg_paid_ratio >= 90:
            analysis_lines.append("\n✅  Excellent overall performance — strong consistency.\n")
        elif avg_paid_ratio >= 70:
            analysis_lines.append("\n🟡  Moderate performance — improve collection and engagement.\n")
        else:
            analysis_lines.append("\n🔴  Weak performance — needs strategic attention.\n")

        # Insert and lock
        text_box.insert("1.0", "".join(analysis_lines))
        text_box.config(state="disabled")
    

    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

    
