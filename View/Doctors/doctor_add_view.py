import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk #type: ignore
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
from Controller import DataController
import Model.DataArchitecture as DataArch
import Router.route as _r

class DoctorAddView(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        # Window Info
        self.title("Create New Doctor")
        self.geometry("1000x600")
        
    def load(self):
        # load doctor add view
        # Initialize UI Element holders and Placeholders
        elements = DataArch.add_doctor_elements
        placeholder = DataArch.add_doctor_elements_placeholders
        # Initialize Entry Objects {element_name: widget}
        self.entry = {}
        self.data = {}
        self.data['ID'] = None

        # Back Button Handling
        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        # Initialize Doctor Card (Main) Frame
        doctor_card = ttk.Frame(self)
        doctor_card.pack(expand=True, fill="both", anchor="center")

        #---------------- Doctor Card
        # Create vertical stack inside doctor card
        vertical_stack = tk.Frame(doctor_card)
        vertical_stack.pack(expand=True, fill="both", anchor="center")
        vertical_stack.place(relx=.5, rely=.5, anchor="c")

        # Add Fields Frame
        fields_frame = ttk.Labelframe(vertical_stack, text="Doctor Info")
        fields_frame.pack(pady=0, anchor="center")
        
        #--------------- Create New Doctor
        # Loop through elements to create labels and entry widgets
        for r, row in enumerate(elements):
            # Each row can have multiple columns
            for c,col in enumerate(row):
                # Create a label for each field
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
                        # Create a StringVar to hold the selected option
                        radio_var = tk.StringVar()
                        radio_var.set(options[0])
                        # Create radio buttons based on options
                        for i, option in enumerate(options):
                            self.entry[option] = ttk.Radiobutton(radio_frame, text=option, variable=radio_var, value=option)
                            self.entry[option].grid(row=0, column=i, padx=20)
                        # Store the StringVar in the entry dictionary
                        self.entry[label_text] = radio_var
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

        def on_create_doctor():
            if DataController.func_doctor(func=DataController.add_new_doctor, 
                                          data=self.data, 
                                          entry=self.entry, 
                                          placeholder=placeholder):
                back_btn_pressed()
        
        create_btn = ttk.Button(vertical_stack, text="Create",
                               command=on_create_doctor)
        create_btn.pack(side="top", pady=25, anchor="center")
    
    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode
