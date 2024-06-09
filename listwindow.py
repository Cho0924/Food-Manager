import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from database import Product, Database



class ListWindow:
    def __init__(self, db):
        self.window = tk.Toplevel()
        self.db = db
        self.window.title('在庫一覧')
        self.window.geometry('1000x1000')

        # Treeviewの生成
        column = ('野菜', '消費期限', '数量')
        tree = ttk.Treeview(self.window, columns=column, selectmode="none")

        #Treeviewの各行のサイズ変更
        s = ttk.Style()
        s.configure("Treeview", rowheight=60, font=("arial", 15))
        s.configure("Treeview.Heading", rowheight=60, font=("arial", 25))

        # 列の設定
        tree.column('#0',width=120, stretch='no')
        tree.column('野菜',anchor='w', width=100)
        tree.column('消費期限', anchor='w', width=80)
        tree.column('数量', anchor='w', width=80)

        # 列の見出し設定
        tree.heading('野菜', text='野菜', anchor='w')
        tree.heading('消費期限',text='消費期限', anchor='w')
        tree.heading('数量',text='数量', anchor='w')
        
        rows = self.db.get_all_products()
        for row in rows:
            if row.imagefile:
                image_pil = Image.open(row.imagefile) #imagefileにはPNG型のパスを入れる
                image_resized = image_pil.resize((60, 60))
                image_tk = ImageTk.PhotoImage(image=image_resized, master=self.window)
                image_tk = ImageTk.PhotoImage(file=row.imagefile)
                
                tree.insert(parent="", 
                        index="end", 
                        image=image_tk,
                        value=(row.name, row.expiry_date, str(row.quantity)+row.unit))
            else:
                tree.insert(parent="", 
                        index="end", 
                        value=(row.name, row.expiry_date, str(row.quantity)+row.unit))
                

#         #レコードの追加
#         img_path = r"C:\Users\qianq\OneDrive\画像\OCR test\receipt3.png"
#         img = Image.open(img_path)
#         resized_img = img.resize((60, 60))
#         tk_img = ImageTk.PhotoImage(resized_img)

#         for i in range(10):
#             tree.insert(parent="", 
#                         index="end", 
#                         image=tk_img, 
#                         value=("にんじん", "2023/3/3"))
#             tree.insert(parent="", 
#                         index="end", 
#                         image=tk_img, 
#                         value=("かぶ", "2023/3/3"))

        #スクロールバーの作成
        ybar = tk.Scrollbar(self.window, orient="vertical", width=25)

        #スクロールバーとtreeを連動させる
        ybar.config(command=tree.yview)

        #スクロールバーを動かせるようにする
        tree.config(yscrollcommand=ybar.set)

        # ウィジェットの配置
        ybar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    db = Database("mydatabase.db")
    root.geometry("1000x1000")
    root.title("main")
    sub = ListWindow(db)    
    root.mainloop()