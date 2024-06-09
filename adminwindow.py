import tkinter as tk
from tkinter import ttk
import datetime
import math
from PIL import Image, ImageTk
from functools import partial
from database import Product, Database
from camerawindow import CameraWindow
from ocrfunction import process

class AdminWindow:
    def __init__(self, db: Database):
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("在庫管理")
        self.window.geometry("1000x1000")
        self.tool_frame = ttk.Frame(self.window, borderwidth = 2, relief = tk.SUNKEN)
        self.tool_frame.pack(side=tk.TOP, fill=tk.X)
        self.back_button = ttk.Button(self.tool_frame, text="戻る", command=lambda:self.window.destroy())
        self.back_button.pack(side="left")
        self.button_paned = ttk.Panedwindow(self.window)
        self.button_paned.pack(expand=True, fill=tk.BOTH)
        self.button_paned.grid_rowconfigure(0, weight=1)
        self.button_paned.grid_columnconfigure(0, weight=1)
        self.button_paned.grid_columnconfigure(1, weight=1)
        self.register_button = ttk.Button(self.button_paned, text="在庫登録", command=lambda:register())
        self.button_paned.add(self.register_button)
        self.register_button.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.delete_button = ttk.Button(self.button_paned, text="在庫編集", command=lambda:edit())
        self.button_paned.add(self.delete_button)
        self.delete_button.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        def register():
            self.window.destroy()
            RegisterWindow(self.db)
        
        def edit():
            self.window.destroy()
            EditWindow(self.db)
        
class RegisterWindow:
    def __init__(self, db: Database):
        from data import data
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("商品の追加")
        self.window.geometry("1000x1000")
        self.button_paned = ttk.Panedwindow(self.window)
        self.button_paned.pack(expand=True, fill=tk.BOTH)
        self.button_paned.grid_rowconfigure(0, weight=1)
        self.button_paned.grid_columnconfigure(0, weight=1)
        self.button_paned.grid_columnconfigure(1, weight=1)
        self.camera_button = ttk.Button(self.button_paned, text="レシート読み取り", command=lambda:add_camera())
        self.button_paned.add(self.camera_button)
        self.camera_button.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.manual_button = ttk.Button(self.button_paned, text="手動入力", command=lambda:add_manual())
        self.button_paned.add(self.manual_button)
        self.manual_button.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        def add_manual():
            self.window.destroy()
            ManualWindow(self.db)
        
        def add_camera():
            self.window.destroy()
            CameraWindow().window.wait_window()
            indices = process("outputimage.jpg", data)
            SelectWindow(self.db, indices)

class ManualWindow:
    def __init__(self, db: Database):
        from data import data
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("手動入力")
        self.window.geometry("1000x1000")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=10)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=20)
        self.window.grid_columnconfigure(2, weight=1)
        self.back_button = ttk.Button(self.window, text="戻る", command=lambda:self.window.destroy())
        self.back_button.grid(row=0, column=0)
        self.var = tk.StringVar(value=data)
        self.listbox = tk.Listbox(self.window, height=10, listvariable=self.var, selectmode=tk.MULTIPLE, font=("", 30))
        self.scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.listbox.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.add_button = ttk.Button(self.window, text="選択", command=lambda:selectnumber(self.listbox.curselection()))
        self.add_button.grid(row=2, column=1, sticky=(tk.W))

        def selectnumber(indices):
            SelectWindow(self.db, indices, self)

class SelectWindow:
    def __init__(self, db: Database, indices: list, parent: ManualWindow = None):
        from data import data
        unitset = ["個", "mL", "L", "mg", "g", "kg"]
        self.db = db
        self.parent = parent
        self.indices = indices
        self.window = tk.Toplevel()
        self.window.title("個数入力")
        self.window.geometry("1000x1000")
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=20)
        self.window.grid_columnconfigure(2, weight=1)
        i = 0
        self.number = []
        self.unit = []
        for index in indices:
            self.number.append([tk.IntVar(), tk.IntVar()])
            self.unit.append(tk.StringVar(value="個"))
            ttk.Label(self.window, text=data[index], font=("", 20)).grid(row=i+1, column=1, sticky=tk.W)
            ttk.Label(self.window, text="数量").grid(row=i+1, column=2)
            ttk.Spinbox(self.window, from_=0, to=1000, increment=1, textvariable=self.number[i][0]).grid(row=i+1, column=3)
            ttk.Label(self.window, text=".").grid(row=i+1, column=4)
            ttk.Spinbox(self.window, from_=0, to=75, increment=25, textvariable=self.number[i][1]).grid(row=i+1, column=5)
            ttk.Spinbox(self.window, state='readonly', textvariable=self.unit[i], values=unitset).grid(row=i+1, column=6)
            i += 1
        self.add_button = ttk.Button(self.window, text="戻る", command=lambda:self.window.destroy())
        self.add_button.grid(row=0, column=0, sticky=(tk.W))
        self.add_button = ttk.Button(self.window, text="選択", command=lambda:self.add_to_database(i))
        self.add_button.grid(row=i+2, column=0, sticky=(tk.W))

    def add_to_database(self, n):
        from data import data
        dt = datetime.datetime.now()
        for i in range(n):
            number = self.number[i][0].get()+self.number[i][1].get()/100
            if number:
                new_item = Product(-1, data[self.indices[i]], (dt.year, dt.month, dt.day), "消費期限"
                , (dt.year, dt.month, dt.day), number, self.unit[i].get()
                , "/Users/debunhiroto/ffffff.png", "")
                self.db.insert_product(new_item)
        self.window.destroy()
        if self:
            self.parent.window.destroy()
        
class EditWindow:
    def __init__(self, db: Database):
        from data import data
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("手動入力")
        self.window.geometry("1000x1000")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=100)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=100)
        self.window.grid_columnconfigure(2, weight=1)
        self.back_button = ttk.Button(self.window, text="戻る", command=lambda:self.window.destroy())
        self.back_button.grid(row=0, column=0)
        self.var = tk.StringVar(value=data)
        self.canvas = tk.Canvas(self.window)
        self.canvas.configure(scrollregion=(0,0,1000,1000))
        self.scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=self.canvas.yview)
        self.canvas['yscrollcommand'] = self.scrollbar.set
        self.canvas.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        i = 0
        self.number = []
        self.spinbox = []
        self.rows = self.db.get_all_products()
        self.namelabel = []
        self.id = []

        def setzero(n):
            self.spinbox[n][0].set(0)
            self.spinbox[n][1].set(0)
        
        for row in self.rows:
            self.id.append(row.id)
            self.number.append([tk.IntVar(), tk.IntVar()])
            self.spinbox.append([])
            self.namelabel.append(ttk.Label(self.canvas, text=row.name))
            self.namelabel[i].grid(row=i, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
            self.namelabel[i].bind("<Button-1>", partial(self.detail_update, i))
            ttk.Button(self.canvas, text="削除", command=partial(setzero, i)).grid(row=i, column=1)
            self.spinbox[i].append(ttk.Spinbox(self.canvas, from_=0, to=1000, increment=1, textvariable=self.number[i][0]))
            self.spinbox[i][0].grid(row=i, column=2)
            self.spinbox[i][0].insert(0, math.floor(row.quantity))
            self.number[i][0].set(int(self.number[i][0].get()/10))
            ttk.Label(self.canvas, text=".").grid(row=i, column=3)
            self.spinbox[i].append(ttk.Spinbox(self.canvas, from_=0, to=75, increment=25, textvariable=self.number[i][1]))
            self.spinbox[i][1].grid(row=i, column=4)
            self.spinbox[i][1].insert(0, int(math.modf(row.quantity)[0]*100))
            ttk.Label(self.canvas, text=row.unit).grid(row=i, column=5)
            i += 1

        self.enter_button = ttk.Button(self.window, text="確定な", command=lambda:self.update_database(i))
        self.enter_button.grid(row=2, column=1, sticky=(tk.W))

    def detail_update(self, i, event):
        print(self.id[i])
        DetailWindow(self.db, self.id[i])

    def update_database(self, n):
        for i in range(n):
            number = self.number[i][0].get()+self.number[i][1].get()/100
            row = self.rows[i]
            if number:
                new_item = Product(row.id, row.name, row.purchase_date, row.expiry_type
                , row.expiry_date, number, row.unit
                , row.imagefile, row.note)
                self.db.update_product(new_item)
            else:
                self.db.delete_product(row)

class DetailWindow:
    def __init__(self, db: Database, id: int):
        self.db = db
        self.id = id
        self.window = tk.Toplevel()
        self.window.title("詳細編集")
        self.window.geometry("1000x1000")
        unitset = ["個", "mL", "L", "mg", "g", "kg"]

        product = self.db.get_product_by_id(self.id)

        self.name = tk.StringVar(value=product.name)
        ttk.Label(self.window, text=self.name).grid(row=0, column=0)

        ttk.Label(self.window, text="購入日").grid(row=1, column=0)
        py, pm, pd = eval(product.purchase_date)
        self.purchase_year = tk.IntVar(value=py)
        self.purchase_month = tk.IntVar(value=pm)
        self.purchase_day = tk.IntVar(value=pd)
        ttk.Spinbox(self.window, from_=2000, to=2100, increment=1, textvariable=self.purchase_year).grid(row=1, column=1)
        ttk.Spinbox(self.window, from_=1, to=12, increment=1, textvariable=self.purchase_month).grid(row=1, column=2)
        ttk.Spinbox(self.window, from_=1, to=31, increment=1, textvariable=self.purchase_day).grid(row=1, column=3)

        self.expiry_type = tk.IntVar(value=["賞味期限", "消費期限"].index(product.expiry_type))
        ttk.Radiobutton(self.window, text="賞味期限", value=0, variable=self.expiry_type).grid(row=2, column=0)
        ttk.Radiobutton(self.window, text="消費期限", value=1, variable=self.expiry_type).grid(row=2, column=1)

        ey, em, ed = eval(product.expiry_date)
        self.expiry_year = tk.IntVar(value=ey)
        self.expiry_month = tk.IntVar(value=em)
        self.expiry_day = tk.IntVar(value=ed)
        ttk.Spinbox(self.window, from_=2000, to=2100, increment=1, textvariable=self.expiry_year).grid(row=2, column=2)
        ttk.Spinbox(self.window, from_=1, to=12, increment=1, textvariable=self.expiry_month).grid(row=2, column=3)
        ttk.Spinbox(self.window, from_=1, to=31, increment=1, textvariable=self.expiry_day).grid(row=2, column=4)

        self.quantity = [tk.IntVar(value=int(product.quantity)), tk.IntVar(value=int(math.modf(product.quantity)[0]*100))]
        self.unit = tk.StringVar(value=product.unit)
        ttk.Button(self.window, text="削除", command=lambda:setzero()).grid(row=3, column=0)
        ttk.Spinbox(self.window, from_=0, to=1000, increment=1, textvariable=self.quantity[0]).grid(row=3, column=1)
        ttk.Label(self.window, text=".").grid(row=3, column=2)
        ttk.Spinbox(self.window, from_=0, to=75, increment=25, textvariable=self.quantity[1]).grid(row=3, column=3)
        ttk.Spinbox(self.window, state='readonly', textvariable=self.unit, values=unitset).grid(row=3, column=4)
        def setzero():
            self.quantity[0].set(0)
            self.quantity[1].set(0)

        self.imagefile = product.imagefile
        image_pil = Image.open(product.imagefile) #imagefileにはPNG型のパスを入れる
        image_resized = image_pil.resize((100, 100))
        image_tk = ImageTk.PhotoImage(image=image_resized, master=self.window)
        self.canvas = tk.Canvas(self.window, bg="white", height=100, width=100)
        self.canvas.grid(row=4, column=0)
        self.canvas.create_image(0, 0, image=image_tk, anchor=tk.NW)

        self.note = tk.StringVar(value=product.note)
        ttk.Entry(self.window, textvariable=self.note).grid(row=5, column=0)

        ttk.Button(self.window, text="確定な", command=lambda:self.update_database()).grid(row=6, column=1)

    def update_database(self):
        number = self.quantity[0].get()+self.quantity[1].get()/100
        print(self.expiry_type.get())
        expiry_type = ["賞味期限", "消費期限"][self.expiry_type.get()]
        if number:
            new_item = Product(self.id, self.name.get(), (self.purchase_year.get(), self.purchase_month.get(), self.purchase_day.get()), expiry_type
            , (self.expiry_year.get(), self.expiry_month.get(), self.expiry_day.get()), number, self.unit.get()
            , self.imagefile, self.note.get())
            self.db.update_product(new_item)
        else:
            self.db.delete_product(Product(self.id, -1, -1, -1, -1, -1, -1, -1, -1))

if __name__ == "__main__":
    root = tk.Tk()
    db = Database("mydatabase.db")
    root.geometry("1000x1000")
    root.title("main")
    sub = AdminWindow(db)    
    root.mainloop()

