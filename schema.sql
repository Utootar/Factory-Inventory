
Project: Factory Inventory Management System
1. สร้าง Database
CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

2. สร้างตาราง Inventory
CREATE TABLE IF NOT EXISTS Inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) DEFAULT 0.00,
    quantity INT DEFAULT 0,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

3. ข้อมูลตัวอย่างสำหรับทดสอบ (Optional)
INSERT INTO Inventory (product_name, category, price, quantity) VALUES 
('Example Product 1', 'Electronics', 1200.00, 10),
('Example Product 2', 'Stationery', 45.50, 100);