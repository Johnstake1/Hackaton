from Modules.db_connection import DatabaseConnection
from Data.create_tables import create_tables
from Utils.config import get_database_config

def main():
    db_config = get_database_config()
    db = DatabaseConnection(**db_config)
    db.connect()
    create_tables(db)
    #need to add remaining processes
    db.close()

if __name__ == "__main__":
    main()
