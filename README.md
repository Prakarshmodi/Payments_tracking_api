# Payment Tracking API

A RESTful API built using Flask and MySQL for managing users and tracking their payments. This API includes robust input validation, error handling, card number validation using the Luhn algorithm, and security features for handling sensitive payment information.

## Features

- Create, read, update, and delete users
- Record and retrieve user payments
- Input validation for all data
- Credit card validation using the Luhn algorithm
- Sensitive data masking (credit card numbers and CVV)
- Comprehensive error handling
- Proper HTTP status codes
- Well-organized code structure

## Project Structure

```
.
├── app.py              # Main Flask application with route handlers
├── config.py           # Database configuration
├── db.py               # Database connection helper
├── models.py           # Database table creation and management
├── utils.py            # Utility functions (validation, masking, etc.)
├── requirements.txt    # Python dependencies
```

## Getting Started

### 1. Set Up MySQL Database

- Create a MySQL database named `payments_db`

### 2. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### User APIs

- **Create User**  
  `POST /users`  
  Body:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9147451517",
    "country": "US"
  }
  ```
  Response (201 Created):
  ```json
  {
    "id": 1,
    "message": "User created successfully"
  }
  ```

- **List Users**  
  `GET /users`  
  Response (200 OK):
  ```json
  [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "9147451517",
      "country": "US",
      "created_at": "2025-05-18T10:30:00",
      "updated_at": "2025-05-18T10:30:00"
    }
  ]
  ```

- **Get User**  
  `GET /users/<user_id>`  
  Response (200 OK):
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9147451517",
    "country": "US",
    "created_at": "2025-05-18T10:30:00",
    "updated_at": "2025-05-18T10:30:00"
  }
  ```

- **Update User**  
  `PUT /users/<user_id>`  
  Body: Same as Create User  
  Response (200 OK):
  ```json
  {
    "message": "User updated successfully"
  }
  ```

- **Delete User**  
  `DELETE /users/<user_id>`  
  Response (200 OK):
  ```json
  {
    "message": "User deleted successfully"
  }
  ```

### Payment APIs

- **Add Payment**  
  `POST /users/<user_id>/payments`  
  Body:
  ```json
  {
    "amount": 100.50,
    "currency": "USD",
    "description": "Test payment",
    "card_no": "4111111111111111",
    "card_expiry": "12/2025",
    "card_cvc": "123"
  }
  ```
  Response (201 Created):
  ```json
  {
    "id": 1,
    "message": "Payment added successfully"
  }
  ```
  Note: Card number will be validated using the Luhn algorithm before storage, and sensitive data will be masked.

- **Get Payments for a User**  
  `GET /users/<user_id>/payments`  
  Response (200 OK):
  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "amount": 100.50,
      "currency": "USD",
      "description": "Test payment",
      "card_no": "411111XXXXXX1111",
      "card_expiry": "12/2025",
      "card_cvc": "XXX",
      "status": "pending",
      "created_at": "2025-05-18T10:35:00"
    }
  ]
  ```

- **Get Specific Payment**  
  `GET /users/<user_id>/payments/<payment_id>`  
  Response (200 OK):
  ```json
  {
    "id": 1,
    "user_id": 1,
    "amount": 100.50,
    "currency": "USD",
    "description": "Test payment",
    "card_no": "411111XXXXXX1111",
    "card_expiry": "12/2025",
    "card_cvc": "XXX",
    "status": "pending",
    "created_at": "2025-05-18T10:35:00"
  }
  ```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400 Bad Request: Invalid input data
- 404 Not Found: Resource not found
- 405 Method Not Allowed: Incorrect HTTP method
- 500 Internal Server Error: Server-side errors

Example error response:
```json
{
  "errors": {
    "email": "Invalid email format",
    "card_no": "Invalid card number (fails Luhn check)"
  }
}
```

## Security Features

- **Luhn Algorithm Validation**: All credit card numbers are validated using the Luhn algorithm before being stored
- **Card Data Masking**: Card numbers are stored in masked format (first 6 and last 4 digits visible)
- **CVC Masking**: CVC/CVV is fully masked before storage

## Requirements

- Python 3.x
- MySQL Server
- Flask
- mysql-connector-python
