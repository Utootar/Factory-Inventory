import tkinter as tk
from tkinter import messagebox
import pymysql
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='56472000sql',
        db='lfgoon' 
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
            cursor.execute(sql, (name.title(), int(qty), float(price), cat))
        conn.commit()
        conn.close()
        load_data()
        messagebox.showinfo("Success", f"เพิ่ม {name} Add in Inventory")
        entry_name.delete(0, tk.END)
        entry_qty.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        selected_category.set("Select Category")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot Connect: {e}")

def search_product(event=None):
    search_query = entry_search.get().strip().lower() # ดึงข้อความจากช่องค้นหา
    
    # ล้างตารางก่อนโชว์ผลการค้นหา
    for i in tree.get_children():
        tree.delete(i)
        
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # ใช้ SQL LIKE เพื่อค้นหาคำที่ใกล้เคียง
            sql = "SELECT product_id, product_name, quantity, unit_price, category FROM inventory WHERE LOWER(product_name) LIKE %s"
            cursor.execute(sql, (f"%{search_query}%",))
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"ค้นหาไม่ได้: {e}")

def show_summary():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            
            sql = """
            SELECT 
                COUNT(*) as total_items, 
                SUM(quantity * unit_price) as total_value 
            FROM inventory
            """
            cursor.execute(sql)
            result = cursor.fetchone() 
            
            total_items = result[0] or 0
            total_value = result[1] or 0
            
            # โชว์ Dashboard แบบสรุปผล
            summary_text = (
                f"📊 สรุปข้อมูลในคลัง:\n\n"
                f"🔹 จำนวนรายการสินค้าทั้งหมด: {total_items} รายการ\n"
                f"💰 มูลค่าสินค้ารวมทั้งคลัง: {total_value:,.2f} บาท"
            )
            messagebox.showinfo("Inventory Dashboard", summary_text)
            
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"ไม่สามารถดึงข้อมูลได้: {e}")

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT product_id, product_name, quantity, unit_price, category FROM Inventory")
            rows = cursor.fetchall()
            print(f"DEBUG: ดึงข้อมูลมาได้ทั้งหมด {len(rows)} แถว") # <--- เติมบรรทัดนี้
            for row in rows:
                print(f"DEBUG: กำลังใส่ข้อมูล -> {row}") # <--- เติมบรรทัดนี้
                tree.insert("", tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Debug Error", f"เกิดปัญหาตอนโหลดข้อมูล: {e}") # <--- เปลี่ยนจาก print เป็น messagebox

def delete_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "กรุณาเลือกสินค้า!")
        return

    item_data = tree.item(selected_item)['values']
    p_id = item_data[0] # อันนี้คือค่า product_id จากแถวที่เลือก

    if messagebox.askyesno("Confirm", f"จะลบ {item_data[1]} ใช่หรือไม่?"):
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                # เปลี่ยนจาก id = %s เป็น product_id = %s
                cursor.execute("DELETE FROM inventory WHERE product_id = %s", (p_id,))
            conn.commit()
            conn.close()
            load_data()
            messagebox.showinfo("Success", "ลบเรียบร้อย!")
        except Exception as e:
            messagebox.showerror("Error", f"ลบไม่ได้: {e}")      

# --- สร้างหน้าต่าง (GUI) ---

root = tk.Tk()
root.title("ระบบคลังสินค้า LF")
root.geometry("850x700")
root.configure(bg="#f4f7f6")


try:
    img_icon = tk.PhotoImage(file=resource_path("favicon.png"))
    root.iconphoto(False, img_icon)
except:
    pass

try:       
        img = Image.open(resource_path("fac.jpg"))
        img = img.resize((80, 80)) # ปรับขนาด
        logo_img = ImageTk.PhotoImage(img)

        tk.Label(root, image=logo_img, bg="#f8f9fa").pack(pady=5)
except:
        tk.Label(root, text="🏢", font=("Arial", 30), bg="#f8f9fa").pack()
tk.Label(root, text="FACTORY INVENTORY", font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#333").pack()

tk.Label(root, text="📦 ระบบจัดการคลังสินค้า", font=("Arial", 16, "bold")).pack(pady=20)

# ส่วนรับข้อมูล

input_frame = tk.LabelFrame(root, text=" 📝 ข้อมูลสินค้าใหม่ ", font=("Helvetica", 10, "bold"), padx=15, pady=15, bg="white", fg="#34495e", relief="flat", highlightbackground="#dcdde1", highlightthickness=1)
input_frame.pack(pady=10, padx=25, fill="x")


# ปรับ Font และสีสำหรับ Label และ Entry
label_font = ("Helvetica", 10)
entry_font = ("Helvetica", 10)
fg_color = "#2c3e50"

# กำหนด Grid Layout สำหรับ Input
tk.Label(input_frame, text="ชื่อสินค้า:", font=label_font, bg="white", fg=fg_color).grid(row=0, column=0, sticky="w", pady=8, padx=5)
entry_name = tk.Entry(input_frame, width=25, font=entry_font, relief="solid", highlightthickness=1, highlightbackground="#dcdde1")
entry_name.grid(row=0, column=1, pady=8, padx=5)

tk.Label(input_frame, text="จำนวน:", font=label_font, bg="white", fg=fg_color).grid(row=1, column=0, sticky="w", pady=8, padx=5)
entry_qty = tk.Entry(input_frame, width=25, font=entry_font, relief="solid", highlightthickness=1, highlightbackground="#dcdde1")
entry_qty.grid(row=1, column=1, pady=8, padx=5)

tk.Label(input_frame, text="ราคา (บาท):", font=label_font, bg="white", fg=fg_color).grid(row=2, column=0, sticky="w", pady=8, padx=5)
entry_price = tk.Entry(input_frame, width=25, font=entry_font, relief="solid", highlightthickness=1, highlightbackground="#dcdde1")
entry_price.grid(row=2, column=1, pady=8, padx=5)

tk.Label(input_frame, text="ประเภท:", font=label_font, bg="white", fg=fg_color).grid(row=3, column=0, sticky="w", pady=8, padx=5)
categories = ["Food", "Beverage", "Household", "Personal Care", "Snack"]
selected_category = tk.StringVar(value="Select Category")
dropdown = tk.OptionMenu(input_frame, selected_category, *categories)
dropdown.config(width=21, font=entry_font, bg="white", relief="solid")
dropdown.grid(row=3, column=1, pady=8, padx=5)



# --- 3. ส่วนปุ่มกด (Action Buttons - Grid and Space) ---
btn_frame = tk.Frame(root, bg="#f4f7f6")
btn_frame.pack(pady=10,fill="x")

# กำหนดสไตล์ปุ่มแบบ 
btn_font = ("Helvetica", 10, "bold")

# ปุ่มเพิ่มสินค้า 
btn_add = tk.Button(btn_frame, text="📥 เพิ่มสินค้า", command=add_product, bg="#3498db", fg="white", font=btn_font, width=15, relief="flat", activebackground="#2980b9", activeforeground="white")
btn_add.grid(row=0, column=0, padx=10)

# ปุ่มดูสรุปผล 
btn_sum = tk.Button(btn_frame, text="📊 ดูสรุปผล", command=show_summary, bg="#2ecc71", fg="white", font=btn_font, width=15, relief="flat", activebackground="#27ae60", activeforeground="white")
btn_sum.grid(row=0, column=1, padx=10)

# ปุ่มลบข้อมูล 
btn_del = tk.Button(root, text="🗑️ ลบสินค้าที่เลือก", command=delete_product, bg="#e74c3c", fg="white", font=btn_font, width=33, relief="flat", activebackground="#c0392b", activeforeground="white")
btn_del.pack(pady=5)

# --- ส่วนค้นหา (Search Section) ---
search_frame = tk.Frame(root, bg="#f4f7f6")
search_frame.pack(pady=10, padx=25, fill="x")

tk.Label(search_frame, text="🔍 ค้นหาชื่อสินค้า:", font=("Helvetica", 10), bg="#f4f7f6").pack(side="left", padx=5)
entry_search = tk.Entry(search_frame, font=("Helvetica", 10), relief="solid", highlightthickness=1, highlightbackground="#dcdde1")
entry_search.pack(side="left", fill="x", expand=True, padx=5)

entry_search.bind("<KeyRelease>", search_product)


columns = ("ID", "Name", "Qty", "Price", "Category")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

# กำหนดสไตล์สำหรับ Treeview 
style = ttk.Style()
style.theme_use("clam") # ใช้ Theme clam เพื่อการปรับแต่งที่ดีที่สุด
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#dcdde1", foreground="#2c3e50")
style.configure("Treeview", font=("Helvetica", 10), rowheight=28) # ขยายความสูงแถว
style.map("Treeview", background=[('selected', '#3498db')]) # สีเมื่อเลือกแถว

# ตั้งหัวตารางและกำหนดความกว้าง
tree.heading("ID", text="ID", anchor="center")
tree.heading("Name", text="Name", anchor="w")
tree.heading("Qty", text="Qty", anchor="center")
tree.heading("Price", text="Price", anchor="e")
tree.heading("Category", text="Category", anchor="w")

tree.column("ID", width=40, anchor="center")
tree.column("Name", width=300, anchor="w")
tree.column("Qty", width=60, anchor="center")
tree.column("Price", width=90, anchor="e")
tree.column("Category", width=200, anchor="w")


scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(pady=10, padx=25, fill="both", expand=True) # ให้ตารางขยายได้
scrollbar.pack(side="right", fill="y")

load_data()
root.mainloop()
