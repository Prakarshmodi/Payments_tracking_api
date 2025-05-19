# utils.py
import re

# Input validation functions
def validate_user_input(data):
    errors = {}
    
    # Check required fields
    if not data.get('name') or not data.get('name').strip():
        errors['name'] = "Name is required"
    
    if not data.get('email') or not data.get('email').strip():
        errors['email'] = "Email is required"
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", data.get('email')):
        errors['email'] = "Invalid email format"
    
    if not data.get('phone') or not data.get('phone').strip():
        errors['phone'] = "Phone number is required"
    elif not re.match(r"^\d{10,15}$", data.get('phone').strip()):
        errors['phone'] = "Phone number should be 10-15 digits"
    
    if not data.get('country') or not data.get('country').strip():
        errors['country'] = "Country code is required"
    elif not re.match(r"^[A-Z]{2,3}$", data.get('country')):
        errors['country'] = "Country code should be 2-3 uppercase letters"
    
    return errors

def validate_payment_input(data):
    errors = {}
    
    # Check required fields
    if not data.get('amount'):
        errors['amount'] = "Amount is required"
    else:
        try:
            amount = float(data.get('amount'))
            if amount <= 0:
                errors['amount'] = "Amount must be greater than zero"
        except (ValueError, TypeError):
            errors['amount'] = "Amount must be a valid number"
    

    
    if not data.get('currency') or not data.get('currency').strip():
        errors['currency'] = "Currency is required"
    elif not re.match(r"^[A-Z]{3}$", data.get('currency')):
        errors['currency'] = "Currency code should be 3 uppercase letters"
    
    if not data.get('description'):
        errors['description'] = "Description is required"
    
    if not data.get('card_no') or not data.get('card_no').strip():
        errors['card_no'] = "Card number is required"
    elif not luhn_check(data.get('card_no').replace(' ', '')):
        errors['card_no'] = "Invalid card number (fails Luhn check)"
    
    if not data.get('card_expiry') or not data.get('card_expiry').strip():
        errors['card_expiry'] = "Card expiry date is required"
    elif not re.match(r"^(0[1-9]|1[0-2])\/20[2-9][0-9]$", data.get('card_expiry')):
        errors['card_expiry'] = "Card expiry should be in MM/YYYY format"
    
    if not data.get('card_cvc') or not data.get('card_cvc').strip():
        errors['card_cvc'] = "Card CVC is required"
    elif not re.match(r"^\d{3,4}$", data.get('card_cvc')):
        errors['card_cvc'] = "CVC should be 3-4 digits"
    
    return errors

# Luhn algorithm implementation for card validation
def luhn_check(card_number):
    if not card_number or not card_number.isdigit():
        return False
    
    # Remove any spaces or hyphens
    card_number = card_number.replace(" ", "").replace("-", "")
    
    # Check if the card number is of valid length
    if len(card_number) < 13 or len(card_number) > 19:
        return False
    
    # Reverse the card number
    card_num = [int(d) for d in card_number]
    
    # Double every second digit from right to left
    for i in range(len(card_num) - 2, -1, -2):
        card_num[i] *= 2
        if card_num[i] > 9:
            card_num[i] -= 9
    
    # Sum all digits
    total = sum(card_num)
    
    # If the total is divisible by 10, the number is valid
    return total % 10 == 0

# Card masking function
def mask_card_number(card_number):
    if not card_number:
        return ""
    
    # Remove any spaces or hyphens
    card_number = card_number.replace(" ", "").replace("-", "")
    
    # Keep first 6 and last 4 digits visible, mask the rest
    visible_prefix = card_number[:6]
    visible_suffix = card_number[-4:]
    masked_part = "X" * (len(card_number) - 10)
    
    return f"{visible_prefix}{masked_part}{visible_suffix}"

# Mask CVC completely
def mask_cvc(cvc):
    if not cvc:
        return ""
    return "XXX" if len(cvc) == 3 else "XXXX"