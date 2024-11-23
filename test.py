import json
from datetime import datetime
from faker import Faker
import random
import psycopg2

# Customer class to represent each customer
class Customer:
    def __init__(self, customer_id, first_name, last_name, email, date_of_birth, address, country, phone_number, registration_date=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.address = address
        self.country = country
        self.phone_number = phone_number
        self.registration_date = registration_date if registration_date else datetime.now()

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_of_birth": self.date_of_birth.strftime("%Y-%m-%d"),
            "address": self.address,
            "country": self.country,
            "phone_number": self.phone_number,
            "registration_date": self.registration_date.strftime("%Y-%m-%d %H:%M:%S")
        }

# Transaction class to represent each transaction
class Transaction:
    def __init__(self, transaction_id, customer_id, transaction_date, transaction_amount, rounded_amount, category, merchant_name):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.transaction_date = transaction_date
        self.transaction_amount = transaction_amount
        self.rounded_amount = rounded_amount
        self.unrounded_difference = rounded_amount - transaction_amount
        self.category = category
        self.merchant_name = merchant_name

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "transaction_date": self.transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_amount": self.transaction_amount,
            "rounded_amount": self.rounded_amount,
            "unrounded_difference": self.unrounded_difference,
            "category": self.category,
            "merchant_name": self.merchant_name
        }

# Function to populate the database with fake data using Faker
def populate_fake_data(num_customers=10, num_transactions=50):
    fake = Faker()
    customers = []
    transactions = []

    # PostgreSQL database connection
    try:
        connection = psycopg2.connect(
            dbname="Centsible Invest",
            user="postgres",
            password="6760",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # Create Customer table
        create_customer_table_query = """
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            date_of_birth DATE NOT NULL,
            address VARCHAR(255),
            country VARCHAR(50),
            phone_number VARCHAR(100),
            registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_customer_table_query)

        # Create Transaction table
        create_transaction_table_query = """
        CREATE TABLE IF NOT EXISTS Transaction (
            transaction_id SERIAL PRIMARY KEY,
            customer_id INT,
            transaction_date TIMESTAMP NOT NULL,
            transaction_amount DECIMAL(10, 2) NOT NULL,
            rounded_amount DECIMAL(10, 2) NOT NULL,
            unrounded_difference DECIMAL(10, 2) NOT NULL,
            category VARCHAR(50),
            merchant_name VARCHAR(100),
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
        )
        """
        cursor.execute(create_transaction_table_query)

        # Generate fake customers and insert them into the database
        for i in range(1, num_customers + 1):
            customer = Customer(
                customer_id=i,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
                address=fake.address(),
                country=fake.country(),
                phone_number=fake.phone_number()
            )
            customers.append(customer)

            insert_customer_query = """
            INSERT INTO Customer (customer_id, first_name, last_name, email, date_of_birth, address, country, phone_number, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_customer_query, (
                customer.customer_id, customer.first_name, customer.last_name, customer.email,
                customer.date_of_birth, customer.address, customer.country, customer.phone_number,
                customer.registration_date
            ))

        # Generate fake transactions and insert them into the database
        for i in range(1, num_transactions + 1):
            customer_id = random.randint(1, num_customers)
            transaction_amount = round(random.uniform(1.0, 100.0), 2)
            rounded_amount = round(transaction_amount)
            transaction = Transaction(
                transaction_id=i,
                customer_id=customer_id,
                transaction_date=fake.date_time_this_year(),
                transaction_amount=transaction_amount,
                rounded_amount=rounded_amount,
                category=fake.word(ext_word_list=["Groceries", "Electronics", "Clothing", "Utilities", "Dining"]),
                merchant_name=fake.company()
            )
            transactions.append(transaction)

            insert_transaction_query = """
            INSERT INTO Transaction (transaction_id, customer_id, transaction_date, transaction_amount, rounded_amount, unrounded_difference, category, merchant_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_transaction_query, (
                transaction.transaction_id, transaction.customer_id, transaction.transaction_date,
                transaction.transaction_amount, transaction.rounded_amount, transaction.unrounded_difference,
                transaction.category, transaction.merchant_name
            ))

        # Commit changes to the database
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# Example of usage
def main():
    populate_fake_data()

if __name__ == "__main__":
    main()
