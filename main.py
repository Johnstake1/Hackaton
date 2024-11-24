from Modules.db_connection import DatabaseConnection
from Utils.config import get_database_config
from Modules.User_regisration import UserRegistration
from Data.create_tables import create_tables

def main():
    # Step 1: Get database configuration
    db_config = get_database_config()

    # Step 2: Connect to the database
    db = DatabaseConnection(**db_config)
    db.connect()

    # Step 3: Ensure the tables exist
    create_tables(db)

    # Step 4: Create an instance of UserRegistration
    user_registration = UserRegistration(db_config)

    # Step 5: Register a customer or fetch existing customer
    customer_data = user_registration.register_customer(db)

    if customer_data:
        print("Customer processed successfully:")
        print(customer_data)

    # Step 6: Close the database connection
    db.close()

if __name__ == "__main__":
    main()