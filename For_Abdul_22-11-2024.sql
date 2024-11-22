-- This is my fourth attempt with more Back and Forth with Chat GPT4 and ClaudAI for copy and paste
-- knowledge / explantations of how make this as "safe" as possible
-- Re-write #5 is to change my variable / column names to be more readable and descriptive
-- Code style should work in PostgreSQL for deployment. Use this style in my Portfolio main project -
-- for linking with the CSV output and the Oracle ALT_VER_input from the XILINIX / LimeSDR combination

-- 1. Creating the 'Customers' table with constraints
CREATE TABLE IF NOT EXISTS Customers (                 -- CREATE TABLE IF NOT EXISTS seems to be the safest way of making tables that I can find
													   -- Should help to reduce the risk of problems further down the line
    Customer_id INT AUTO_INCREMENT PRIMARY KEY,        -- Automatically increments customer ID
    First_name VARCHAR(100) NOT NULL,                   -- Customer first name cannot be NULL ( field input check )
    Fast_name VARCHAR(100) NOT NULL,                    -- Customer last name cannot be NULL ( field input check )
    Email VARCHAR(255) UNIQUE NOT NULL,                 -- Unique email, cannot be NULL ( field input check )
    Phone_number VARCHAR(20),                           -- Optional phone number
    Address TEXT                                        -- Optional address
);

-- 2. Creating the "OrderStatus" table to store valid statuses
CREATE TABLE IF NOT EXISTS OrderStatus (
    Status_id INT AUTO_INCREMENT PRIMARY KEY,
    Status_name VARCHAR(50) UNIQUE NOT NULL
);

-- 3. Creating the "Orders" table with foreign key relationships
CREATE TABLE IF NOT EXISTS Orders (
    Order_id INT AUTO_INCREMENT PRIMARY KEY,           -- Automatically increments order ID
    Customer_id INT,                                    -- Links to customer_id from Customers table
    Order_date DATETIME NOT NULL,                       -- Order date cannot be NULL ( field input check )
    Status_id INT NOT NULL,                             -- Foreign key to OrderStatus
    FOREIGN KEY (Customer_id) REFERENCES Customers(Customer_id) ON DELETE CASCADE,
    -- Without CASCADE, I get an error trying to delete a parent row that has child records.
    -- It is a referential action that you can specify in a foreign key constraint.
    -- It automatically deletes rows from the child table when the corresponding rows in the parent table are deleted.
    -- I still need further understanding as this will probably impact back and forth with Oracle.
    FOREIGN KEY (Status_id) REFERENCES OrderStatus(Status_id) -- Ensure status is valid
);

-- 4. Creating the 'Products' table (assumed structure)
CREATE TABLE IF NOT EXISTS Products (
    Product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    Price DECIMAL(10, 2) NOT NULL,
    Stock_quantity INT NOT NULL CHECK (Stock_quantity >= 0)
);

-- 5. Creating the 'OrderItems' table with foreign key relationships
CREATE TABLE IF NOT EXISTS OrderItems (
    Order_item_id INT AUTO_INCREMENT PRIMARY KEY,       -- Automatically increments order item ID
    Order_id INT,                                       -- Links to order_id from Orders table
    Product_id INT,                                     -- Links to product_id from Products table
    Quantity INT NOT NULL,                              -- Quantity must be greater than 0 ( field value check )
    Price DECIMAL(10, 2) NOT NULL,                      -- Price cannot be NULL ( field input check )
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT
);

-- 6. Inserting sample data (Products, Customers, Orders)
-- Sample products (use prepared statements for real-world scenarios)
INSERT INTO Products (Name, Description, Price, Stock_quantity)
VALUES 
('Laptop', 'High-performance laptop with 128GB RAM', 1500.00, 50),
('Smartphone', 'Latest smartphone with great camera', 800.00, 200),
('Headphones', 'Noise-cancelling wireless headphones', 150.00, 100);

-- Sample customers (use prepared statements for real-world scenarios)
INSERT INTO Customers (First_name, Last_name, Email, Phone_number, Address)
VALUES 
('John', 'Doe', 'john.doe@example.com', '123-456-7890', '123 Main St, Cityville'),
('Jane', 'Smith', 'jane.smith@example.com', '987-654-3210', '456 Elm St, Townville');

-- 7. Inserting sample orders
INSERT INTO Orders (Customer_id, Order_date, Status_id)
VALUES 
(1, '2024-11-01 14:30:00', 1),  -- 'Pending' status, assumed status_id 1
(2, '2024-11-02 16:45:00', 2);  -- 'Shipped' status, assumed status_id 2

-- 8. Inserting order items
INSERT INTO OrderItems (Order_id, Product_id, Quantity, Price)
VALUES 
(1, 1, 1, 1500.00),
(1, 2, 2, 800.00),
(2, 3, 1, 150.00);

-- 9. Updating stock quantity after an order
UPDATE Products p
JOIN OrderItems oi ON p.Product_id = oi.Product_id
SET p.Stock_quantity = p.Stock_quantity - oi.Quantity
WHERE oi.Order_id = 1 AND p.Stock_quantity >= oi.Quantity;





