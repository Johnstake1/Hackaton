from Modules.db_connection import DatabaseConnection
from Data.create_tables import create_tables
from Utils.config import get_database_config
from Modules.User_regisration import Customer
from Modules.Transactions import Transaction

def main():
    db_config = get_database_config()
    db = DatabaseConnection(**db_config)
    db.connect()
    create_tables(db)
    customers = [UserRegistration.input_customer_data()]
    Transaction.fake_transactions(db, customers) 
    db.close()

if __name__ == "__main__":
    main()
