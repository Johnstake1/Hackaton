from datetime import datetime
from faker import Faker
import random
import psycopg2
import pandas as pd


class Transaction:
    def __init__(self, transaction_id, customer_id, transaction_date, transaction_amount, rounded_amount, category, merchant_name):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.transaction_date = transaction_date
        self.transaction_amount = transaction_amount
        self.rounded_amount = rounded_amount
        self.unrounded_difference = rounded_amount - transaction_amount if rounded_amount > transaction_amount else transaction_amount - rounded_amount
        self.category = category
        self.merchant_name = merchant_name

    def to_dict(self):
        """Convert transaction object to a dictionary for easier handling."""
        return {
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "transaction_date": self.transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_amount": self.transaction_amount,
            "rounded_amount": self.rounded_amount,
            "unrounded_difference": self.unrounded_difference,
            "category": self.category,
            "merchant_name": self.merchant_name
        }

    @staticmethod
    def generate_fake_transactions(db, customer_id, registration_date, num_transactions=10):
        """
        Generate fake transactions for a given customer if they don't already exist.
        Each transaction is linked to the customer's registration date and spans until the current date.
        """
        if db.check_existing_transactions(customer_id):
            print(f"Transactions already exist for customer {customer_id}. Skipping generation.")
            return

        fake = Faker()
        print(f"Generating {num_transactions} fake transactions for customer {customer_id}...")

        for _ in range(num_transactions):
            transaction_date = fake.date_time_between(start_date=registration_date, end_date="now")
            transaction_amount = round(random.uniform(1.0, 10000.0), 2)
            rounded_amount = int(transaction_amount) + (1 if transaction_amount != int(transaction_amount) else 0)
            category = fake.word(ext_word_list=["Groceries", "Electronics", "Clothing", "Utilities", "Dining"])
            merchant_name = fake.company()

            # SQL query to insert transaction
            insert_transaction_query = """
            INSERT INTO Transaction (customer_id, transaction_date, transaction_amount, rounded_amount, unrounded_difference, category, merchant_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(insert_transaction_query, (
                customer_id,
                transaction_date,
                transaction_amount,
                rounded_amount,
                abs(rounded_amount - transaction_amount),
                category,
                merchant_name
            ))

        print(f"Fake transactions generated successfully for customer {customer_id}.")

    def calculate_monthly_savings(self):

        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()
        
        query = """
        SELECT transaction_date, unrounded_difference
        FROM transaction
        WHERE customer_id = %s
        ORDER BY transaction_date
        """
        cursor.execute(query, (self.customer_id,))
        transactions = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        data = []
        for transaction_date, unrounded_difference in transactions:
            transaction_date = pd.to_datetime(transaction_date)
            data.append([transaction_date, unrounded_difference])

        df = pd.DataFrame(data, columns=['transaction_date', 'unrounded_difference'])
        
        # Set the transaction date as the index to group by month
        df.set_index('transaction_date', inplace=True)
        
        # Group by month and calculate the total savings for each month
        monthly_savings = df['unrounded_difference'].resample('M').sum()
        
        # Print or return the results
        print("Monthly Savings (Total for Each Month):")
        for date, savings in monthly_savings.items():
            print(f"{date.strftime('%Y-%m')}: {savings:.2f}")