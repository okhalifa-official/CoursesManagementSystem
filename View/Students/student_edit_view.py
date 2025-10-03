import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Model'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
from DataModel import Student
import DataArchitecture as DataArch
import Router.route as _r


class StudentEditView(tk.Toplevel):
    def __init__(self, parent, student: Student):
        super().__init__(parent)

        # Window Info
        self.title("Edit Student")
        self.geometry("1000x600")
        self.student = student

    def load(self):
        student = self.student
        elements = DataArch.add_student_elements
        placeholder = DataArch.add_student_elements_placeholders
        self.entry = {}

        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        student_card = ttk.Frame(self)
        student_card.pack(expand=True, fill="both", anchor="center")
        # student_card.place(relx=.5, rely=.5, anchor="c")

        #---------------- Student Card
        vertical_stack = tk.Frame(student_card)
        vertical_stack.pack(expand=True, fill="both", anchor="center")
        vertical_stack.place(relx=.5, rely=.5, anchor="c")
        
        # Add picture box (image preview + select button)
        self.entry['Student Image'] = None
        self.img_preview = tk.Label(vertical_stack, text="No Image", width=20, height=8, bg="#eee", relief="ridge")
        self.img_preview.pack(pady=5, anchor="center")

        # Load existing image
        if student._student_data['Image']:
            path = student._student_data['Image']
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

        fields_frame = ttk.Labelframe(vertical_stack, text="")
        fields_frame.pack(pady=0, anchor="center")
        
        #--------------- Edit Student Fields
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
                        if student._student_data[label_text]:
                            radio_var.set(student._student_data[label_text])
                        else:
                            radio_var.set(options[0])
                        for i, option in enumerate(options):
                            self.entry[option] = ttk.Radiobutton(radio_frame, text=option, variable=radio_var, value=option)
                            self.entry[option].grid(row=0, column=i, padx=20)
                        self.entry[label_text] = radio_var
                    case _:
                        entry_widget = ttk.Entry(fields_frame)
                        entry_widget.grid(row=r, column=1, padx=20)
                        if student._student_data[label_text]:
                            entry_widget.insert(0, student._student_data[label_text])
                            entry_widget.config(foreground="")
                        else:
                            entry_widget.insert(0, placeholder[label_text]) # placeholder
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
        def update_student():
            print("hello world")
        def delete_student():
            print("delete")
        
        btn_frame = ttk.Frame(vertical_stack)
        btn_frame.pack(side="top", pady=25, fill="x", anchor="center")

        delete_btn = tk.Button(
            btn_frame,
            text="Delete",
            fg='red',
            command=delete_student
        )
        delete_btn.grid(row=0, column=0, sticky="w")

        create_btn = ttk.Button(btn_frame, text="Save Changes",
                    command=update_student)
        create_btn.grid(row=0, column=1, padx=30, sticky="e")

    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

    
