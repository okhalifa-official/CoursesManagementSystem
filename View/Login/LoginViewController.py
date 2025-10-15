import tkinter as tk
from tkinter import ttk, filedialog
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
from Controller import DataController
import Router.route as _r
from View import TableView


class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Info
        self.title("Login to Courses Management System")
        self.geometry("1000x600")

        self.entry = {}
        self.data = {}

        credentials_frame = ttk.Frame(self)
        credentials_frame.pack(expand=True, fill="both", anchor="center")

        #---------------- Credentials Frame
        vertical_stack = tk.Frame(credentials_frame)
        vertical_stack.pack(expand=True, fill="x", anchor="center")
        vertical_stack.place(relx=.5, rely=.5, anchor="c")
        
        email_label = ttk.Label(vertical_stack, text="E-mail")
        email_label.grid(row=0, column=0, pady=15, padx=30, sticky="w")
        email_entry = ttk.Entry(vertical_stack)
        email_entry.grid(row=0, column=1, padx=20, sticky='w')

        pass_label = ttk.Label(vertical_stack, text="Password")
        pass_label.grid(row=1, column=0, pady=15, padx=30, sticky="w")
        pass_entry = ttk.Entry(vertical_stack)
        pass_entry.grid(row=1, column=1, padx=20, sticky='w')

        def attempt_login():
            print("login pressed")
            _r.route(self, TableView.CoursesApp(self))
        
        login_btn = ttk.Button(credentials_frame, text="Login",
                               command=attempt_login)
        login_btn.pack(side='bottom', pady=25, anchor="center")
    
    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode
