from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import time

app = FastAPI(title="Dosa Restaurant API")

class Client(BaseModel):
    client_id: int | None = None
    full_name: str
    contact_number: str

class Dish(BaseModel):
    dish_id: int | None = None
    dish_title: str
    dish_price: float

class ClientOrder(BaseModel):
    order_id: int | None = None
    remarks: str
    client_id: int
    order_time: int

def get_db_connection():
    conn = sqlite3.connect("restaurant_db.sqlite")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@app.post("/clients/")
def create_client(client: Client):
    if client.client_id is not None:
        raise HTTPException(status_code=400, detail="ID should not be provided for creation.")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Clientele (ClientName, PhoneNumber) VALUES (?, ?);", (client.full_name, client.contact_number))
    client.client_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return client

@app.get("/clients/{client_id}")
def get_client(client_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ClientID, ClientName, PhoneNumber FROM Clientele WHERE ClientID = ?", (client_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return Client(client_id=result[0], full_name=result[1], contact_number=result[2])
    else:
        raise HTTPException(status_code=404, detail="Client not found")

@app.put("/clients/{client_id}")
def update_client(client_id: int, client: Client):
    conn = get_db_connection()
    cursor = conn.cursor()
    update_query = "UPDATE Clientele SET "
    update_data = []
    if client.full_name:
        update_query += "ClientName=?, "
        update_data.append(client.full_name)
    if client.contact_number:
        update_query += "PhoneNumber=? "
        update_data.append(client.contact_number)
    update_query = update_query.rstrip(", ") + "WHERE ClientID=?;"
    update_data.append(client_id)
    cursor.execute(update_query, update_data)
    conn.commit()
    cursor.execute("SELECT ClientID, ClientName, PhoneNumber FROM Clientele WHERE ClientID = ?", (client_id,))
    updated_client = cursor.fetchone()
    conn.close()
    return Client(client_id=updated_client[0], full_name=updated_client[1], contact_number=updated_client[2])

@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientele WHERE ClientID = ?;", (client_id,))
    conn.commit()
    changes = conn.total_changes
    conn.close()
    if changes:
        return {"message": "Client deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")

#Cred Operations for Items

@app.post("/dishes/")
def create_dish(dish: Dish):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Dishes (DishTitle, DishPrice) VALUES (?, ?);", (dish.dish_title, dish.dish_price))
    dish.dish_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return dish

@app.get("/dishes/{dish_id}")
def get_dish(dish_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DishID, DishTitle, DishPrice FROM Dishes WHERE DishID = ?", (dish_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return Dish(dish_id=result[0], dish_title=result[1], dish_price=result[2])
    else:
        raise HTTPException(status_code=404, detail="Dish not found")

@app.put("/dishes/{dish_id}")
def update_dish(dish_id: int, dish: Dish):
    conn = get_db_connection()
    cursor = conn.cursor()
    update_query = "UPDATE Dishes SET "
    update_data = []
    if dish.dish_title:
        update_query += "DishTitle=?, "
        update_data.append(dish.dish_title)
    if dish.dish_price is not None:
        update_query += "DishPrice=? "
        update_data.append(dish.dish_price)
    update_query = update_query.rstrip(", ") + "WHERE DishID=?;"
    update_data.append(dish_id)
    cursor.execute(update_query, update_data)
    conn.commit()
    cursor.execute("SELECT DishID, DishTitle, DishPrice FROM Dishes WHERE DishID = ?", (dish_id,))
    updated_dish = cursor.fetchone()
    conn.close()
    return Dish(dish_id=updated_dish[0], dish_title=updated_dish[1], dish_price=updated_dish[2])

@app.delete("/dishes/{dish_id}")
def delete_dish(dish_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Dishes WHERE DishID = ?;", (dish_id,))
    conn.commit()
    changes = conn.total_changes
    conn.close()
    if changes:
        return {"message": "Dish deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    #Cred Operations for Orders

@app.post("/orders/")
def create_order(order: ClientOrder):
    if order.order_id is not None:
        raise HTTPException(status_code=400, detail="Order ID should not be set on creation.")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO FoodOrders (Remarks, ClientID, OrderTime) VALUES (?, ?, ?);",
                   (order.remarks, order.client_id, int(time.time())))
    order.order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT FoodOrderID, Remarks, ClientID, OrderTime FROM FoodOrders WHERE FoodOrderID = ?", (order_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return ClientOrder(order_id=result[0], remarks=result[1], client_id=result[2], order_time=result[3])
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: ClientOrder):
    conn = get_db_connection()
    cursor = conn.cursor()
    update_query = "UPDATE FoodOrders SET "
    update_data = []
    if order.remarks:
        update_query += "Remarks=?, "
        update_data.append(order.remarks)
    update_query = update_query.rstrip(", ") + "WHERE FoodOrderID=?;"
    update_data.append(order_id)
    cursor.execute(update_query, update_data)
    conn.commit()
    cursor.execute("SELECT FoodOrderID, Remarks, ClientID, OrderTime FROM FoodOrders WHERE FoodOrderID = ?", (order_id,))
    updated_order = cursor.fetchone()
    conn.close()
    return ClientOrder(order_id=updated_order[0], remarks=updated_order[1], client_id=updated_order[2], order_time=updated_order[3])

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM FoodOrders WHERE FoodOrderID = ?;", (order_id,))
    conn.commit()
    changes = conn.total_changes
    conn.close()
    if changes:
        return {"message": "Order deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Order not found")

