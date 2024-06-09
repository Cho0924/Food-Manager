import tkinter as tk
from tkinter import ttk
from database import Product, Database
from listwindow import ListWindow
from adminwindow import AdminWindow
from recipewindow import RecipeWindow

class MainWindow(tk.Tk):
    def __init__(self, dbname):
        super().__init__()
        self.db = Database(dbname)
        self.geometry("1000x1000")
        self.title("冷蔵庫管理アプリ deactory")
        
        # ボタンを配置するフレームを作成
        button_frame = ttk.Frame(self, relief=tk.RIDGE)
        button_frame.pack(expand=True, fill=tk.BOTH)
        
        style = ttk.Style()
        style.configure("my.TButton", font=("", 20))

        # ボタン1を作成
        button1 = ttk.Button(button_frame, text="在庫管理", style='my.TButton', command=lambda:add_admin_window())
        button1.pack(side="left", padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        # ボタン2を作成
        button2 = ttk.Button(button_frame, text="在庫一覧", style='my.TButton', command=lambda:add_list_window())
        button2.pack(side="left", padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        # ボタン3を作成
        button3 = ttk.Button(button_frame, text="レシピ検索", style='my.TButton', command=lambda:add_recipe_window())
        button3.pack(side="left", padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        def add_admin_window():
            AdminWindow(self.db)
            
        def add_list_window():
            ListWindow(self.db)
            
        def add_recipe_window():
            RecipeWindow(self.db)
        
    
if __name__ == "__main__":
    app = MainWindow("mydatabase.db")
    app.mainloop()