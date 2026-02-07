# Flask REST API Documentation

This project is a simple **Flask REST API** with CRUD operations for **Users, Products, Orders**


---

## Authentication

### Register a New User
**Endpoint:** `POST /register`  
**Request JSON:**
```
{
  "username": "your_username",
  "fullname": "Your Full Name",
  "email": "your_email@example.com",
  "password": "your_password"
}
```
**Response 201 Created:**
```
{
  "status": "success",
  "data": {
    "username": "your_username",
    "fullname": "Your Full Name",
    "email": "your_email@example.com"
  }
}
```
**Response 400 Bad Request (example):**
```
{
  "status": "failed",
  "message": "Password must be at least 6 characters"
}
```

### Login
**Endpoint:** `POST /login`  
**Request JSON:**
```
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```
**Response 200 OK:**
```
{
  "status": "success",
  "data": {
    "user": {
      "id": user_id,
      "username": "your_username",
      "email": "your_email@example.com"
    },
    "token": "JWT_TOKEN"
  }
}
```
> **Note:** Use the returned token as a Bearer token for authenticated requests:
```
Authorization: Bearer JWT_TOKEN
```

---

## Users Endpoints

> All User endpoints require Bearer token authentication.

### List Users
```
GET /users/
```
**Response:**
```
{
  "status": "success",
  "users": [
    {
      "id": user_id,
      "username": "username",
      "fullname": "Full Name",
      "email": "email@example.com"
    }
  ]
}
```

### Get User by ID
```
GET /users/<user_id>
```
**Response:**
```
{
  "status": "success",
  "user": "your_username",
  "data": {
    "id": user_id,
    "username": "username",
    "fullname": "Full Name",
    "email": "email@example.com"
  }
}
```

### Create User
```
POST /users/
```
**Request JSON:**
```
{
  "username": "new_username",
  "fullname": "New Full Name",
  "email": "new_email@example.com",
  "password": "password"
}
```
**Response 201 Created:**
```
{
  "status": "success",
  "message": "User new_username created"
}
```

### Update User
```
PUT /users/<user_id>
```
**Request JSON:**
```
{
  "fullname": "Updated Full Name",
  "email": "updated_email@example.com"
}
```
**Response 200 OK:**
```
{
  "status": "success",
  "message": "User username updated"
}
```

### Delete User
```
DELETE /users/<user_id>
```
**Response 200 OK:**
```
{
  "status": "success",
  "message": "User username deleted"
}
```

---

## Products Endpoints

> All Product endpoints require Bearer token authentication.

### List Products
```
GET /product
```
**Response:**
```
{
  "status": "success",
  "user": "your_username",
  "products": [
    {
      "id": product_id,
      "name": "Product Name",
      "description": "Product Description",
      "stock": stock_quantity,
      "price": price
    }
  ]
}
```

### Get Product by ID
```
GET /product/<product_id>
```
**Response:**
```
{
  "status": "success",
  "user": "your_username",
  "product": {
    "id": product_id,
    "name": "Product Name",
    "description": "Product Description",
    "stock": stock_quantity,
    "price": price
  }
}
```

### Create Product
```
POST /product
```
**Request JSON:**
```
{
  "name": "Product Name",
  "description": "Product Description",
  "stock": stock_quantity,
  "price": price
}
```
**Response 201 Created:**
```
{
  "status": "success",
  "message": "Product Product Name created by your_username"
}
```

### Update Product
```
PUT /product/<product_id>
```
**Request JSON:**
```
{
  "stock": updated_stock,
  "price": updated_price
}
```
**Response 200 OK:**
```
{
  "status": "success",
  "message": "Product Product Name updated by your_username"
}
```

### Delete Product
```
DELETE /product/<product_id>
```
**Response 200 OK:**
```
{
  "status": "success",
  "message": "Product Product Name deleted by your_username"
}
```

---

## Orders Endpoints

> All Order endpoints require Bearer token authentication.

### List Orders
```
GET /order
```
**Response:**
```
{
  "status": "success",
  "user": "your_username",
  "orders": [
    {
      "id": order_id,
      "customer_name": "Customer Name",
      "created_at": "ISO Timestamp",
      "total_price": total_price,
      "items": [
        {
          "product_id": product_id,
          "quantity": quantity,
          "price": price
        }
      ]
    }
  ]
}
```

### Get Order by ID
```
GET /order/<order_id>
```
**Response:**
```
{
  "status": "success",
  "user": "your_username",
  "order": {
    "id": order_id,
    "customer_name": "Customer Name",
    "status": "order_status",
    "created_at": "ISO Timestamp",
    "total_price": total_price,
    "items": [
      {
        "product_id": product_id,
        "quantity": quantity,
        "price": price
      }
    ]
  }
}
```

### Create Order
```
POST /order
```
**Request JSON:**
```
{
  "customer_name": "Customer Name",
  "items": [
    {"product_id": product_id, "quantity": quantity, "price": price}
  ]
}
```
**Response 201 Created:**
```
{
  "status": "success",
  "message": "Order order_id created by your_username",
  "order_id": order_id
}
```

### Update Order
```
PUT /order/<order_id>
```
**Request JSON:**
```
{
  "status": "order_status",
  "items": [
    {"product_id": product_id, "quantity": quantity, "price": price}
  ]
}
```
**Response 200 OK:**
```
{
  "status": "success",
  "message": "Order order_id updated by your_username",
  "order_id": order_id
}
```

### Delete Order
```
DELETE /order/<order_id>
```
**Response 200 OK:**
```
{
  "status": "success",
  "message": "Order order_id deleted by your_username"
}
```

---

## Authorization Header Example
For endpoints requiring authentication:
```
GET /order
Authorization: Bearer JWT_TOKEN
```

---

## Notes
- All endpoints return JSON responses.
- Errors return a structure like:
```
{
  "status": "error",
  "message": "Description of the error"
}
```

