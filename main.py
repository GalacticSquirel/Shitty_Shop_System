import tkinter as tk
import time
import tkinter.font as tkFont
import time
import os
from tkinter import *
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def admin_pass_check():
            global top
            top= Toplevel(app)
            top.geometry("200x100")
            label = Label(top,text="Input Password")
            label.pack()
            password = Entry(top,show="*",width=20)
            password.pack()
            def check():
                global valid
                pswd = password.get()
                if pswd == "yes":
                    valid = True
                    top.destroy()
                else:
                    valid = False
            button= Button(top, text="Submit", command=check)
            button.pack(pady=5, side= TOP)
        def final_check():
            admin_pass_check()
            app.wait_window(top)
            if not valid == None:
                if valid == True:
                    print("Password Was Correct")
                    master.switch_frame(Admin)

        frame = tk.Frame(self)## This is the bit I need help with
        self.grid_columnconfigure(0, weight=1)##


        label = tk.Label(self, text="This is the start page")
        user = tk.Button(self, text="User", command=lambda: master.switch_frame(User))
        admin = tk.Button(self, text="Admin", command=final_check)
        label.grid(row=0,column=0,sticky="NSEW")
        user.grid(row=1,column=0,sticky="NSEW")
        admin.grid(row=2,column=0,sticky="NSEW")

class User(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        page_1_label = tk.Label(self, text="This is page one")
        start_button = tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(StartPage))
        page_1_label.pack(side="top", fill="x", pady=10)
        start_button.pack()


class Admin(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        page_2_label = tk.Label(self, text="This is page two")
        start_button = tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(StartPage))
        page_2_label.grid(row=0,column=0,sticky="NSEW")
        start_button.grid(row=1,column=0,sticky="NSEW")
        start_button.grid()



app = App() 
app.geometry("500x500")
app.mainloop()
