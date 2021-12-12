import tkinter as tk
import os
from tkinter import *
import enchant
d = enchant.Dict("en_GB")
from tkinter import messagebox
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill='both', expand=1)


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def admin_pass_check():
            global top
            top= Toplevel(app)
            top.title("")
            top.geometry("200x100")
            top.resizable(False,False)
            label = Label(top,text="Input Password")
            label["justify"] = "center"
            label["text"] = "Input Password"
            label.place(x=0,y=0,width=200,height=30)
            password = Entry(top,show="*",width=30)
            password["justify"] = "center"
            password["text"] = "Input Password"
            password.place(x=10,y=30,width=180,height=30)
            
            def check():
                global valid
                pswd = password.get()
                if pswd == "yes":
                    valid = True
                    top.destroy()
                else:
                    valid = False
            submit= Button(top, text="Submit", command=check)
            submit["justify"] = "center"
            submit.place(x=20,y=70,width=70,height=25)
            cancel= Button(top, text="Cancel",command=lambda:top.destroy())
            cancel["justify"] = "center"
            cancel.place(x=110,y=70,width=70,height=25)
        def final_check():
            label["state"] = DISABLED
            user["state"] = DISABLED
            admin["state"] = DISABLED
            admin_pass_check()
            app.wait_window(top)
            label["state"] = NORMAL
            user["state"] = NORMAL
            admin["state"] = NORMAL
            if not valid == None:
                if valid == True:
                    print("Password Was Correct")
                    master.switch_frame(Admin)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        label = tk.Label(self, text="Select Mode",font=("Arial", 25))
        user = tk.Button(self, text="User", command=lambda: master.switch_frame(User), font=("Arial", 16))
        admin = tk.Button(self, text="Admin", command=final_check, font=("Arial", 16))
        label.grid(row=0,column=0,sticky="NSEW",padx = 50, pady = 60)
        user.grid(row=1,column=0,sticky="NSEW",padx = 50, pady = 60)
        admin.grid(row=2,column=0,sticky="NSEW",padx = 50, pady = 60)

class User(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        page_1_label = tk.Label(self, text="Mode Select")
        start_button = tk.Button(self, text="Mode Select", command=lambda: master.switch_frame(StartPage))
        page_1_label.pack(side="top", fill="x", pady=10)
        start_button.pack()


class Admin(tk.Frame):
    def __init__(self, master):
        global items
        global prices
        tk.Frame.__init__(self, master)
        class EditableListbox(tk.Listbox):
            tk.Frame.__init__(self, master)
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                self.edit_item = None
                self.bind("<Double-1>", self._start_edit)
            def _start_edit(self, event):
                global index
                index = self.index(f"@{event.x},{event.y}")
                self.start_edit(index)
                return "break"

            def start_edit(self, index):

                self.edit_item = index
                text = self.get(index)
                y0 = self.bbox(index)[1]
                entry = tk.Entry(self, borderwidth=0, highlightthickness=1)
                entry.bind("<Return>", self.accept_edit)
                entry.bind("<Escape>", self.cancel_edit)

                entry.insert(0, text)
                entry.selection_from(0)
                entry.selection_to("end")
                entry.place(relx=0, y=y0, relwidth=1, width=-1)
                entry.focus_set()
                entry.grab_set()

            def cancel_edit(self, event):
                event.widget.destroy()

            def accept_edit(self, event):
                new_data = event.widget.get()
                self.delete(self.edit_item)
                self.insert(self.edit_item, new_data)
                with open("items.txt", encoding='utf8') as f:
                    items = f.read().split(",")
                    print(items)
                items[index] = new_data
                with open("items.txt","w+") as f:
                    f.write(",".join(items))
                event.widget.destroy()
        class EditableListbox2(tk.Listbox):
            tk.Frame.__init__(self, master)
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                self.edit_item = None
                self.bind("<Double-1>", self._start_edit)
            def _start_edit(self, event):
                global index
                index = self.index(f"@{event.x},{event.y}")
                self.start_edit(index)
                return "break"

            def start_edit(self, index):

                self.edit_item = index
                text = self.get(index)
                y0 = self.bbox(index)[1]
                entry = tk.Entry(self, borderwidth=0, highlightthickness=1)
                entry.bind("<Return>", self.accept_edit)
                entry.bind("<Escape>", self.cancel_edit)

                entry.insert(0, text)
                entry.selection_from(0)
                entry.selection_to("end")
                entry.place(relx=0, y=y0, relwidth=1, width=-1)
                entry.focus_set()
                entry.grab_set()

            def cancel_edit(self, event):
                event.widget.destroy()

            def accept_edit(self, event):
                new_data = event.widget.get()
                self.delete(self.edit_item)
                self.insert(self.edit_item, new_data)
                with open("prices.txt", encoding='utf8') as f:
                    items = f.read().split(",")
                    print(items)
                items[index] = new_data
                with open("prices.txt","w+") as f:
                    f.write(",".join(items))
                event.widget.destroy()

        self.actual = EditableListbox(app)
        self.scrollbar = tk.Scrollbar(app, command=self.yview)
        self.actual.configure(yscrollcommand=self.yscroll1)
        self.price = EditableListbox2(app)
        self.price.configure(yscrollcommand=self.yscroll2)
        self.actual.place(height=340,width=375,x=5,y=40)
        self.scrollbar.place(x=480, y=40,height=340)
        self.price.place(height=340,width=100,x=380,y=40)
        with open("items.txt", encoding='utf8') as f:
            items = f.read().split(",")
        for i in items:
            self.actual.insert("end", i.capitalize())

        with open("prices.txt", encoding='utf8') as f:
            prices = f.read().split(",")
        for i in prices:
            self.price.insert("end", i)

        def Scankey(event):
            val = event.widget.get()
            print(val)
            if val == '':
                data = items
                prices_to_show = prices
            else:
                data = []
                for item in items:
                    if val.lower() in item.lower():
                        data.append(item)
                prices_to_show = []
                for thing in data:
                    index = items.index(thing)
                    prices_to_show.append(prices[index])
                
                print(prices_to_show)

            update(data)
            update_price(prices_to_show)
        def update(data):
            self.actual.delete(0, 'end')
            for item in data:
                self.actual.insert('end', item.capitalize())
        def update_price(data):
            self.price.delete(0,"end")
            for item in data:
                self.price.insert("end",item)
        entry = Entry(self)
        entry.place(width=420,x=60,y=5)
        entry.bind('<KeyRelease>', Scankey)
        searchlabel = Label(text="Search:")
        searchlabel.place(x=5,y=5)
        def insert(item,price,items):
            try:
                if d.check(item) == True and "".join(price.split(".")).isdigit():
                    if not item.lower() in items:
                        self.actual.insert('end', item.capitalize())
                        self.price.insert('end', price)
                        self.actual.see(self.actual.size())
                        with open("items.txt", encoding='utf8') as f:
                            items = f.read().split(",")
                        items.append(item)
                        with open("items.txt","w+") as f:
                            f.write(",".join(items))
                        with open("prices.txt", encoding='utf8') as f:
                            prices = f.read().split(",")
                        prices.append(price)
                        with open("prices.txt","w+") as f:
                            f.write(",".join(prices))
                        item_entry.delete(0,END)
                        price_entry.delete(0,END)
                    else:
                        messagebox.showerror('Python Error', 'Error: Item Already in List')
                elif d.check(item) == False:
                    messagebox.showerror('Python Error', 'Error: Item to Insert is Not a Word')
                elif not "".join(price.split(".")).isdigit():
                    messagebox.showerror('Python Error', 'Error: Price to Insert is Not a Valid Number or is Empty')
            except ValueError:
                messagebox.showerror('Python Error', 'Error: Can Not Insert Empty Item')
        def delete():
            for i in self.actual.curselection():
                self.actual.delete(i)
                self.price.delete(i)
                with open("items.txt", encoding='utf8') as f:
                    items = f.read().split(",")
                    del items[i]
                with open("items.txt","w+") as f:
                    f.write(",".join(items))
                with open("prices.txt", encoding='utf8') as f:
                    prices = f.read().split(",")
                    del prices[i]
                with open("prices.txt","w+") as f:
                    f.write(",".join(prices))
                

        item_entry = Entry(self)
        item_entry.place(width=295,x=5,y=400)
        price_entry = Entry(self)
        price_entry.place(width=130,x=305,y=400)
        insert_btn = Button(text="Insert",command=lambda:insert(item_entry.get().strip(),price_entry.get().strip(),items))
        insert_btn.place(height=20,width=50,x=440,y=400)
        delete_btn = Button(text="Delete Selected",command=delete)
        delete_btn.place(width=490,x=5,y=430)
        start_button = tk.Button(self, text="Mode Select", command=lambda: master.switch_frame(StartPage))
        start_button.place(width=490,x=5,y=465)

    def yscroll1(self, *args):
        if self.price.yview() != self.actual.yview():
            self.price.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yscroll2(self, *args):
        if self.actual.yview() != self.price.yview():
            self.actual.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def yview(self, *args):
        self.actual.yview(*args)
        self.price.yview(*args)

app = App()
app.iconbitmap(default='transparent.ico')
app.title("Shitty Shop")
app.geometry("500x500")
app.resizable(False,False)
app.mainloop()
