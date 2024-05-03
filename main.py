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

