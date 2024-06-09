# -*- coding: utf-8 -*-
import tkinter as tk
import webbrowser
from urllib.parse import quote
from database import Database

#クラスRecipeの定義
class Recipe:
    def __init__(self,name,ingredients):
        self.name = name 
        self.ingredients = ingredients

class RecipeWindow:
    def __init__(self,db: Database):
        self.db = db
        self.window = tk.Toplevel()
        self.window.title("レシピ検索")
        self.window.geometry("1000x1000")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        
        def open_link(dish):
            query = "{} レシピ".format(dish)
            encoded_query = quote(query)
            webbrowser.open("https://search.yahoo.com/search?p=" + encoded_query)
        karaage = Recipe("唐揚げ",{"鶏もも肉","にんにく"})
        teriyaki = Recipe("照り焼き",{"鶏もも肉"})
        kyabetsu = Recipe("キャベツ",{"キャベツ"})
        tamanegisupu = Recipe("玉ねぎスープ", {"玉ねぎ"})
        itigonodaikonorosi = Recipe("イチゴの大根おろし", {"イチゴ", "大根"})
        sansyokupapurika = Recipe("3色パプリカ", {"レッドパプリカ", "オレンジパプリカ", "イエローパプリカ"})
        imozanmai = Recipe("芋三昧", {"サツマイモ", "サトイモ", "ジャガイモ"})
        mamezanmai = Recipe("豆三昧", {"エンドウマメ", "グリーンピース", "ソラマメ"})
        takenokogohan = Recipe("タケノコご飯", {"タケノコ", "米"})
        furufuru = Recipe("フルフル", {"きくらげ", "びわ", "オクラ"})
        kyuritataki = Recipe("きゅうり叩き", {"きゅうり"})
        furutuponti = Recipe("フルーツポンチ", {"マンゴー", "ブルーベリー", "スイカ", "メロン"})
        kare = Recipe("カレー", {"ジャガイモ", "にんじん", "玉ねぎ"})
        kinpira = Recipe("きんぴら", {"ジャガイモ", "にんじん", "玉ねぎ"})
        yasaitobekonitame = Recipe("野菜とベーコン炒め", {"にんじん", "じゃがいも", "玉ねぎ"})
        pariparigaretto = Recipe("パリパリガレット", {"にんじん", "ジャガイモ", "玉ねぎ"})
        tamanegitoninjinnohassyudopoku = Recipe("玉ねぎとにんじんのハッシュドポーク", {"玉ねぎ", "ジャガイモ", "にんじん"})
        self.recipes = {karaage, teriyaki, kyabetsu, tamanegisupu,itigonodaikonorosi,sansyokupapurika,imozanmai, mamezanmai,takenokogohan, furufuru, kyuritataki, furutuponti, kare, kinpira, yasaitobekonitame, pariparigaretto, tamanegitoninjinnohassyudopoku}
        self.ingredients = {row.name for row in self.db.get_all_products()}
        search_result = find_recipe(self.ingredients, self.recipes)
        for j in range(len(search_result)):
            exec('self.TitleLabel{} = tk.Label(self.window,text="{}",font=("Helvetica","15"))'.format(j,search_result[j].name))
            exec("self.TitleLabel{}.grid(row={},column=0, sticky=tk.W)".format(j,j))
            #フレームjに移動するボタン
            exec('self.Button{} = tk.Button(self.window,text="Go to recipe", command=lambda:open_link("{}"))'.format(j,search_result[j].name),locals(),globals())
            exec("self.Button{}.grid(row={},column=1, sticky=tk.W)".format(j,j))

        #手持ちの材料リスト(my_ingredients)が材料リストを包含してる
        # 場合、そのレシピを表示させる関数

def find_recipe(my_ingredients,recipes):
    can_make = []
    for recipe in recipes:
        if(my_ingredients >= recipe.ingredients):
            can_make.append(recipe)
    return can_make

if __name__ == "__main__":
    root = tk.Tk()
    db = Database("mydatabase.db")
    root.geometry("1000x1000")
    root.title("main")
    sub = RecipeWindow(db)    
    root.mainloop()
