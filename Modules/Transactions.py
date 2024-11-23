from faker import Faker
from customer import Customer
import random
from db_connection import DatabaseConnection

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


def populate_fake_data(db, num_transactions=10000):
    fake = Faker()

    # Generate fake transactions and insert them into the database
    for i in range(1, num_transactions + 1):
        customer_id = customer_id
        registration_date = customers[customer_id - 1].registration_date
        transaction_date = fake.date_time_between(start_date=registration_date, end_date="now")
        transaction_amount = round(random.uniform(1.0, 1000.0), 2)
        rounded_amount = int(transaction_amount) + (1 if transaction_amount != int(transaction_amount) else 0)
        transaction = Transaction(
            transaction_id=i,
            customer_id=customer_id,
            transaction_date=transaction_date,
            transaction_amount=transaction_amount,
            rounded_amount=rounded_amount,
            category=fake.word(ext_word_list=["Groceries", "Electronics", "Clothing", "Utilities", "Dining"]),
            merchant_name=fake.company()
        )

        insert_transaction_query = """
        INSERT INTO Transaction (transaction_id, customer_id, transaction_date, transaction_amount, rounded_amount, unrounded_difference, category, merchant_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        db.execute_query(insert_transaction_query, (
            transaction.transaction_id, transaction.customer_id, transaction.transaction_date,
            transaction.transaction_amount, transaction.rounded_amount, transaction.unrounded_difference,
            transaction.category, transaction.merchant_name
        ))