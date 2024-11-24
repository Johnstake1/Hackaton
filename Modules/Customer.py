import datetime
from Modules.db_connection import DatabaseConnection
from faker import Faker
import random

class UserRegistration:
    def __init__(self, customer_id, first_name, last_name, email, date_of_birth, address, country, phone_number, registration_date=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.address = address
        self.country = country
        self.phone_number = phone_number
        self.registration_date = registration_date

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "address": self.address,
            "country": self.country,
            "phone_number": self.phone_number,
            "registration_date": self.registration_date
        }

    @staticmethod
    def input_customer_data():
        customer_id = None #Im having an issue generating the customer_id
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        date_of_birth = datetime.datetime.strptime(input("Enter Date of Birth (YYYY-MM-DD): "), "%Y-%m-%d")
        address = input("Enter Address: ")
        country = input("Enter Country: ")
        phone_number = input("Enter Phone Number: ")
        registration_date = Faker().date_time_between(start_date='-5y', end_date='now')
        return UserRegistration(customer_id, first_name, last_name, email, date_of_birth, address, country, phone_number, registration_date)
    
    def insert_customer_data(db):
        customer = UserRegistration.input_customer_data()
        insert_customer_query = """
        INSERT INTO Customer (first_name, last_name, email, date_of_birth, address, country, phone_number, registration_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
        db.execute_query(insert_customer_query, (
        customer.customer_id, customer.first_name, customer.last_name, customer.email,
        customer.date_of_birth, customer.address, customer.country, customer.phone_number,
        customer.registration_date))

