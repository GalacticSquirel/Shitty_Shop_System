import os
import tkinter as tk
import tkinter
from tkinter import Spinbox
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Listbox
from tkinter import Toplevel
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import END
import enchant
d = enchant.Dict("en_GB")
import json
import os
import tkinter.messagebox as messagebox

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Cart)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=1)
        
class Cart(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        super().__init__(master)
        with open("cart.json") as f:
            cart = json.load(f)
            print(cart)
        y = 5
        displayed = []
        to_display = []
        def pressed(m):
            print(m," = ",variables.get(m).get())

        print(list(cart["items"]))
        for item in list(cart["items"]):
            if item not in displayed:
                to_display.append(item)
        current_vals = {}
        variables = {}
        for item in to_display:
            var = tk.StringVar()
            var.set(str(float(cart["items"][item]["quantity"])))
            current_vals[item] = var
            variables[item] = Spinbox(self,name=item,from_=0,to=30,textvariable=current_vals[item],wrap=True,command=lambda m=item:pressed(m))
            if y > 480:
                break
            Label(text=item).place(x=5,y=y)
            variables.get(item).place(x=100,y=y)
            y += 25
            displayed.append(item)

app = App()

app.iconbitmap(default="transparent.ico")
app.title("Shitty Shop")
app.geometry("500x500")

app.mainloop()