from Modules.db_connection import DatabaseConnection
from Utils.config import get_database_config
from Modules.User_regisration import UserRegistration
from Data.create_tables import create_tables
from Modules.portfolio import Portfolio
from Modules.Transaction import Transaction

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
    
    customer_data = user_registration.register_customer(db)

    if customer_data:
        print("Customer processed successfully:")
        print(customer_data)

        while True:
            print("\nPlease select an option:")
            print("1. Register a new user")
            print("2. View monthly savings")
            print("3. Exit")
            
            choice = input("Enter your choice (1/2/3): ").strip()
            
            if choice == '1':
                customer_data = user_registration.register_customer(db)
                if customer_data:
                    print("Customer processed successfully:")
                    print(customer_data)
            elif choice == '2':
                customer_id = customer_data['customer_id']
                transactions = Transaction(customer_id)
                monthly_savings = transactions.calculate_monthly_savings()
                print("\nMonthly Savings (Total for Each Month):")
                for entry in monthly_savings:
                    print(f"{entry['month']}: {entry['savings']:.2f}")
            elif choice == '3':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.") 
    else:
        print('You are not a customer')

    # Step 6: Close the database connection
    db.close()

if __name__ == "__main__":
    main()
