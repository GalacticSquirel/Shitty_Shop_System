import json
import os
import os
import tkinter
import tkinter as tk
from tkinter import (
    Button,
    DISABLED,
    END,
    Entry,
    Label,
    Listbox,
    NORMAL,
    Spinbox,
    Toplevel,
)
import tkinter.messagebox as messagebox

import enchant

d = enchant.Dict("en_GB")


items_location = "items.txt"
prices_location = "prices.txt"
combined_location="items_and_prices.json"
def on_close():
    if "cart.json" in os.listdir():
        os.remove("cart.json")
    if "combined.json" in os.listdir():
        os.remove("combined.json")

def close():
    if "cart.json" in os.listdir():
        os.remove("cart.json")
    if "combined.json" in os.listdir():
        os.remove("combined.json")
    app.destroy()


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
        self._frame.pack(fill="both", expand=1)


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
                    master.switch_frame(Admin)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        label = tk.Label(self, text="Select Mode",font=("Arial", 25))
        user = tk.Button(self, text="User", command=lambda:master.switch_frame(User), font=("Arial", 16))
        admin = tk.Button(self, text="Admin", command=final_check, font=("Arial", 16))
        label.grid(row=0,column=0,sticky="NSEW",padx = 50, pady = 60)
        user.grid(row=1,column=0,sticky="NSEW",padx = 50, pady = 60)
        admin.grid(row=2,column=0,sticky="NSEW",padx = 50, pady = 60)

class User(tk.Frame):
    def __init__(self, master):
        global items
        global prices
        tk.Frame.__init__(self, master)

        self.actual = Listbox(app)
        self.scrollbar = tk.Scrollbar(app, command=self.yview)
        self.actual.configure(yscrollcommand=self.yscroll1)
        self.price = Listbox(app)
        self.price.configure(yscrollcommand=self.yscroll2)
        self.actual.place(height=340,width=375,x=5,y=40)
        self.scrollbar.place(x=480, y=40,height=340)
        self.price.place(height=340,width=100,x=380,y=40)

        with open(combined_location) as f:
            combined = json.load(f)
            items = list(combined)
            prices = list(combined.values())
        for i in items:
            self.actual.insert("end", i.title())
            self.price.insert("end", prices[items.index(i)])
            
        def Scankey(event):
            val = event.widget.get()

            if val == "":
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
                

            update(data)
            update_price(prices_to_show)
        def update(data):
            self.actual.delete(0, "end")
            for item in data:
                self.actual.insert("end", item.title())
        def update_price(data):
            self.price.delete(0,"end")
            for item in data:
                self.price.insert("end",item)
        entry = Entry(self)
        entry.place(width=420,x=60,y=5)
        entry.bind("<KeyRelease>", Scankey)
        searchlabel = Label(text="Search:")
        searchlabel.place(x=5,y=5)
        def subtotal():
            global items_in_basket
            with open("cart.json") as f:
                cart = json.load(f)
            items_in_basket = []
            for item in list(cart["items"]):
                if cart["items"][item]["quantity"] == 1:
                    items_in_basket.append(float(cart["items"][item]["price"]))
                else:
                    items_in_basket.append(float(cart["items"][item]["quantity"]) * float(cart["items"][item]["price"]))

            subtotal_label["text"] = "Subtotal: " + str("{:.2f}".format(float(sum(list(map(float, items_in_basket))))))
        def add_to_cart():
            selected = []
            for i in self.actual.curselection():
                selected.append(i)
            if not selected == []:
                global cart
                with open(combined_location) as f:
                    combined = json.load(f)
                
                if not "cart.json" in os.listdir():
                    with open("cart.json","w") as f:
                        f.write('{"items":{}}')

                with open("cart.json") as f:
                    cart = json.load(f)

                for i in self.actual.curselection():
                    if not self.actual.get(i).lower() in list(cart["items"]):
                        cart["items"][self.actual.get(i).lower()] = {"price":combined[str(self.actual.get(i).lower())],"quantity":1}
                    else:
                        cart["items"][self.actual.get(i).lower()]["quantity"] = int(cart["items"][self.actual.get(i).lower()]["quantity"]) + 1
                    
                with open("cart.json", "w") as file:
                    file.write(json.dumps(cart))
                combined["cart"] = cart
                with open("combined.json", "w") as file:
                    file.write(json.dumps(combined))
                subtotal()
            else:
                messagebox.showerror("Python Error", "Error: Nothing Selected")
        def cart_check():
            if "cart.json" in os.listdir():
                with open("cart.json") as f:
                    cart = json.load(f)
                if not list(cart["items"]) == []:
                    master.switch_frame(Detailed_Cart)
                else:
                    messagebox.showerror("Python Error", "Error: Basket is Empty")
            else:
                messagebox.showerror("Python Error", "Error: Basket is Empty")

        button = Button(text="Add to Cart",command=add_to_cart)
        button.place(width=475,x=5,y=390)
        subtotal_label = Label(text="Subtotal")
        subtotal_label.place(width=475,x=5,y=417.5)
        cart = Button(text="Check Out",command=lambda:cart_check())
        cart.place(width=475,x=5,y=440)
        Button(text="Mode Select",command=lambda:master.switch_frame(StartPage)).place(width=475,x=5,y=470)
        
        
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
                self.insert(self.edit_item, new_data.title())
                with open(combined_location) as f:
                    combined = json.load(f)
                    items = list(combined)
                    prices = list(combined.values())
                    items[index] = new_data.lower()
                    combined = dict(zip(items, prices))
                    loc = open(combined_location, "w")
                    json.dump(combined,loc)
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
                with open(combined_location) as f:
                    combined = json.load(f)
                    items = list(combined)
                    prices = list(combined.values())
                    prices[index] = new_data.lower()
                    combined = dict(zip(items, prices))
                    loc = open(combined_location, "w")
                    json.dump(combined,loc)
                event.widget.destroy()

        self.actual = EditableListbox(app)
        self.scrollbar = tk.Scrollbar(app, command=self.yview)
        self.actual.configure(yscrollcommand=self.yscroll1)
        self.price = EditableListbox2(app)
        self.price.configure(yscrollcommand=self.yscroll2)
        self.actual.place(height=340,width=375,x=5,y=40)
        self.scrollbar.place(x=480, y=40,height=340)
        self.price.place(height=340,width=100,x=380,y=40)
        with open(combined_location) as f:
            combined = json.load(f)
            items = list(combined)
            prices = list(combined.values())
        for i in items:
            self.actual.insert("end", i.title())
            self.price.insert("end", prices[items.index(i)])

        def Scankey(event):
            val = event.widget.get()
            if val == "":
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

            update(data)
            update_price(prices_to_show)
        def update(data):
            self.actual.delete(0, "end")
            for item in data:
                self.actual.insert("end", item.title())
        def update_price(data):
            self.price.delete(0,"end")
            for item in data:
                self.price.insert("end",item)
        entry = Entry(self)
        entry.place(width=420,x=60,y=5)
        entry.bind("<KeyRelease>", Scankey)
        searchlabel = Label(text="Search:")
        searchlabel.place(x=5,y=5)
        def insert(item,price,items):

            try:
                if d.check(item) == True and "".join(price.split(".")).isdigit():
                    if not item.lower() in items and not item in items:
                        self.actual.insert("end", item.title())
                        self.price.insert("end", str("{:.2f}".format(float(price))))
                        self.actual.see(self.actual.size())
                        with open(combined_location) as f:
                            combined = json.load(f)
                            items = list(combined)
                            prices = list(combined.values())
                            items.append(item.lower())
                            prices.append(str("{:.2f}".format(float(price))))
                            combined = dict(zip(items, prices))
                            loc = open(combined_location, "w")
                            json.dump(combined,loc)
                        item_entry.delete(0,END)
                        price_entry.delete(0,END)
                    else:
                        messagebox.showerror("Python Error", "Error: Item Already in List")
                elif d.check(item) == False:
                    messagebox.showerror("Python Error", "Error: Item to Insert is Not a Word")
                elif not "".join(price.split(".")).isdigit():
                    messagebox.showerror("Python Error", "Error: Price to Insert is Not a Valid Number or is Empty")
            except ValueError:
                messagebox.showerror("Python Error", "Error: Can Not Insert Empty Item")
        def delete():
            for i in self.actual.curselection():
                self.actual.delete(i)
                self.price.delete(i)
                with open(combined_location) as f:
                    combined = json.load(f)
                    items = list(combined)
                    prices = list(combined.values())
                    del items[i]
                    del prices[i]
                    combined = dict(zip(items, prices))
                    loc = open(combined_location, "w")
                    json.dump(combined,loc)
                    f.close()

        item_entry = Entry(self)
        item_entry.place(width=295,x=5,y=400)
        price_entry = Entry(self)
        price_entry.place(width=130,x=305,y=400)
        insert_btn = Button(text="Insert",command=lambda:insert(item_entry.get().strip().lower(),price_entry.get().strip(),items))
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

class Cart(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        def pay():
            pass
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        lb = Label(text= f"You Owe {str('{:.2f}'.format(float(sum(list(map(float, items_in_basket))))))}")
        lb.place(width=490,x=5,y=5,height=40)
        
        def coin_count(amount, coin_name, coin_value):
            num_coins = 0
            
            
            while float(amount) >= float(coin_value):

                num_coins += 1
                float(amount) 
                float(coin_value)
                amount -= coin_value
            if num_coins == 1 :
                coinlist.append(f"{str(num_coins)} {str(coin_name)}")
            elif num_coins > 1:
                coinlist.append(f"{str(num_coins)} {str(coin_name)}s")
            return amount
        global coinlist
        coinlist=[]
        temp_amount = float(sum(list(map(float, items_in_basket))))
        print(temp_amount)
        temp_amount = coin_count(temp_amount, "Fifty Pound", 50.00)
        temp_amount = coin_count(temp_amount, "Twenty Pound", 20.00)
        temp_amount = coin_count(temp_amount, "Ten Pound", 10.00)
        temp_amount = coin_count(temp_amount, "Five Pound", 5.00)
        temp_amount = coin_count(temp_amount, "Two Pound", 2.00)
        temp_amount = coin_count(temp_amount, "Pound", 10)
        temp_amount = coin_count(temp_amount, "50p", 0.50)
        temp_amount = coin_count(temp_amount, "20p", 0.20)
        temp_amount = coin_count(temp_amount, "5p", 0.05)
        temp_amount = coin_count(temp_amount, "2p", 0.02)
        temp_amount = coin_count(temp_amount, "1p", 0.01)
        lb = Label(text=", ".join(coinlist))
        lb.place(width=490,x=5,y=55,height=40)
        back = Button(text="Back" ,command=lambda:master.switch_frame(Detailed_Cart))
        back.place(width=490,x=5,y=100,height=40)
        done = Button(text="Done" ,command=close)
        done.place(width=490,x=5,y=180,height=40)
#i wouldnt look below the code is dodgy
class Detailed_Cart(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        with open("cart.json") as f:
            cart = json.load(f)
            print(cart)
        def next_page(labels,displayed):
            for widgets in self.winfo_children():
                widgets.destroy()
            for item in list(labels):
                labels.get(item).destroy()
            to_display = []
            for item in list(cart["items"]):
                if item not in displayed:
                    to_display.append(item)
        y = 5
        displayed = []
        to_display = []
        def pressed(m):
            print(m," = ",variables.get(m).get())

        for item in list(cart["items"]):
            if item not in displayed:
                to_display.append(item)
        pages_required = len(to_display)/40
        print(pages_required)
        current_vals = {}
        variables = {}
        labels = {}
        if pages_required <= 1:
            for item in to_display:
                var = tk.StringVar()
                var.set(str(float(cart["items"][item]["quantity"])))
                current_vals[item] = var
                variables[item] = Spinbox(self,name=item,from_=0,to=30,textvariable=current_vals[item],wrap=True,command=lambda m=item:pressed(m))
                variables.get(item).place(x=100,y=y)
                if y > 480:
                    y=5
                    break
                labels[item] = Label(text=item.title())
                labels.get(item).place(x=5,y=y)
                
                y += 25
                displayed.append(item)
            to_display = []
            for item in list(cart["items"]):
                if item not in displayed:
                    to_display.append(item)
            for item in to_display:
                var = tk.StringVar()
                var.set(str(float(cart["items"][item]["quantity"])))
                current_vals[item] = var
                variables[item] = Spinbox(self,name=item,from_=0,to=30,textvariable=current_vals[item],wrap=True,command=lambda m=item:pressed(m))
                variables.get(item).place(x=100,y=y)
                if y > 480:
                    y=5
                    break
                labels[item] = Label(text=item.title())
                labels.get(item).place(x=5,y=y)
                y += 25
                displayed.append(item)
            Button(text="Previous Page").place(x=5,width=240,y=470)
            Button(text="Next Page",command=lambda:next_page(labels,displayed)).place(x=255,width=240,y=470)
        else:

            pass
            #delete current ones and add next set
# class Cart(tk.Frame):

#     def __init__(self, master):
#         tk.Frame.__init__(self, master)
#         super().__init__(master)
#         def final_total(event,current_value):
#             item_name = str(event.widget).split(".")[2]

#             print(event.widget.get())
#             with open("combined.json") as f:
#                 combined = json.load(f)
            
#             with open("cart.json") as f:
#                 cart = json.load(f)

#             print(current_value,"not equal value")

#             cart["items"][item_name]["quantity"] = int(current_value.get())
#             print(current_value)
#             with open("cart.json", "w") as file:
#                 file.write(json.dumps(cart))
#             combined["cart"] = cart
#             with open("combined.json", "w") as file:
#                 file.write(json.dumps(combined))
#         def display_selected(event):

#             item_name = str(event.widget).split(".")[2]
#             print(item_name)
#             lb=Label(self,text=f"You selected {current_vals[item_name].get()}", font=("sans-serif", 6),)
#             lb.pack()
#             print(current_vals[item_name].get())
#         with open("cart.json") as f:
#             cart = json.load(f)
#             print(cart)
#         y = 5
#         displayed = []
#         to_display = []
    
#         print(list(cart["items"]))
#         for item in list(cart["items"]):
#             print("item", item)
#             if item not in displayed:
#                 to_display.append(item)
#                 print(item)
#         print(displayed)
#         current_vals = {}
#         for item in to_display:
#             if y > 480:
#                 break
#             Label(text=item).place(x=5,y=y)
#             var = tk.StringVar()
#             var.set(str(float(cart["items"][item]["quantity"])))
#             current_vals[item] = var
#             print(current_vals)
#             #current_value = StringVar(value=str(float(((cart["items"][item]["quantity"])))))
#             spin_box = Spinbox(self,name=item,from_=0,to=30,textvariable=current_vals[item],wrap=True)
#             spin_box.bind("<Button-1>",lambda event: display_selected(event))
#             spin_box.place(x=100,y=y)
#             y += 25
#             displayed.append(item)
#         def oddblue(var,b,c):
#             if len(var.get())%2 == 0:
#                 lb = Label(text=var)
#                 lb.place(x=400,y=80)
#             else:

#                 spin_box.update_idletasks()
        #var.trace("w",oddblue)
        #this is a very work in progress area
            #need to add pages to accomodate more items to be added by admin

app = App()
app.protocol("WM_DELETE_WINDOW", close)
app.iconbitmap(default="transparent.ico")
app.title("Shitty Shop")
app.geometry("500x500")
#app.resizable(False,False)
app.mainloop()
