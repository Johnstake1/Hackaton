from Modules.db_connection import DatabaseConnection
from Utils.config import get_database_config
from Modules.User_regisration import UserRegistration
from Data.create_tables import create_tables
from Modules.portfolio import Portfolio
from Modules.API import get_sp500_value


def main():
    # Step 1: Get database configuration
    db_config = get_database_config()

    # Step 2: Connect to the database
    db = DatabaseConnection(**db_config)
    db.connect()

    # Step 3: Ensure the tables exist
    create_tables(db)

    # Step 4: Create an instance of UserRegistration
    User_registration = UserRegistration(db_config)

    # Step 5: Register a customer or fetch existing customer
    customer_data = User_registration.register_customer(db)

    if customer_data:
        print("Customer processed successfully:")
        print(customer_data)
        
        # Step 6: Prompt to view portfolio
        view_portfolio = input("Would you like to view your portfolio? (yes/no): ").strip().lower()

        if view_portfolio == "yes":
            customer_id = customer_data['customer_id']  # Fetch the customer_id from the registered data
            portfolio = Portfolio(customer_id, db_config)

            # Display the current portfolio
            portfolio.display_portfolio()  # Ensure display_portfolio method is implemented in Portfolio

        else:
            print("You chose not to view the portfolio.")

    # Step 7: Close the database connection
    db.close()

if __name__ == "__main__":
    main()