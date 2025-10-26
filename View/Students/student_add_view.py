import tkinter as tk
from tkinter import ttk, filedialog, messagebox
# suppress warning
from PIL import Image, ImageTk # type: ignore
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
import Model.DataArchitecture as DataArch
from Controller import DataController
import Router.route as _r
import shutil

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller extracts files here
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class StudentAddView(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        # Window Info
        self.title("Create New Student")
        self.geometry("1000x600")
        
    def load(self):
        # load student add view
        # Initialize UI Element holders and Placeholders
        elements = DataArch.add_student_elements
        placeholder = DataArch.add_student_elements_placeholders

        # Initialize Entry Objects {element_name: widget}
        self.entry = {}

        # Initialize Actual Entry Values
        self.data = {}

        # Back Button Handling
        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)


        # Initialize Student Card (Main) Frame
        student_card = ttk.Frame(self)
        student_card.pack(expand=True, fill="both", anchor="center")

        #---------------- Student Card
        # Create vertical stack inside student card
        vertical_stack = tk.Frame(student_card)
        vertical_stack.pack(expand=True, fill="both", anchor="center")
        vertical_stack.place(relx=.5, rely=.5, anchor="c")
        
        # Add picture box (image preview + select button)
        self.entry['Image'] = None
        self.img_preview = tk.Label(vertical_stack, text="No Image", width=20, height=8, bg="#eee", relief="ridge")
        self.img_preview.pack(pady=5, anchor="center")

        def select_image():
            path = filedialog.askopenfilename(filetypes=[("Image Files", ["*.png","*.jpg","*.jpeg","*.gif"])])
            if path:
                self.entry['Image'] = path
                # Show image in label
                img = Image.open(path)
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
                print(f"image updated {path}")
        img_btn = ttk.Button(vertical_stack, text="Select Image", command=select_image, width=10)
        img_btn.pack(pady=5, anchor="center")


        # Create entry fields frame below student image
        fields_frame = ttk.Labelframe(vertical_stack, text="")
        fields_frame.pack(pady=0, anchor="center")
        
        #--------------- Create New Student
        # Create entry fields for each element
        for r, row in enumerate(elements):
            # loop on all elements in the row
            for c,col in enumerate(row):
                # Create label for each field
                label_text = list(col.keys())[0]
                label = ttk.Label(fields_frame, text=f"{label_text}")
                label.grid(row=r, column=0, pady=15, padx=30, sticky="w")
                
                # Create input widget based on type
                values = list(col.values())
                if type(values[0]).__name__ == 'list':
                    # handle list of options (e.g., for radio buttons)
                    values = values[0]
                # Determine the type of the field
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
                        for i, option in enumerate(options):
                            self.entry[option] = ttk.Radiobutton(radio_frame, text=option, variable=radio_var, value=option)
                            self.entry[option].grid(row=0, column=i, padx=20)
                        self.entry[label_text] = radio_var
                    case _:
                        entry_widget = ttk.Entry(fields_frame)
                        entry_widget.grid(row=r, column=1, padx=20)

                        # Set placeholder text
                        entry_widget.insert(0, placeholder[label_text])
                        entry_widget.config(foreground="grey")

                        # Placeholder handling on focus in/out
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

                        # Store the entry widget in the dictionary
                        self.entry[label_text] = entry_widget
        
        def delete_image():
            target_folder = "assets/student_profile"
            try:
                if target_folder in self.data['Image']:
                    os.remove(self.data['Image'])
                    return True
            except Exception as e:
                    print(f"Error copying image: {e}")
                    return False

        def add_image():
            def name_image():
                # Create a unique name for the image
                return self.data['First Name'] + self.data['Last Name'] + self.data['Phone Number'][-5:]

            def copy_image_to_assets(path, custom_name):
                try:
                    ext = os.path.splitext(path)[1]
                    target_folder = resource_path("assets/student_profile")
                    os.makedirs(target_folder, exist_ok=True)

                    # Define new file path
                    new_filename = f"{custom_name}{ext}"
                    new_path = os.path.join(target_folder, new_filename)

                    # ✅ Skip copying if source and destination are same
                    if os.path.abspath(path) == os.path.abspath(new_path):
                        print("Source and destination are the same file — skipping copy.")
                        return new_path

                    # ✅ Copy and replace
                    shutil.copy2(path, new_path)
                    print(f"Image copied to: {new_path}")
                    delete_image()

                    return new_path

                except Exception as e:
                    print(f"Error copying image: {e}")
                    return False

            if self.data['Image'] is None:
                return True
            
            # Copy the selected image and update data
            self.data['Image'] = copy_image_to_assets(
                path=self.entry['Image'],
                custom_name=name_image()
            )

            if not self.data['Image']:
                return False
            return True

        def on_create_student():
            # on create button press call create_student from data controller
            if DataController.func_student(func=DataController.add_new_student,
                entry=self.entry, 
                data=self.data, 
                placeholder=placeholder
            ):
                if add_image():
                    back_btn_pressed()

        create_btn = ttk.Button(vertical_stack, text="Create", command=on_create_student)
        create_btn.pack(side="top", pady=25, anchor="center")
    
    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode
