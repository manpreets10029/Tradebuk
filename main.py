import sqlite3
from datetime import datetime, timedelta

class TradeBuk:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('tradebuk.db')
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            exit(1)

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY,
                date TEXT,
                stock TEXT,
                action TEXT,
                quantity INTEGER,
                price REAL,
                profit_loss REAL,
                notes TEXT
            )
        ''')
        self.conn.commit()

    def add_trade(self):
        try:
            date = input("Enter date (YYYY-MM-DD): ")
            datetime.strptime(date, "%Y-%m-%d")  # Validate date format
            stock = input("Enter stock symbol: ")
            action = input("Buy or Sell: ").lower()
            if action not in ['buy', 'sell']:
                raise ValueError("Action must be 'buy' or 'sell'")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price per share (in ₹): "))
            profit_loss = input("Enter profit/loss (in ₹, optional): ")
            notes = input("Add notes (optional): ")

            profit_loss = float(profit_loss) if profit_loss else None

            self.cursor.execute('''
                INSERT INTO trades (date, stock, action, quantity, price, profit_loss, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (date, stock, action, quantity, price, profit_loss, notes))
            self.conn.commit()
            print("Trade recorded successfully!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def view_trades(self):
        try:
            self.cursor.execute("SELECT * FROM trades")
            trades = self.cursor.fetchall()
            if not trades:
                print("No trades found.")
                return
            for trade in trades:
                print(f"Date: {trade[1]}, Stock: {trade[2]}, Action: {trade[3]}, "
                      f"Quantity: {trade[4]}, Price: ₹{trade[5]:.2f}, "
                      f"Profit/Loss: ₹{trade[6] or 0:.2f}, Notes: {trade[7]}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def calculate_profit_loss(self, period):
        try:
            end_date = datetime.now().date()
            if period == 'daily':
                start_date = end_date
            elif period == 'weekly':
                start_date = end_date - timedelta(days=7)
            elif period == 'monthly':
                start_date = end_date.replace(day=1)
            else:
                raise ValueError("Invalid period. Choose 'daily', 'weekly', or 'monthly'.")

            self.cursor.execute('''
                SELECT SUM(profit_loss) FROM trades 
                WHERE date BETWEEN ? AND ?
            ''', (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
            result = self.cursor.fetchone()[0]
            print(f"Total {period} profit/loss: ₹{result or 0:.2f}")
        except ValueError as e:
            print(f"Error: {e}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def run(self):
        while True:
            print("\nTradeBuk Menu:")
            print("1. Add Trade")
            print("2. View Trades")
            print("3. Calculate Profit/Loss")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                self.add_trade()
            elif choice == '2':
                self.view_trades()
            elif choice == '3':
                period = input("Enter period (daily/weekly/monthly): ").lower()
                self.calculate_profit_loss(period)
            elif choice == '4':
                print("Thank you for using TradeBuk!")
                break
            else:
                print("Invalid choice. Please try again.")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    app = TradeBuk()
    app.run()
    