from datetime import datetime
from collections import defaultdict

class Portfolio:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.savings = 0.0  # Total savings from rounded differences
        self.transactions = []  # List to store transactions related to the customer
        self.investments = defaultdict(float)  # Tracks stocks and investment amounts

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
        Simulates investing savings into a single stock at the end of the month.
        """
        # Get the current month and year
        now = datetime.now()
        current_month = now.month
        current_year = now.year

        # Filter transactions from the current month
        monthly_transactions = [
            txn for txn in self.transactions
            if txn["transaction_date"].month == current_month and txn["transaction_date"].year == current_year
        ]

        # If there are savings, "invest" in a stock
        if self.savings > 0:
            # For simplicity, select a random stock (could connect to an API for real stock data)
            stock = self.select_stock()
            self.investments[stock] += self.savings
            print(f"Invested {self.savings:.2f} into {stock}.")
            self.savings = 0.0  # Reset savings after investment
        else:
            print("No savings to invest this month.")

    def select_stock(self):
        """
        Select a stock to invest in (can be random or logic-based).
        """
        stock_list = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"]  # Example stock options
        selected_stock = random.choice(stock_list)  # Randomly select a stock
        return selected_stock