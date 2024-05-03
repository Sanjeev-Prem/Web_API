import sqlite3
import json

# Connecting to the SQLite database
database = sqlite3.connect("restaurant_db.sqlite")
db_cursor = database.cursor()

# Creating database tables with modified names and data types
db_cursor.execute("""
CREATE TABLE Clientele (
    ClientID INTEGER PRIMARY KEY,
    ClientName VARCHAR(100),
    PhoneNumber VARCHAR(15)
);
""")

db_cursor.execute("""
CREATE TABLE Dishes (
    DishID INTEGER PRIMARY KEY,
    DishTitle VARCHAR(100),
    DishPrice DECIMAL(10, 2)
);
""")

db_cursor.execute("""
CREATE TABLE FoodOrders (
    FoodOrderID INTEGER PRIMARY KEY,
    ClientRemarks TEXT,
    LinkedClientID INTEGER,
    OrderPlacedAt BIGINT,
    FOREIGN KEY(LinkedClientID) REFERENCES Clientele(ClientID)
);
""")

db_cursor.execute("""
CREATE TABLE OrderDetails (
    DetailID INTEGER PRIMARY KEY,
    LinkedOrderID INTEGER,
    LinkedDishID INTEGER,
    FOREIGN KEY(LinkedOrderID) REFERENCES FoodOrders(FoodOrderID),
    FOREIGN KEY(LinkedDishID) REFERENCES Dishes(DishID)
);
""")

# Load and insert data from JSON file
with open('example_orders.json', 'r') as file:
    order_data = json.load(file)

clients = {}
dishes = {}

for order in order_data:
    clients[order["phone"]] = order["name"]
    for item in order["items"]:
        if item["name"] not in dishes:
            dishes[item["name"]] = item["price"]

for phone, name in clients.items():
    db_cursor.execute("INSERT INTO Clientele (ClientName, PhoneNumber) VALUES (?, ?);", (name, phone))

for dish_name, price in dishes.items():
    db_cursor.execute("INSERT INTO Dishes (DishTitle, DishPrice) VALUES (?, ?);", (dish_name, price))

for order in order_data:
    db_cursor.execute("SELECT ClientID FROM Clientele WHERE PhoneNumber=?;", (order["phone"],))
    client_id = db_cursor.fetchone()[0]
    db_cursor.execute("INSERT INTO FoodOrders (ClientRemarks, OrderPlacedAt, LinkedClientID) VALUES (?, ?, ?);",
                      (order["notes"], order["timestamp"], client_id))
    order_id = db_cursor.lastrowid
    for item in order["items"]:
        db_cursor.execute("SELECT DishID FROM Dishes WHERE DishTitle=?;", (item["name"],))
        dish_id = db_cursor.fetchone()[0]
        db_cursor.execute("INSERT INTO OrderDetails (LinkedOrderID, LinkedDishID) VALUES (?, ?);",
                          (order_id, dish_id))

# Commit changes and close the database connection
database.commit()
database.close()
