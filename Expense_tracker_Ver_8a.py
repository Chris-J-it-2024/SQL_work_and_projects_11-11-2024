import json
import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import mysql.connector
from mysql.connector import Error

class ExpenseTracker:
    def __init__(self):
        """Initialize the expense tracker with database connection and file handling setup"""
        self.expenses_file = 'expenses.json'
        self.summary_file = 'expense_summary.json'
        self.valid_categories = {'food', 'transport', 'entertainment', 'utilities', 'other'}
        self.db_connection = self.connect_to_database()
        self.load_expenses()

    def connect_to_database(self):
        """Establish connection to MySQL database"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='expense_tracker',
                user='your_username',
                password='your_password'
            )
            if connection.is_connected():
                print("Successfully connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None

    def load_expenses(self):
        """Load existing expenses from database"""
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
                self.expense_list = cursor.fetchall()
                cursor.close()
            except Error as e:
                print(f"Error loading expenses: {e}")
                self.expense_list = []
        else:
            self.expense_list = []

    def save_expense(self, expense_data):
        """Save expense to MySQL database"""
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                query = """INSERT INTO expenses 
                          (amount, category, description, date) 
                          VALUES (%s, %s, %s, %s)"""
                values = (
                    expense_data['amount'],
                    expense_data['category'],
                    expense_data['description'],
                    expense_data['date']
                )
                cursor.execute(query, values)
                self.db_connection.commit()
                cursor.close()
                return True
            except Error as e:
                print(f"Error saving expense: {e}")
                return False
        return False

    def validate_expense(self, expense_data):
        """Validate expense data before saving"""
        try:
            # Check if amount is positive
            if not isinstance(expense_data['amount'], (int, float)) or expense_data['amount'] <= 0:
                return False, "Amount must be positive"
            
            # Check if category is valid
            if expense_data['category'] not in self.valid_categories:
                return False, "Invalid category"
            
            # Check if description exists
            if not expense_data['description'].strip():
                return False, "Description cannot be empty"
            
            return True, ""
        except KeyError as error:
            return False, f"Missing required field: {str(error)}"

    def add_expense(self, expense_data):
        """Add a new expense after validation"""
        is_valid, error_message = self.validate_expense(expense_data)
        if not is_valid:
            print(f"Error: {error_message}")
            return False
        
        if self.save_expense(expense_data):
            self.load_expenses()  # Reload expenses from database
            self.update_summary()
            return True
        return False

    def calculate_summary(self):
        """Calculate expense summary including totals by category"""
        if not self.db_connection:
            return None

        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # Calculate total amount
            cursor.execute("SELECT SUM(amount) as total FROM expenses")
            total_result = cursor.fetchone()
            total_amount = total_result['total'] if total_result['total'] else 0

            # Calculate category totals
            cursor.execute("""
                SELECT category, SUM(amount) as total 
                FROM expenses 
                GROUP BY category
            """)
            category_totals = {row['category']: row['total'] for row in cursor.fetchall()}
            
            # Fill in missing categories with 0
            for category in self.valid_categories:
                if category not in category_totals:
                    category_totals[category] = 0

            cursor.close()
            
            return {
                'total_amount': total_amount,
                'category_totals': category_totals,
                'expenses': self.expense_list
            }
        except Error as e:
            print(f"Error calculating summary: {e}")
            return None

    def update_summary(self):
        """Update the summary file with current data"""
        summary_data = self.calculate_summary()
        if summary_data:
            with open(self.summary_file, 'w') as file:
                json.dump(summary_data, file, indent=2)

class NewExpenseHandler(FileSystemEventHandler):
    """Handle new expense file events"""
    def __init__(self, expense_tracker):
        self.expense_tracker = expense_tracker

    def on_created(self, event):
        """Process new expense files when they're created"""
        if event.src_path.endswith('new_expense.json'):
            try:
                # Wait briefly to ensure file is completely written
                time.sleep(0.1)
                with open(event.src_path, 'r') as file:
                    expense_data = json.load(file)
                
                self.expense_tracker.add_expense(expense_data)
                os.remove(event.src_path)
            except Exception as error:
                print(f"Error processing new expense: {str(error)}")

def main():
    """Main function to run the expense tracker"""
    # Initialize expense tracker
    tracker = ExpenseTracker()
    
    # Set up file system observer for new expenses
    event_handler = NewExpenseHandler(tracker)
    file_observer = Observer()
    file_observer.schedule(event_handler, path='.', recursive=False)
    file_observer.start()

    print("Expense tracker is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        file_observer.stop()
        if tracker.db_connection:
            tracker.db_connection.close()
    file_observer.join()

if __name__ == "__main__":
    main()