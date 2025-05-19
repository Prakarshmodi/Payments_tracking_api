from flask import Flask, request, jsonify
from db import get_db_connection
from utils import (
    validate_user_input, 
    validate_payment_input, 
    mask_card_number, 
    mask_cvc
)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Welcome to the Payment Tracking API',
        'documentation': 'See README.md for API documentation',
        'endpoints': {
            'users': '/users',
            'payments': '/users/<user_id>/payments',
            'health': '/health'
        }
    }), 200


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({"error": "An internal server error occurred"}), 500
    wrapper.__name__ = func.__name__
    return wrapper

# Create a user
@app.route('/users', methods=['POST'])
@handle_exceptions
def create_user():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validate input
    errors = validate_user_input(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    # Process valid data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, phone, country) VALUES (%s, %s, %s, %s)",
                   (data['name'], data['email'], data['phone'], data['country']))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'id': user_id, 'message': 'User created successfully'}), 201

# List all users
@app.route('/users', methods=['GET'])
@handle_exceptions
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(users), 200

# Get a specific user
@app.route('/users/<int:user_id>', methods=['GET'])
@handle_exceptions
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user), 200

# Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
@handle_exceptions
def update_user(user_id):
    # Verify user exists
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    if not data:
        cursor.close()
        conn.close()
        return jsonify({"error": "No data provided"}), 400
    
    # Validate input
    errors = validate_user_input(data)
    if errors:
        cursor.close()
        conn.close()
        return jsonify({"errors": errors}), 400
    
    # Update user
    cursor.execute("UPDATE users SET name=%s, email=%s, phone=%s, country=%s WHERE id=%s",
                   (data['name'], data['email'], data['phone'], data['country'], user_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'User updated successfully'}), 200

# Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
@handle_exceptions
def delete_user(user_id):
    # Verify user exists
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    # Delete user
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'User deleted successfully'}), 200

# Add payment
@app.route('/users/<int:user_id>/payments', methods=['POST'])
@handle_exceptions
def add_payment(user_id):
    # Verify user exists
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    if not data:
        cursor.close()
        conn.close()
        return jsonify({"error": "No data provided"}), 400
    
    # Validate payment input
    errors = validate_payment_input(data)
    if errors:
        cursor.close()
        conn.close()
        return jsonify({"errors": errors}), 400
    
    # Store payment with masked card data
    masked_card = mask_card_number(data['card_no'])
    masked_cvc = mask_cvc(data['card_cvc'])
    
    cursor.execute("""INSERT INTO payments 
        (user_id, amount, currency, description, card_no, card_expiry, card_cvc)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (user_id, data['amount'], data['currency'], data['description'],
         masked_card, data['card_expiry'], masked_cvc))
    
    conn.commit()
    payment_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({
        'id': payment_id,
        'message': 'Payment added successfully'
    }), 201

# Get all payments for a user
@app.route('/users/<int:user_id>/payments', methods=['GET'])
@handle_exceptions
def get_payments(user_id):
    # Verify user exists
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    # Get payments
    cursor.execute("SELECT * FROM payments WHERE user_id=%s", (user_id,))
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(payments), 200

# Get a specific payment
@app.route('/users/<int:user_id>/payments/<int:payment_id>', methods=['GET'])
@handle_exceptions
def get_payment(user_id, payment_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Verify user exists
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    # Get payment
    cursor.execute("SELECT * FROM payments WHERE id=%s AND user_id=%s", (payment_id, user_id))
    payment = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    
    return jsonify(payment), 200

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

# Custom 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "The requested resource was not found"}), 404

# Custom 405 handler
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(debug=True)