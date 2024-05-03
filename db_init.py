import sqlite3
import json

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite")
curr = conn.cursor()

# Create tables in the database
curr.execute("""
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT
);
""")

curr.execute("""
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
);
""")

curr.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    notes TEXT,
    cust_id INTEGER,
    timestamp INTEGER,
    FOREIGN KEY(cust_id) REFERENCES customers(id)
);
""")

curr.execute("""
CREATE TABLE order_list (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    item_id INTEGER,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
""")

# Load data from JSON file
with open('example_orders.json', 'r') as file:
    order_list = json.load(file)

# Dictionary to hold customers and items to avoid duplicates
customers = {}
items = {}

# Process orders from JSON data
for order in order_list:
    customers[order["phone"]] = order["name"]
    for item in order["items"]:
        items[item["name"]] = item["price"]

# Insert data into the customers table
for phone, name in customers.items():
    curr.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))

# Fetch and print all customers to verify insertion
curr.execute("SELECT * FROM customers")
print("Customers:")
print(curr.fetchall())

# Insert data into the items table
for name, price in items.items():
    curr.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))

# Process each order and its associated items
for order in order_list:
    # Fetch the customer ID based on phone number
    curr.execute("SELECT id FROM customers WHERE phone = ?", (order["phone"],))
    cust_id = curr.fetchone()[0]

    # Insert the order into the orders table
    curr.execute("INSERT INTO orders (notes, timestamp, cust_id) VALUES (?, ?, ?)",
                 (order["notes"], order["timestamp"], cust_id))
    order_id = curr.lastrowid

    # Insert items into the order_list table
    for item in order["items"]:
        curr.execute("SELECT id FROM items WHERE name = ?", (item["name"],))
        item_id = curr.fetchone()[0]
        curr.execute("INSERT INTO order_list (order_id, item_id) VALUES (?, ?)", 
                     (order_id, item_id))

# Commit the transactions
conn.commit()

# Close the database connection
conn.close()
