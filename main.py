import tkinter as tk
from tkinter import ttk
from mainwindow import MainWindow

def main():
    # データベースを初期化する
    dbname = "mydatabase.db"

    # アプリのメインウィンドウを作成する
    main_window = MainWindow(dbname)
    main_window.mainloop()

if __name__ == "__main__":
    main()
