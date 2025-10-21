import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
from DataModel import Doctor
from Controller import DataController, PopupHandler
import DataArchitecture as DataArch
import Router.route as _r
from Controller.Validation import Validation

def show_error(message: str):
    messagebox.showerror(
            "Invalid Entry",
            message
    )

def validate_data(data: dict) -> bool:
    # Example validation: Ensure required fields are filled
    message = ""
    if (message := Validation.is_valid_name(data['first_name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_name(data['last_name'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_country_code(data['country_code'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_phone_number(data['phone_number'])) != True:
        show_error(message)
        return False
    if (message := Validation.is_valid_email(data['email'])) != True:
        show_error(message)
        return False
    return True

class DoctorEditView(tk.Toplevel):
    def __init__(self,parent, doctor: Doctor):
        super().__init__(parent)

        # Window Info
        self.title("Edit Doctor")
        self.geometry("1000x600")
        self.doctor = doctor
        
    def load(self):
        doctor = self.doctor
        elements = DataArch.add_doctor_elements
        placeholder = DataArch.add_doctor_elements_placeholders
        self.entry = {}
        self.data = {}

        def back_btn_pressed():
            _r.route_back(self)

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
                        if doctor._doctor_data[label_text]:
                            radio_var.set(doctor._doctor_data[label_text])
                        else:
                            radio_var.set(options[0])
                        for i, option in enumerate(options):
                            self.entry[option] = ttk.Radiobutton(radio_frame, text=option, variable=radio_var, value=option)
                            self.entry[option].grid(row=0, column=i, padx=20)
                        self.entry[label_text] = radio_var
                    case _:
                        entry_widget = ttk.Entry(fields_frame)
                        if doctor._doctor_data[label_text]:
                            entry_widget.insert(0, doctor._doctor_data[label_text])
                            entry_widget.config(foreground="")
                        else:
                            entry_widget.insert(0, placeholder[label_text]) # placeholder
                            entry_widget.config(foreground="grey")
                        entry_widget.grid(row=r, column=1, padx=20)
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

        def update_doctor():
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
                self.data[key] = None
                try:
                    if value != placeholder[key]:
                        self.data[key] = value
                except KeyError:
                    self.data[key] = value

            if validate_data(self.data):
                if DataController.update_doctor(
                    id=self.doctor._doctor_data[self.doctor._doctor_columns[0]],
                    fname=self.data['first_name'],
                    lname=self.data['last_name'],
                    gender=self.data['gender'],
                    country=self.data['country_code'],
                    phone=self.data['phone_number'],
                    email=self.data['email']
                ):
                    back_btn_pressed()

        def delete_doctor():
            # show confirmation pop_up
            message = "Are you sure you want to delete this doctor?"
            confirmation_text = "Delete"
            result = PopupHandler.confirmation_popup(self, title="Delete Doctor", message=message, button1_text="Cancel", button2_text=confirmation_text)
            if result:
                print("delete")
                if DataController.delete_doctor(
                    id=self.doctor._doctor_data[self.doctor._doctor_columns[0]]
                ):
                    back_btn_pressed()
            else:
                print("canceled")
        
        btn_frame = ttk.Frame(vertical_stack)
        btn_frame.pack(fill="x", pady=25, side="bottom", anchor="center")

        delete_btn = tk.Button(
            btn_frame,
            text="Delete",
            fg='red',
            command=delete_doctor
        )
        delete_btn.grid(row=0, column=0, sticky="w")

        create_btn = ttk.Button(btn_frame, text="Save Changes",
                    command=update_doctor)
        create_btn.grid(row=0, column=1, padx=30, sticky="e")
    
    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

        

#sav = StudentAddView()
# sav.mainloop()
