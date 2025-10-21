import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
from DataModel import Course
from Controller import DataController, PopupHandler
import DataArchitecture as DataArch
import Router.route as _r
from Controller.Validation import Validation

from lib.DateModule import DatePicker

def show_error(message: str):
    messagebox.showerror(
            "Invalid Entry",
            message
    )

def validate_data(data: dict) -> bool:
    # Example validation: Ensure required fields are filled
    message = ""
    if (message := Validation.is_valid_course_name(data['name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_doctor_name(data['doctor_name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_payment_amount(data['price'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_start_date(data['start_date'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_end_date(data['end_date'])) != True:
        show_error(message)
        return False
    return True


class CourseEditView(tk.Toplevel):
    def __init__(self,parent, course: Course):
        super().__init__(parent)

        # Window Info
        self.title("Edit Course")
        self.geometry("1000x600")
        self.course = course
        
    def load(self):
        course = self.course
        elements = DataArch.add_course_elements
        doctors_name, doctors_id = DataController.get_doctors_names_id()
        placeholder = DataArch.add_course_elements_placeholders
        self.entry = {}
        self.data = {}
        style = ttk.Style()

        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        course_card = ttk.Frame(self)
        course_card.pack(expand=True, fill="both", anchor="center")
        course_card.place(relx=.5, rely=.5, anchor="c")

        #---------------- Course Card
        left_vertical_stack = tk.Frame(course_card)
        left_vertical_stack.pack(pady=20, side="left", fill="both", expand=True, anchor="w")

        # Add picture box (image preview + select button)
        self.entry['Course Image'] = None
        self.img_preview = tk.Label(left_vertical_stack, text="No Image", width=30, bg="#eee", relief="ridge")
        self.img_preview.pack(fill="both", expand=True)

        # Load existing image
        if course._course_data['Image']:
            path = course._course_data['Image']
            # Show image in label
            img = Image.open(path)
            # Calculate new size to ensure min width/height 270
            w, h = img.size
            scale = max(270/w, 270/h)
            new_w, new_h = int(w*scale), int(h*scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            # Center crop to 160x160 if needed
            if new_w > 270 or new_h > 270:
                left = (new_w - 270) // 2
                top = (new_h - 270) // 2
                img = img.crop((left, top, left+270, top+270))
            self.img_tk = ImageTk.PhotoImage(img)
            self.img_preview.config(image=self.img_tk, text="", width=270, height=270)

        def select_image():
            path = filedialog.askopenfilename(filetypes=[("Image Files", ["*.png","*.jpg","*.jpeg","*.gif"])])
            if path:
                self.entry['Image'] = path
                # Show image in label
                img = Image.open(path)
                # Calculate new size to ensure min width/height 270
                w, h = img.size
                scale = max(270/w, 270/h)
                new_w, new_h = int(w*scale), int(h*scale)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                # Center crop to 160x160 if needed
                if new_w > 270 or new_h > 270:
                    left = (new_w - 270) // 2
                    top = (new_h - 270) // 2
                    img = img.crop((left, top, left+270, top+270))
                self.img_tk = ImageTk.PhotoImage(img)
                self.img_preview.config(image=self.img_tk, text="", width=270, height=270)
                print(f"image updated {path}")
        img_btn = ttk.Button(left_vertical_stack, text="Select Image", command=select_image, width=10)
        img_btn.pack(fill="x", pady=(20,5), anchor="center")

        right_vertical_stack = ttk.Frame(course_card)
        right_vertical_stack.pack(side="right", fill="both", expand=True, padx=(20,0), anchor="n")
        fields_frame = ttk.Labelframe(right_vertical_stack, text="")
        fields_frame.pack(side="top", fill="both", expand=True)
        
        #--------------- Create New Course
        for r, row in enumerate(elements):
            for c,col in enumerate(row):
                # fields_frame.grid_rowconfigure(r, weight=1)

                label_text = list(col.keys())[0]
                label = ttk.Label(fields_frame, text=f"{label_text}")
                label.grid(row=r, column=0, pady=15, padx=30, sticky="w")
                
                values = list(col.values())
                if type(values[0]).__name__ == 'list':
                    values = values[0]
                val = values[0]
                match val:
                    case 'radio':
                        radio_frame = ttk.Frame(fields_frame)
                        radio_frame.grid(row=r, column=1)
                        options = values[1:]
                        radio_var = tk.StringVar()
                        if course._course_data[label_text]:
                            radio_var.set(course._course_data[label_text])
                        else:
                            radio_var.set(options[0])
                        for i, option in enumerate(options):
                            self.entry[option] = ttk.Radiobutton(radio_frame, text=option, variable=radio_var, value=option)
                            self.entry[option].grid(row=0, column=i, padx=20)
                        self.entry[label_text] = radio_var
                    case 'combo_box':
                        entry_widget = ttk.Combobox(fields_frame, textvariable=placeholder[label_text], values=doctors_name, state="readonly")
                        entry_widget.grid(row=r, column=1, padx=20)
                        # Find the index of the doctor ID and set the corresponding name
                        doctor_id = course._course_data[label_text]
                        if doctor_id in doctors_id:
                            idx = doctors_id.index(doctor_id)
                            entry_widget.set(doctors_name[idx])
                        else:
                            entry_widget.set(doctor_id)  # a default value
                        self.entry[label_text] = entry_widget
                    case 'date':
                        # Use custom DatePicker (Entry + Calendar) to avoid DateEntry freeze issues
                        init_date = None
                        try:
                            init_date = datetime.strptime(course._course_data[label_text], "%Y-%m-%d").date()
                        except Exception:
                            init_date = None

                        datepicker = DatePicker(fields_frame, date_pattern="yyyy-mm-dd", initial_date=init_date)
                        datepicker.grid(row=r, column=1, padx=20, sticky="w")
                        self.entry[label_text] = datepicker
                    case _:
                        entry_widget = ttk.Entry(fields_frame)
                        if course._course_data[label_text]:
                            entry_widget.insert(0, course._course_data[label_text])
                            entry_widget.config(foreground="")
                        else:
                            entry_widget.insert(0, placeholder[label_text]) # placeholder
                            entry_widget.config(foreground="grey")
                        entry_widget.grid(row=r, column=1, padx=20)

                        # Placeholder function setup
                        def on_focus_in(event, e=entry_widget, ph=placeholder[label_text]):
                            if e.get() == ph:
                                e.delete(0, tk.END)
                                e.config(foreground="")
                        def on_focus_out(event, e=entry_widget, ph=placeholder[label_text]):
                            if e.get() == "":
                                e.insert(0, ph)
                                e.config(foreground="grey")
                        entry_widget.bind("<FocusIn>", on_focus_in)
                        entry_widget.bind("<FocusOut>", on_focus_out)
                        self.entry[label_text] = entry_widget
                #print(values)

        def update_course():
            # print("hello world")
            # store all new course data in self.data{}
            for key, widget in self.entry.items():
                # DatePicker (custom)
                if hasattr(widget, "entry") and isinstance(getattr(widget, "entry"), ttk.Entry):
                    # e.g. DatePicker: .entry is the underlying entry widget
                    value = widget.entry.get().strip()
                elif isinstance(widget, tk.StringVar):
                    value = widget.get()
                elif isinstance(widget, ttk.Entry):
                    value = widget.get()
                elif isinstance(widget, ttk.Combobox):
                    value = widget.get()
                else:
                    # fallback: whatever the widget is (e.g., radiobutton group stringvar earlier)
                    try:
                        value = widget.get()
                    except Exception:
                        value = widget

                # store
                self.data[key] = None
                try:
                    if value != placeholder[key]:
                        self.data[key] = value
                except KeyError:
                    self.data[key] = value
            
            if validate_data(self.data):
                if DataController.update_course(
                    id=self.course._course_data[self.course._course_columns[0]],
                    name=self.data['name'],
                    doc_name=self.data['doctor_name'],
                    price=self.data['price'],
                    s_date=self.data['start_date'],
                    e_date=self.data['end_date']
                ):
                    back_btn_pressed()
            
        def delete_course():
            # show confirmation pop_up
            message = "Are you sure you want to delete this course?"
            confirmation_text = "Delete"
            result = PopupHandler.confirmation_popup(self, title="Delete Course", message=message, button1_text="Cancel", button2_text=confirmation_text)
            if result:
                print("delete")
                if DataController.delete_course(
                    id=self.course._course_data[self.course._course_columns[0]]
                ):
                    back_btn_pressed()
            else:
                print("canceled")
        
        btn_frame = ttk.Frame(right_vertical_stack)
        btn_frame.pack(fill="x", pady=25, side="bottom", anchor="center")

        delete_btn = tk.Button(
            btn_frame,
            text="Delete",
            fg='red',
            command=delete_course
        )
        delete_btn.grid(row=0, column=0, sticky="w")

        create_btn = ttk.Button(btn_frame, text="Save Changes",
                    command=update_course)
        create_btn.grid(row=0, column=1, padx=30, sticky="e")
    
    def view(self):
        self.lift()
        self.after(200, lambda: self.focus_force())  # delayed focus fix
        self.state('zoomed')

        

#cav = CourseAddView()
# cav.mainloop()
