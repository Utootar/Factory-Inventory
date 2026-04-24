# Factory-Inventory
A Python-based Inventory Management System with MySQL database integration for factory stock tracking
# Factory Inventory Management System 🏭

ระบบจัดการคลังสินค้าขนาดเล็ก พัฒนาด้วยภาษา **Python** เชื่อมต่อฐานข้อมูล **MySQL**

##  Features
- **Add Product**: เพิ่มรายชื่อสินค้าเข้าคลัง
- **Calculate Value**: คำนวณมูลค่ารวม (Price * Quantity) อัตโนมัติ
- **Database Integration**: จัดเก็บข้อมูลถาวรใน MySQL
- **User-Friendly GUI**: หน้าจอใช้งานง่ายด้วย Tkinter

##  Tech Stack
- **Language**: Python 3.13
- **Database**: MySQL
- **Libraries**: PyMySQL, Pillow

##  How to use
1. สร้างฐานข้อมูลโดยใช้ไฟล์ `schema.sql` ใน MySQL Workbench
2. ติดตั้ง Library ที่จำเป็น: `pip install -r requirements.txt`
3. รันไฟล์ `LF_KEY.py` เพื่อเริ่มใช้งาน
