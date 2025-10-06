import tkinter as tk
from tkinter import ttk

class PopupView(tk.Toplevel):
    def __init__(self, parent, title="Confirmation", message="Are you sure?", 
                 button1_text="No", button2_text="Yes"):
        super().__init__(parent)
        
        self.result = None  # Store the result
        
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        
        # Center the popup on parent window
        self.transient(parent)
        self.grab_set()
        
        # Center the popup
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.winfo_screenheight() // 2) - (150 // 2)
        self.geometry(f"300x150+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Centered label
        self.message_label = tk.Label(main_frame, text=message, 
                                     font=("Arial", 12), wraplength=250, 
                                     justify="center")
        self.message_label.pack(expand=True)
        
        # Button frame at bottom
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side="bottom", pady=(10, 0))
        
        # Buttons centered
        self.button1 = ttk.Button(button_frame, text=button1_text, 
                                 command=self.on_button1)
        self.button1.pack(side="left", padx=(0, 10))
        
        self.button2 = ttk.Button(button_frame, text=button2_text, 
                                 command=self.on_button2)
        self.button2.pack(side="left")
        
        # Focus on the second button (typically "No" or "Cancel")
        self.button2.focus()
    
    def on_button1(self):
        self.result = False
        self.destroy()
    
    def on_button2(self):
        self.result = True
        self.destroy()