import requests
from datetime import datetime, timedelta
from collections import defaultdict
import psycopg2
from API import get_sp500_value 

class Portfolio:
    def __init__(self, customer_id, db_config):
        self.customer_id = customer_id
        self.savings = 0.0  # Total savings from rounded differences
        self.transactions = []  # List to store transactions related to the customer
        self.investments = defaultdict(float)  # Tracks stocks and investment amounts
        self.db_config = db_config  # Database configuration
        self.invested_this_month = False  # Track if savings have already been invested this month

    def add_transaction(self, transaction_id, transaction_date, unrounded_difference):
        """
        Add a transaction and update savings based on the unrounded difference.
        """
        self.transactions.append({
            "transaction_id": transaction_id,
            "transaction_date": transaction_date,
            "unrounded_difference": unrounded_difference,
        })
        self.savings += unrounded_difference  # Update savings with the rounded difference
        print(f"Transaction {transaction_id} added. Savings updated to {self.savings:.2f}.")

    def invest_savings(self):
        """
        Simulates investing savings into the S&P 500 ETF (SPY) at the end of the month (last day).
        Inserts the investment record into the Portfolio table in the database.
        """
        if self.invested_this_month:
            print("Savings have already been invested this month. No further investments can be made.")
            return

        now = datetime.now()
        current_month = now.month
        current_year = now.year
        next_month = current_month + 1 if current_month < 12 else 1
        next_month_year = current_year if current_month < 12 else current_year + 1
        
        first_day_next_month = datetime(next_month_year, next_month, 1)
        last_day_of_current_month = first_day_next_month - timedelta(days=1)
        
        if now.date() != last_day_of_current_month.date():
            print(f"Today is not the last day of the month. Investment will be made on {last_day_of_current_month.date()}.")
            return

        if self.savings > 0:
            stock = self.select_stock()  # Always invest in the S&P 500 ETF
            stock_purchase_amount = self.savings
            stock_value = self.get_stock_value(stock)
            portfolio_value = stock_purchase_amount * stock_value
            percentage_change = self.calculate_percentage_change()
            cumulative_savings = self.calculate_cumulative_savings()

            self.insert_into_portfolio(stock, stock_purchase_amount, stock_value, portfolio_value, percentage_change, cumulative_savings)
            self.invested_this_month = True
            self.savings = 0.0  # Reset savings after investment
            print(f"Invested {stock_purchase_amount:.2f} into {stock}.")
        else:
            print("No savings to invest this month.")

    def select_stock(self):
        return ".INX:INDEXSP"

    def get_stock_value(self, ticker):
        stock_value = get_sp500_value()
        print(f"Stock Value Retrieved: {stock_value}")  # Debugging line
        if stock_value is not None:
            return stock_value
        else:
            print("Error: Could not fetch stock value.")
            return 0.0

    def calculate_percentage_change(self):
        previous_value = 0  # Placeholder: assuming previous value is 0 for simplicity
        percentage_change = ((self.savings - previous_value) / previous_value) * 100 if previous_value else 0
        return percentage_change

    def calculate_cumulative_savings(self):
        return sum(txn["unrounded_difference"] for txn in self.transactions)

    def insert_into_portfolio(self, ticker, stock_purchase_amount, stock_value, portfolio_value, percentage_change, cumulative_savings):
        try:
            connection = psycopg2.connect(**self.db_config)
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO Portfolio (
                customer_id, ticker, stock_purchase_amount, stock_value, portfolio_value,
                percentage_change, cumulative_savings
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                self.customer_id, ticker, stock_purchase_amount, stock_value, portfolio_value,
                percentage_change, cumulative_savings
            )

            cursor.execute(insert_query, data)
            connection.commit()
            print(f"Portfolio updated for customer {self.customer_id}. Investment details added.")
        except Exception as e:
            print(f"Error inserting into Portfolio table: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def display_portfolio(self):
        try:
            connection = psycopg2.connect(**self.db_config)
            cursor = connection.cursor()

            select_query = """
            SELECT ticker, stock_purchase_amount, stock_value, portfolio_value, percentage_change, cumulative_savings
            FROM Portfolio
            WHERE customer_id = %s
            """
            cursor.execute(select_query, (self.customer_id,))
            records = cursor.fetchall()

            if records:
                print("Portfolio:")
                for record in records:
                    print(f"Stock: {record[0]}, Purchased Amount: {record[1]:.2f}, Stock Value: {record[2]:.2f}, "
                          f"Portfolio Value: {record[3]:.2f}, Percentage Change: {record[4]}%, "
                          f"Cumulative Savings: {record[5]:.2f}")
            else:
                print("No portfolio data found.")
        except Exception as e:
            print(f"Error displaying portfolio: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()