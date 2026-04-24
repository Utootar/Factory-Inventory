import tkinter as tk
from tkinter import messagebox
import pymysql


def get_connection():
    return pymysql.connect(
        host='Your server',
        user='Your Username',
        password='Your password',
        db='your database' 
    )

def add_product():
    name = entry_name.get().strip()
    qty = entry_qty.get().strip()
    price = entry_price.get().strip()
    cat = selected_category.get()
    if name == "" or qty == "" or price ==""or cat == "Select Category":
        messagebox.showwarning("Warning", "Please complete all required fields!!")
        return
    
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO inventory (product_name, quantity, unit_price, category) 
            VALUES (%s, %s, %s,%s)
            ON DUPLICATE KEY UPDATE 
                quantity = quantity + VALUES(quantity),
                unit_price = VALUES(unit_price),
                category = VALUES(category) 
            """
            cursor.execute(sql, (name.title(), int(qty), int(price), cat))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"เพิ่ม {name} Add in Inventory")
        entry_name.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        selected_category.set("Select Category")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot Connect: {e}")

# --- สร้างหน้าต่าง (GUI) ---

root = tk.Tk()
root.title("ระบบคลังสินค้า LF")
root.geometry("400x400")

# ส่วนรับข้อมูล
tk.Label(root, text="📦 ระบบจัดการคลังสินค้า", font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(root, text="ชื่อสินค้า:").pack()
entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)

tk.Label(root, text="จำนวน:").pack()
entry_qty = tk.Entry(root, width=30)
entry_qty.pack(pady=5)

tk.Label(root, text="ราคา:").pack()
entry_price = tk.Entry(root, width=30)
entry_price.pack(pady=5)

tk.Label(root, text="ประเภทสินค้า:").pack()

categories = ["Food", "Beverage", "Household", "Personal Care","Snack"]
selected_category = tk.StringVar()
selected_category.set("Select Category")

dropdown = tk.OptionMenu(root, selected_category, *categories)
dropdown.config(width=25)
dropdown.pack(pady=5)

# ปุ่มกด
tk.Button(root, text="เพิ่มสินค้า", command=add_product, bg="blue", fg="white", width=20).pack(pady=20)

root.mainloop()