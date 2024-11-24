import psycopg2
from datetime import datetime
#test
class UserRegistration:
    def __init__(self, db_config): #Connecting to the database using the db_config so that registration_customer can open and add the new information to the DB.
        self.db_config = db_config

    def connect_to_db(self):
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)
            return None

    def register_customer(self):
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
            print(f"Registration successful! Your Customer ID is: {customer_id}")
            return customer_id
        except (Exception, psycopg2.Error) as error:
            print("Error during registration:", error)
            connection.rollback()
        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    # Database connection configuration
    db_config = {
        "dbname": "Centsible Invest",
        "user": "postgres",
        "password": "1234",
        "host": "localhost",
        "port": "5433"
    }

    registration = UserRegistration(db_config)

    print("\nWelcome to Centsible Invest Customer Registration!")
    registration.register_customer()