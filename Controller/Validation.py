from datetime import datetime
import re

class Validation:
    pass
    
    @staticmethod
    def is_valid_date(date_str):
        # Implement date validation logic
        if isinstance(date_str, datetime):
            return True
        if isinstance(date_str, str):
            # Check if the date string is in the correct format (e.g., YYYY-MM-DD)
            pattern = r'^\d{4}-\d{2}-\d{2}$'
            if re.match(pattern, date_str):
                return True
        return "Invalid date format. Expected YYYY-MM-DD."

    @staticmethod
    def is_valid_email(email_str):
        # Implement email validation logic
        if isinstance(email_str, str):
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(pattern, email_str):
                return True
        return "Invalid email format. Expected format: user@example.com"

    @staticmethod
    def is_valid_password(password):
        # Implement password validation logic
        if isinstance(password, str):
            if len(password) >= 8:
                return True
        return "Invalid password format. Password must be at least 8 characters long."

    @staticmethod
    def is_valid_name(name):
        # Implement name validation logic
        if isinstance(name, str):
            if len(name) > 0 and all(x.isalpha() for x in name):
                return True
        return "Invalid name format. Name must contain only alphabetic characters."

    @staticmethod
    def is_valid_country_code(country_code):
        # Implement country code validation logic
        if isinstance(country_code, str):
            # Match a string starting with '+' followed by 1 to 3 digits
            return bool(re.fullmatch(r"\+\d{1,3}", country_code))
        return "Invalid country code format. Expected format: +123"

    @staticmethod
    def is_valid_phone_number(phone_number):
        # Implement phone validation logic
        if isinstance(phone_number, str):
            # Match a string with 10 to 15 digits
            return bool(re.fullmatch(r"\d{10,15}", phone_number))
        return "Invalid phone number format. Expected format: 1234567890 (with 10 to 15 digits)"

    @staticmethod
    def is_valid_university(university):
        # Implement university validation logic
        if isinstance(university, str):
            if len(university) > 0:
                return True
        return "University name cannot be empty."

    # def is_valid_barcode(barcode):
    #     # Implement barcode validation logic
    #     if isinstance(barcode, str):
    #         if len(barcode) > 0 and all(x.isalnum() for x in barcode):
    #             return True
    #     return False

    @staticmethod
    def is_valid_payment_amount(amount):
        # Implement payment amount validation logic
        if isinstance(amount, (int, float)):
            if amount >= 0:
                return True
        return False

    @staticmethod
    def is_valid_transaction_date(trans_date):
        # Implement transaction date validation logic
        if Validation.is_valid_date(trans_date):
            # Check if the date is not in the future
            if isinstance(trans_date, str):
                trans_date = datetime.strptime(trans_date, "%Y-%m-%d")
            if trans_date > datetime.now():
                return False
            return True
        return False

    @staticmethod
    def is_valid_payment_type(pay_type):
        # Implement payment type validation logic
        if isinstance(pay_type, str):
            if len(pay_type) > 0:
                return True
        return False

    @staticmethod
    def is_valid_course_name(course_name):
        # Implement course name validation logic
        if isinstance(course_name, str):
            if len(course_name) > 0:
                return True
        return False

    @staticmethod
    def is_valid_doctor_id(doc_id):
        # Implement doctor ID validation logic
        if isinstance(doc_id, str):
            if len(doc_id) > 0 and all(x.isalnum() for x in doc_id):
                return True
        return False
    
    @staticmethod
    def is_valid_start_date(start_date):
        # Implement start date validation logic
        if Validation.is_valid_date(start_date):
            # Check if the date is not in the future
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            if start_date > datetime.now():
                return False
            return True
        return False

    @staticmethod
    def is_valid_end_date(end_date):
        # Implement end date validation logic
        if Validation.is_valid_date(end_date):
            return True
        return False