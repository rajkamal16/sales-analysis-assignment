import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Creating tables
cur.executescript("""
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS items;

CREATE TABLE customer (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER
);

CREATE TABLE sales (
    sales_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    sales_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (sales_id) REFERENCES sales(sales_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);
""")

# Inserting data
cur.executescript("""
INSERT INTO customer VALUES (1, 21), (2, 23), (3, 35);

INSERT INTO sales VALUES (1, 1), (2, 2), (3, 2), (4, 3), (5, 3);

INSERT INTO items VALUES (1, 'x'), (2, 'y'), (3, 'z');

INSERT INTO orders VALUES 
    (1, 1, 1, 4),  
    (2, 1, 1, 6), 
    (3, 2, 1, 1),  
    (4, 2, 2, 1), 
    (5, 3, 3, 1),  
    (6, 4, 3, 1),  
    (7, 5, 3, 1);  
""")

conn.commit()
conn.close()
