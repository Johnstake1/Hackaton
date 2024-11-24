import psycopg2
from datetime import datetime
from Modules.Transactions import Transaction


class UserRegistration:
    def __init__(self, db_config):
        """Initialize with database configuration for connecting to the database."""
        self.db_config = db_config

    def connect_to_db(self):
        """Establish a database connection."""
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)
            return None

    def check_if_registered(self, email):
        """
        Check if the user with the given email is already registered.
        Returns the customer's details if registered, otherwise None.
        """
        connection = self.connect_to_db()
        if not connection:
            return None

        cursor = connection.cursor()
        check_email_query = "SELECT customer_id, first_name, last_name, registration_date FROM Customer WHERE email = %s"
        try:
            cursor.execute(check_email_query, (email,))
            result = cursor.fetchone()
            if result:
                return {
                    "customer_id": result[0],
                    "first_name": result[1],
                    "last_name": result[2],
                    "registration_date": result[3],
                }
            else:
                return None
        except (Exception, psycopg2.Error) as error:
            print("Error during email check:", error)
            return None
        finally:
            cursor.close()
            connection.close()

    def register_customer(self, db):
        """
        Register a new customer or fetch existing customer details.
        Ensures fake transactions are generated for new customers.
        """
        print("Please provide the following details to register as a customer:")

        # Collect user input
        email = input("Email: ").strip()

        # Check if the user is already registered
        existing_customer = self.check_if_registered(email)
        if existing_customer:
            print(f"Customer already registered: {existing_customer['first_name']} {existing_customer['last_name']}.")
            Transaction.generate_fake_transactions(db, existing_customer["customer_id"], existing_customer["registration_date"])
            return existing_customer

        # If not registered, collect full details for registration
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        date_of_birth = input("Date of Birth (YYYY-MM-DD): ").strip()
        address = input("Address: ").strip()
        country = input("Country: ").strip()
        phone_number = input("Phone Number: ").strip()
        registration_date = datetime.now()

        # SQL query to insert the new customer
        insert_customer_query = """
        INSERT INTO Customer (first_name, last_name, email, date_of_birth, address, country, phone_number, registration_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING customer_id
        """
        try:
            db.cursor.execute(insert_customer_query, (
                first_name, last_name, email, date_of_birth, address, country, phone_number, registration_date
            ))
            customer_id = db.cursor.fetchone()[0]
            db.connection.commit()
            print(f"Customer registered successfully! Customer ID: {customer_id}")

            # Generate fake transactions for the new customer
            Transaction.generate_fake_transactions(db, customer_id, registration_date)

            return {
                "customer_id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "date_of_birth": date_of_birth,
                "address": address,
                "country": country,
                "phone_number": phone_number,
                "registration_date": registration_date,
            }
        except (Exception, psycopg2.Error) as error:
            print("Error during registration:", error)
            db.connection.rollback()
            return None