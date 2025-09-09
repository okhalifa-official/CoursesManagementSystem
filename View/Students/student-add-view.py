import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import student_info_data_model as info


class StudentAddView(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Info
        self.title("Add Student")
        self.geometry("1000x600")

        elements = info.add_student_elements
        self.entry = {}

        def back_btn_pressed():
            print("Hello")

        back_btn = ttk.Button(self, text="Back",
                    command=lambda: back_btn_pressed)
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

        def select_image():
            self.withdraw()
            path = filedialog.askopenfilename(filetypes=[("Image Files", ["*.png","*.jpg","*.jpeg","*.gif"])])
            self.deiconify()
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
        
        #--------------- Create New Student
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
                    case 'entry':
                        self.entry[label_text] = ttk.Entry(fields_frame)
                        self.entry[label_text].grid(row=r, column=1, padx=20)
                    case 'number':
                        self.entry[label_text] = ttk.Entry(fields_frame)
                        self.entry[label_text].grid(row=r, column=1, padx=20)
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
                #print(values)
        def create_student():
            print("hello world")
        create_btn = ttk.Button(vertical_stack, text="Create",
                               command=lambda: create_student)
        create_btn.pack(side="top", pady=25, anchor="center")

        

if __name__ == "__main__":
    sav = StudentAddView()
    sav.lift()           # Bring window to front
    sav.focus_force()    # Force focus to window
    sav.attributes('-topmost', True)  # Temporarily set as topmost
    sav.after(100, lambda: sav.attributes('-topmost', False))  # Remove topmost after 100ms
    sav.mainloop()
