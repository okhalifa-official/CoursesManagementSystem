import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk # type: ignore
from datetime import datetime
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
import DataArchitecture as DataArch
import Router.route as _r
from Controller import DataController
from lib.DateModule import DatePicker


class CourseAddView(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        # Window Info
        self.title("Create New Course")
        self.geometry("1000x600")
        
    def load(self):
        # load course add view
        elements = DataArch.add_course_elements
        # get doctors names and ids for combo box
        doctors_name, doctors_id = DataController.get_doctors_names_id()
        placeholder = DataArch.add_course_elements_placeholders
        self.entry = {}
        self.data = {}
        self.data['ID'] = None

        # Back Button Handling
        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        # Create Course Card (Main) Frame
        course_card = ttk.Frame(self)
        course_card.pack(expand=True, fill="both", anchor="center")
        course_card.place(relx=.5, rely=.5, anchor="c")

        #---------------- Course Card
        # Add left stack to Course Card (Main Frame)
        left_vertical_stack = tk.Frame(course_card)
        left_vertical_stack.pack(pady=20, side="left", fill="both", expand=True, anchor="w")

        # Add picture box (image preview + select button)
        self.entry['Course Image'] = None
        self.img_preview = tk.Label(left_vertical_stack, text="No Image", width=30, bg="#eee", relief="ridge")
        self.img_preview.pack(fill="both", expand=True)

        def select_image():
            path = filedialog.askopenfilename(filetypes=[("Image Files", ["*.png","*.jpg","*.jpeg","*.gif"])])
            if path:
                self.entry['Image'] = path
                # Show image in label
                img = Image.open(path)
                # Calculate new size to ensure min width/height 160
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

        # Add right stack to Course Card (Main Frame)
        right_vertical_stack = ttk.Frame(course_card)
        right_vertical_stack.pack(side="right", fill="both", expand=True, padx=(20,0), anchor="n")
        # Add frame for fields
        fields_frame = ttk.Labelframe(right_vertical_stack, text="")
        fields_frame.pack(side="top", fill="both", expand=True)
        
        #--------------- Create New Course
        # loop on all rows of elements
        for r, row in enumerate(elements):
            # loop through fields in each row
            for c,col in enumerate(row):
                # label text for entity
                label_text = list(col.keys())[0]
                label = ttk.Label(fields_frame, text=f"{label_text}")
                label.grid(row=r, column=0, pady=15, padx=30, sticky="w")
                
                # Create corresponding entry widget based on type
                values = list(col.values())
                if type(values[0]).__name__ == 'list':
                    # list of options (e.g., for radio buttons)
                    values = values[0]

                # Determine widget type
                val = values[0]
                match val:
                    case 'radio':
                        radio_frame = ttk.Frame(fields_frame)
                        radio_frame.grid(row=r, column=1)
                        # Create radio buttons for each option
                        options = values[1:]
                        radio_var = tk.StringVar()
                        for i, option in enumerate(options):
                            self.entry[option] = ttk.Radiobutton(radio_frame, text=option, variable=radio_var, value=option)
                            self.entry[option].grid(row=0, column=i, padx=20)
                        
                        # set default value for radio button
                        radio_var.set(options[0])
                        self.entry[label_text] = radio_var
                    case 'combo_box':
                        entry_widget = ttk.Combobox(fields_frame, textvariable=placeholder[label_text], values=doctors_name, state="readonly")
                        entry_widget.grid(row=r, column=1, padx=20)
                        self.entry[label_text] = entry_widget
                    case 'date':
                        # Use custom DatePicker (Entry + Calendar) to avoid DateEntry freeze issues
                        init_date = None

                        datepicker = DatePicker(fields_frame, date_pattern="yyyy-mm-dd", initial_date=init_date)
                        datepicker.grid(row=r, column=1, padx=20, sticky="w")
                        self.entry[label_text] = datepicker
                    case _:
                        entry_widget = ttk.Entry(fields_frame)
                        entry_widget.grid(row=r, column=1, padx=20)
                        # placeholder handling
                        entry_widget.insert(0, placeholder[label_text])
                        entry_widget.config(foreground="grey")
                        # Placeholder focus in/out events
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

        def on_create_course():
            if DataController.func_course(DataController.add_new_course, 
                                          self.entry, 
                                          self.data, 
                                          placeholder):
                back_btn_pressed()
        
        create_btn = ttk.Button(right_vertical_stack, text="Create",
                    command=on_create_course)
        create_btn.pack(fill="x", pady=25, side="bottom")
    
    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

        

#cav = CourseAddView()
# cav.mainloop()
