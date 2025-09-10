import random

names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
    "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]

country_codes = ["+1", "+44", "+33", "+49", "+61", "+81", "+86", "+91", "+7", "+39"]
addresses = [
    "123 Main St", "456 Oak Ave", "789 Pine Rd", "101 Maple Dr", "202 Elm St",
    "303 Cedar Ln", "404 Birch Blvd", "505 Spruce Ct", "606 Walnut Pl", "707 Chestnut Way"
]
universities = [
    "Harvard University", "Stanford University", "MIT", "Oxford University", "Cambridge University",
    "Yale University", "Princeton University", "Columbia University", "Caltech", "UCLA"
]

def random_email(first, last):
    domains = ["gmail.com", "yahoo.com", "outlook.com", "edu.com", "mail.com"]
    return f"{first.lower()}.{last.lower()}@{random.choice(domains)}"

def random_phone():
    return str(random.randint(1000000000, 9999999999))

def random_barcode():
    return str(random.randint(100000, 999999))