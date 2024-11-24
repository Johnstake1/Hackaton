import psycopg2

class DatabaseConnection:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

    def close(self):
        """Close the connection to the PostgreSQL database."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

    def execute_query(self, query, values=None):
        """Execute an SQL query with optional values."""
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error executing query:", error)
            self.connection.rollback()

    def fetch_one(self, query, values=None):
        """Execute a query and fetch a single result."""
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data:", error)
            return None

    def fetch_all(self, query, values=None):
        """Execute a query and fetch all results."""
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error fetching data:", error)
            return None

    def check_existing_transactions(self, customer_id):
        """Check if transactions exist for the given customer."""
        query = "SELECT COUNT(*) FROM Transaction WHERE customer_id = %s"
        try:
            self.cursor.execute(query, (customer_id,))
            return self.cursor.fetchone()[0] > 0
        except (Exception, psycopg2.Error) as error:
            print(f"Error checking transactions for customer {customer_id}:", error)
            return False