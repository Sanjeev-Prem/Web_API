
# Web_API

## Project Overview
Web_API is a robust RESTful backend designed to manage operations for a restaurant specializing in dosas. This system is built using FastAPI and SQLite to handle CRUD operations effectively for customers, menu items, and orders. It offers a clean interface for users to interact with the backend easily, enhancing the management and accessibility of restaurant data.

## Features
- **Customer Management**: Add, retrieve, update, or delete customer information.
- **Menu Management**: Manage the dosa menu by adding new items, updating existing items, or removing items.
- **Order Management**: Handle customer orders efficiently by creating new orders, updating order details, or deleting orders.

## Setup and Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8 or newer
- SQLite3
- FastAPI
- Uvicorn

### Installation
Clone the repository to your local machine and navigate to the project directory:
```bash
git clone [Your Repository URL]
cd [Your Project Directory]
```

Install the required dependencies:
```bash
pip install fastapi uvicorn sqlite3
```

### Initialize the Database
Run the following command to set up and populate the SQLite database:
```bash
python init_db.py
```

### Running the Application
Start the API server with the following command:
```bash
uvicorn main:app --reload
```
This command will host the server on `http://127.0.0.1:8000`, allowing you to access the API through your web browser.

## API Endpoints
Detailed description of the API endpoints available:

### Customers
- **POST** `/clients/`: Create a new customer with specified details.
- **GET** `/clients/{client_id}`: Retrieve detailed information of a customer by their ID.
- **PUT** `/clients/{client_id}`: Update existing customer information.
- **DELETE** `/clients/{client_id}`: Remove a customer from the database.

### Items
- **POST** `/dishes/`: Add a new menu item to the restaurant's offerings.
- **GET** `/dishes/{dish_id}`: Retrieve details of a specific menu item.
- **PUT** `/dishes/{dish_id}`: Update the information of a menu item.
- **DELETE** `/dishes/{dish_id}`: Delete a menu item from the database.

### Orders
- **POST** `/orders/`: Place a new order by specifying item details and customer ID.
- **GET** `/orders/{order_id}`: Access details of an existing order.
- **PUT** `/orders/{order_id}`: Modify details of an existing order.
- **DELETE** `/orders/{order_id}`: Cancel an existing order.

## Expected Outputs

### API Interaction Examples
- **POST** `/clients/`: Returns the details of the newly created customer.
- **GET** `/clients/{client_id}`: Returns the details of the requested customer, or a 404 error if not found.
- **PUT** `/clients/{client_id}`: Returns the updated customer details.
- **DELETE** `/clients/{client_id}`: Returns a confirmation message on successful deletion.

### Items
- **POST** `/dishes/`: Returns the details of the newly added menu item.
- **GET** `/dishes/{dish_id}`: Returns the details of the requested item, or a 404 error if not found.
- **PUT** `/dishes/{dish_id}`: Returns the updated item details.
- **DELETE** `/dishes/{dish_id}`: Returns a confirmation message on successful deletion.

### Orders
- **POST** `/orders/`: Returns the details of the newly placed order.
- **GET** `/orders/{order_id}`: Returns the details of the existing order, or a 404 error if not found.
- **PUT** `/orders/{order_id}`: Returns the updated order details.
- **DELETE** `/orders/{order_id}`: Returns a confirmation message on successful order cancellation.

## Conclusion
This API serves as a robust backend system for managing a dosa restaurant. It streamlines operations by providing clear interfaces for managing customers, orders, and menu items. The FastAPI framework ensures that the application is fast, reliable, and easy to maintain, making it a valuable tool for restaurant management.
