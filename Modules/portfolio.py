from datetime import datetime, timedelta
from collections import defaultdict
import psycopg2

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
        # Ensure that savings have not already been invested this month
        if self.invested_this_month:
            print("Savings have already been invested this month. No further investments can be made.")
            return

        # Get the current date and determine if today is the last day of the month
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        next_month = current_month + 1 if current_month < 12 else 1
        next_month_year = current_year if current_month < 12 else current_year + 1
        
        # Find the first day of the next month
        first_day_next_month = datetime(next_month_year, next_month, 1)
        
        # Last day of the current month is one day before the first day of the next month
        last_day_of_current_month = first_day_next_month - timedelta(days=1)
        
        # Check if today is the last day of the month
        if now.date() != last_day_of_current_month.date():
            print(f"Today is not the last day of the month. Investment will be made on {last_day_of_current_month.date()}.")
            return

        # If there are savings, "invest" in the S&P 500 ETF (SPY)
        if self.savings > 0:
            stock = self.select_stock()  # Always invest in the S&P 500 ETF
            stock_purchase_amount = self.savings
            stock_value = self.get_stock_value(stock)
            portfolio_value = stock_purchase_amount * stock_value
            percentage_change = self.calculate_percentage_change()
            cumulative_savings = self.calculate_cumulative_savings()

            # Insert the investment into the portfolio table
            self.insert_into_portfolio(stock, stock_purchase_amount, stock_value, portfolio_value, percentage_change, cumulative_savings)

            # Mark savings as invested
            self.invested_this_month = True
            self.savings = 0.0  # Reset savings after investment
            print(f"Invested {stock_purchase_amount:.2f} into {stock}.")
        else:
            print("No savings to invest this month.")

    def select_stock(self):
        """
        Select the S&P 500 stock (SPY) for investment.
        """
        return "SPY"  # Always invest in the S&P 500 ETF (SPY)

    def get_stock_value(self, ticker):
        """
        Fetch the current stock value from an API like Google Finance or any stock price API.
        For simplicity, we'll return a static value for SPY.
        """
        if ticker == "SPY":
            # Example: static value for SPY, in a real scenario, you can fetch this from an API
            return 450.00  # Placeholder value, replace with actual API call

    def calculate_percentage_change(self):
        """
        Calculate the percentage change in portfolio value month-over-month.
        """
        # Placeholder: assuming no previous value for simplicity
        # In practice, you would calculate based on previous month's value
        previous_value = 0  # Assuming previous value is 0 for first time calculation
        percentage_change = ((self.savings - previous_value) / previous_value) * 100 if previous_value else 0
        return percentage_change

    def calculate_cumulative_savings(self):
        """
        Calculate cumulative savings for the month (sum of rounded transaction differences).
        """
        return sum(txn["unrounded_difference"] for txn in self.transactions)

    def insert_into_portfolio(self, ticker, stock_purchase_amount, stock_value, portfolio_value, percentage_change, cumulative_savings):
        """
        Insert the portfolio record into the database.
        """
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

    def get_portfolio_data(self):
        """
        Fetch the portfolio data from the database for a specific customer.
        """
        query = """
        SELECT portfolio_id, ticker, stock_purchase_amount, stock_value, portfolio_value, 
               percentage_change, cumulative_savings 
        FROM Portfolio
        WHERE customer_id = %s
        ORDER BY portfolio_id DESC
        """
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute(query, (self.customer_id,))
        portfolio_data = cursor.fetchall()
        cursor.close()
        connection.close()
        return portfolio_data

    def display_portfolio(self):
        """
        Display the portfolio data to the user.
        """
        portfolio_data = self.get_portfolio_data()

        if portfolio_data:
            print(f"Portfolio for Customer ID: {self.customer_id}")
            for record in portfolio_data:
                portfolio_id, ticker, stock_purchase_amount, stock_value, portfolio_value, percentage_change, cumulative_savings = record
                print(f"\nPortfolio ID: {portfolio_id}")
                print(f"Ticker: {ticker}")
                print(f"Stock Purchase Amount: {stock_purchase_amount:.2f}")
                print(f"Stock Value: {stock_value:.2f}")
                print(f"Portfolio Value: {portfolio_value:.2f}")
                print(f"Percentage Change: {percentage_change:.2f}%")
                print(f"Cumulative Savings: {cumulative_savings:.2f}")
        else:
            print("No portfolio data found for this customer.")
    