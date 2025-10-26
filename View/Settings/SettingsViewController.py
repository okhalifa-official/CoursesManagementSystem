import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '../Router'))
from Controller import DataController
import DataArchitecture as DataArch
import Router.route as _r


class SettingsView(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        # Window Info
        self.title("Settings")
        self.geometry("1000x600")
        
    def load(self):

        def back_btn_pressed():
            _r.route_back(self)

        back_btn = ttk.Button(self, text="Back",
                    command=back_btn_pressed)
        back_btn.pack(side="top", anchor="w", pady=10, padx=10)

        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill="both", anchor="center")
        main_frame.place(relx=.5, rely=.5, anchor="c")

        #---------------- Main Frame
        def button_pressed(type):
            print(type)


        users_btn = ttk.Button(main_frame, command=lambda x='users': button_pressed(x))
        users_btn.grid(column=0,row=0)
        logs_btn = ttk.Button(main_frame, command=lambda x='logs': button_pressed(x))
        logs_btn.grid(column=1,row=0)
        options_btn = ttk.Button(main_frame, command=lambda x='options': button_pressed(x))
        options_btn.grid(column=0,row=1)
        logout_btn = ttk.Button(main_frame, command=lambda x='signout': button_pressed(x))
        logout_btn.grid(column=1,row=1)
    
    def view(self):
        self.lift()
        self.focus_force()    # Force focus to window
        self.attributes('-topmost', True)  # Temporarily set as topmost
        self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
        self.state('zoomed')  # Open window in full screen mode

        

#sav = StudentAddView()
# sav.mainloop()
