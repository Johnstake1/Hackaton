def create_tables(db):
    create_customer_table_query = """
    CREATE TABLE IF NOT EXISTS Customer (
        customer_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        date_of_birth DATE NOT NULL,
        address VARCHAR(255),
        country VARCHAR(50),
        phone_number VARCHAR(50),
        registration_date TIMESTAMP NOT NULL
    )
    """
    db.execute_query(create_customer_table_query)

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
    db.execute_query(create_transaction_table_query)
