import sqlite3
from typing import List, Tuple
from tkinter import messagebox

class Product:
    def __init__(self, id: int, name: str, purchase_date: Tuple[int, int, int], expiry_type: int, expiry_date: Tuple[int, int, int], quantity: float, unit: str, imagefile: str, note: str):
        self.id = id
        self.name = name
        self.purchase_date = purchase_date
        self.expiry_type = expiry_type
        self.expiry_date = expiry_date
        self.quantity = quantity
        self.unit = unit
        self.imagefile = imagefile
        self.note = note

    def to_tuple(self) -> Tuple:
        return (self.id, self.name, str(self.purchase_date), self.expiry_type, str(self.expiry_date), self.quantity, self.unit, self.imagefile, self.note)
    
    @classmethod
    def from_tuple(cls, data: Tuple):
        id, name, purchase_date, expiry_type, expiry_date, quantity, unit, imagefile, note = data
        return cls(id, name, purchase_date, expiry_type, expiry_date, quantity, unit, imagefile, note)
    
class Database:
    def __init__(self, filename: str):
        self.conn = sqlite3.connect(filename)
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS products (
                     id INTEGER PRIMARY KEY,
                     name TEXT not NULL,
                     purchase_date TEXT,
                     expiry_type TEXT,
                     expiry_date TEXT,
                     quantity REAL not NULL,   
                     unit TEXT,
                     image TEXT,
                     note TEXT
                     )""")
        self.conn.commit()
    
    def insert_product(self, product: Product):
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO products (name, purchase_date, expiry_type, expiry_date, quantity, unit, image, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", product.to_tuple()[1:])
            self.conn.commit()
            messagebox.showinfo('Success', 'Product added successfully')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def delete_product(self, product: Product):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM products WHERE id=?", (product.id,))
            self.conn.commit()
            messagebox.showinfo('Success', 'Product deleted successfully')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def update_product(self, product: Product):
        try:
            c = self.conn.cursor()
            c.execute("UPDATE products SET name=?, purchase_date=?, expiry_type=?, expiry_date=?, quantity=?, unit=?, image=?, note=? WHERE id=?", (product.to_tuple()[1:] + (product.id, )))
            self.conn.commit()
            messagebox.showinfo('Success', 'Product updated successfully')
        except Exception as e:
            messagebox.showerror('Error', str(e))
        
    def get_all_products(self) -> List[Product]:
        c = self.conn.cursor()
        c.execute("SELECT * FROM products")
        rows = c.fetchall()
        return [Product.from_tuple(row) for row in rows]
    
    def search_products_by_name(self, name: str) -> List[Product]:
        c = self.conn.cursor()
        c.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{name}%",))
        rows = c.fetchall()
        return [Product.from_tuple(row) for row in rows]
    
    def get_product_by_id(self, id: int) -> Product:
        c = self.conn.cursor()
        c.execute("SELECT * FROM products WHERE id=?", (id,))
        row = c.fetchone()
        if row is not None:
            return Product.from_tuple(row)
        else:
            return None

    def __del__(self):
        self.conn.close()

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
