import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
import DataArchitecture as DataArch
import Router.route as _r


class DoctorAddView(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        # Window Info
        self.title("Create New Doctor")
        self.geometry("1000x600")
        
    def load(self):
        elements = DataArch.add_doctor_elements
        placeholder = DataArch.add_doctor_elements_placeholders
        self.entry = {}
        self.data = {}

        def back_btn_pressed():
            _r.route_back(self)
            print("Hello")

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        doctor_card = ttk.Frame(self)
        doctor_card.pack(expand=True, fill="both", anchor="center")
        # doctor_card.place(relx=.5, rely=.5, anchor="c")

        #---------------- Doctor Card
        vertical_stack = tk.Frame(doctor_card)
        vertical_stack.pack(expand=True, fill="both", anchor="center")
        vertical_stack.place(relx=.5, rely=.5, anchor="c")

        fields_frame = ttk.Labelframe(vertical_stack, text="Doctor Info")
        fields_frame.pack(pady=0, anchor="center")
        
        #--------------- Create New Doctor
        for r, row in enumerate(elements):
            for c,col in enumerate(row):

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
                        radio_var.set(options[0])
                        for i, option in enumerate(options):
                            self.entry[option] = ttk.Radiobutton(radio_frame, text=option, variable=radio_var, value=option)
                            self.entry[option].grid(row=0, column=i, padx=20)
                        self.entry[label_text] = radio_var
                    case _:
                        entry_widget = ttk.Entry(fields_frame)
                        entry_widget.insert(0, placeholder[label_text]) # placeholder
                        entry_widget.grid(row=r, column=1, padx=20)
                        entry_widget.config(foreground="grey")
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

        def create_doctor():
            # store all new doctor data in self.data{}
            for key, widget in self.entry.items():
                # Handle different widget types
                if isinstance(widget, ttk.Entry):
                    value = widget.get()
                elif isinstance(widget, tk.StringVar):
                    value = widget.get()
                elif isinstance(widget, ttk.Radiobutton):
                    # For radiobuttons, get the value from the associated StringVar
                    continue  # Skip individual radiobuttons, use the StringVar stored with the group label
                else:
                    value = widget
                self.data[key] = value
            print(self.data)
        
        create_btn = ttk.Button(vertical_stack, text="Create",
                               command=create_doctor)
        create_btn.pack(side="top", pady=25, anchor="center")
    
    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

        

#sav = StudentAddView()
# sav.mainloop()
