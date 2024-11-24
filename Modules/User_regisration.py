import psycopg2
from datetime import datetime


class UserRegistration:
    def __init__(self, db_config):
        """Connect to the database using the db_config so the registration_customer method can interact with the DB."""
        self.db_config = db_config

    def connect_to_db(self):
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)
            return None

    def check_if_registered(self, email):
        """Check if the user with the given email is already registered in the database."""
        connection = self.connect_to_db()
        if not connection:
            return None

        cursor = connection.cursor()
        check_email_query = "SELECT customer_id, first_name, last_name FROM Customer WHERE email = %s"
        try:
            cursor.execute(check_email_query, (email,))
            result = cursor.fetchone()
            if result:
                # Return customer data if email exists
                return {"customer_id": result[0], "first_name": result[1], "last_name": result[2]}
            else:
                # Return None if the email is not found
                return None
        except (Exception, psycopg2.Error) as error:
            print("Error during email check:", error)
            return None
        finally:
            cursor.close()
            connection.close()

    def register_customer(self):
        """Register a new customer by collecting details and adding them to the database."""
        connection = self.connect_to_db()
        if not connection:
            return None

        cursor = connection.cursor()
        print("Please provide the following details to register as a customer:")

        # Collect user input
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("Email: ").strip()
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
            cursor.execute(insert_customer_query, (
                first_name, last_name, email, date_of_birth, address, country, phone_number, registration_date
            ))
            customer_id = cursor.fetchone()[0]
            connection.commit()
            print(f"Customer registered successfully! Customer ID: {customer_id}")
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
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()


class Customer:
    def __init__(self, db_config, user_data):
        """Initialize the Customer object with user data."""
        self.db_config = db_config
        self.customer_id = user_data["customer_id"]
        self.first_name = user_data["first_name"]
        self.last_name = user_data["last_name"]
        self.email = user_data["email"]
        self.date_of_birth = user_data["date_of_birth"]
        self.address = user_data["address"]
        self.country = user_data["country"]
        self.phone_number = user_data["phone_number"]
        self.registration_date = user_data["registration_date"]

    def display_customer_details(self):
        """Print the customer details."""
        print("\nCustomer Details:")
        print(f"Customer ID: {self.customer_id}")
        print(f"Name: {self.first_name} {self.last_name}")
        print(f"Email: {self.email}")
        print(f"Date of Birth: {self.date_of_birth}")
        print(f"Address: {self.address}")
        print(f"Country: {self.country}")
        print(f"Phone Number: {self.phone_number}")
        print(f"Registration Date: {self.registration_date}")


if __name__ == "__main__":
    # Database connection configuration
    db_config = {
        "dbname": "Centsible Invest",
        "user": "postgres",
        "password": "6760",
        "host": "localhost",
        "port": "5432"
    }

    print("\nWelcome to Centsible Invest Customer Registration!")
    registration = UserRegistration(db_config)

    # Ask for email to check if the user is already registered
    email = input("Please enter your email: ").strip()
    user_data = registration.check_if_registered(email)

    if user_data:
        print(f"\nWelcome back, {user_data['first_name']} {user_data['last_name']}!")
        customer = Customer(db_config, user_data)
        customer.display_customer_details()
    else:
        print("You are not registered yet. Let's register you.")
        user_data = registration.register_customer()

        if user_data:
            # Create a Customer object after registration
            customer = Customer(db_config, user_data)
            customer.display_customer_details()


