import tkinter as tk
from tkinter import filedialog
import csv

#ウィンドウの作成
root = tk.Tk()
root.title("家計簿アプリ")
root.geometry("400x350")

#利用するカテゴリ一覧
categories = ["食費", "交際費", "日用品", "ガソリン代", "その他"]

#カテゴリごとの合計を記録する辞書
category_totals = {cat: 0 for cat in categories}
expenses = [] #支出データリスト保存用

#ラベルと入力欄（項目）
tk.Label(root, text = "項目名").grid(row=0, column=0, padx=5, pady=5)
entry_item = tk.Entry(root)
entry_item.grid(row=0, column=1)

#ラベルと入力欄（金額）
tk.Label(root, text = "金額").grid(row=1, column=0, padx=5, pady=5)
entry_amount = tk.Entry(root)
entry_amount.grid(row=1, column=1)

#カテゴリ選択プルダウン
selected_category = tk.StringVar(root)
selected_category.set(categories[0]) #デフォルト
tk.Label(root, text="カテゴリ").grid(row=2, column=0, padx=5, pady=5)
category_menu = tk.OptionMenu(root, selected_category, *categories)
category_menu.grid(row=2, column=1)

#支出表示用　Textウィジェット
text_output = tk.Text(root, height=10, width=45)
text_output.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

#支出追加ボタンの処理
def add_expense():
    item = entry_item.get()
    amount_text = entry_amount.get()
    category = selected_category.get()
    
    if item == "" or not amount_text.isdigit():
        text_output.insert(tk.END, "⚠️入力が不正です。\n")
        return
    
    amount = int(amount_text)
    category_totals[category] += amount
    expenses.append((category, item, amount))
    
    #表示を更新
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, f"【カテゴリ別合計】\n")
    for cat, total in category_totals.items():
        text_output.insert(tk.END, f"・{cat}：{total}円\n")

    #入力欄をクリア
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

#CSVファイルを出力
def save_to_csv():
    #保存先のフォルダを選ぶ
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSVファイル", ".csv")],
        title="保存先を選んでください。",
        initialfile ="kakeibo.csv",
    )

    #キャンセルされたら何もしない
    if not filepath:
        return

    #ファイル書き込み処理
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["カテゴリ", "項目名", "金額"])
        for data in expenses:
            writer.writerow(data)
    text_output.insert(tk.END, "\n ✅️CSVファイルに保存しました。\n")

#追加ボタン
tk.Button(root, text="追加", command=add_expense).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(root, text="CSV出力", command=save_to_csv).grid(row=5, column=0, columnspan=2, pady=10)

#メインループ
root.mainloop()
