import json
import os
import time
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class ExpenseTracker:
    def __init__(self):
        
        # Initialize the expense tracker with database connection and file handling setup
        
        self.expenses_file = os.getenv('EXPENSES_FILE', 'expenses.json')
        self.summary_file = os.getenv('SUMMARY_FILE', 'expense_summary.json')
        self.valid_categories = {'food', 'transport', 'entertainment', 'utilities', 'other'}
        self.db_connection = self.connect_to_database()
        self.load_expenses()

    def connect_to_database(self):
        
        # Establish connection to MySQL database using environment variables
        # I NEED TO LOOK AT DB CONNECTION DEEP METHODS ETC
        
        connection = mysql.connector.connect(host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'expense_tracker'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'))
        
        try:
            
        # look for ways to define sql path -----------------------------------------------------------
        
            if connection.is_connected():
                print("Successfully connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None

    def load_expenses(self):
        
        # Load existing expenses from the database
        
        self.expense_list = []
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
                self.expense_list = cursor.fetchall()
                cursor.close()
            except Error as e:
                print(f"Error loading expenses: {e}")

    def save_expense(self, expense_data):
        
        # Save expense to MySQL database
        
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                query = """INSERT INTO expenses 
                          (user_id, category_id, amount, description, date) 
                          VALUES (%s, (SELECT category_id FROM categories WHERE name = %s), %s, %s, %s)"""
                values = (
                    expense_data['user_id'],
                    expense_data['category'],
                    expense_data['amount'],
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

    def archive_old_expenses(self, archive_date):
        
        # Archive expenses older than a specific date
        
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                query = """
                INSERT INTO archived_expenses (user_id, category_id, amount, description, date)
                SELECT user_id, category_id, amount, description, date 
                FROM expenses 
                WHERE date < %s
                """
                cursor.execute(query, (archive_date,))
                self.db_connection.commit()
                
                delete_query = "DELETE FROM expenses WHERE date < %s"
                cursor.execute(delete_query, (archive_date,))
                self.db_connection.commit()
                cursor.close()
                print(f"Archived and deleted expenses older than {archive_date}")
            except Error as e:
                print(f"Error archiving expenses: {e}")

    def validate_expense(self, expense_data):
        
        # Validate expense data before saving
        
        try:
            if not isinstance(expense_data['amount'], (int, float)) or expense_data['amount'] <= 0:
                return False, "Amount must be positive"
            
            if expense_data['category'] not in self.valid_categories:
                return False, "Invalid category"
            
            if not expense_data['description'].strip():
                return False, "Description cannot be empty"
            
            return True, ""
        except KeyError as error:
            return False, f"Missing required field: {str(error)}"

    def update_summary(self):
        
        # Update the summary file with current data
        
        summary_data = self.calculate_summary()
        if summary_data:
            try:
                with open(self.summary_file, 'w') as file:
                    json.dump(summary_data, file, indent=2)
            except Exception as e:
                print(f"Error writing summary file: {e}")

class NewExpenseHandler(FileSystemEventHandler):
    
    # Handle new expense file events
    
    def __init__(self, expense_tracker):
        self.expense_tracker = expense_tracker

    def on_created(self, event):
        
        # Process new expense files when they're created
        
        if event.src_path.endswith('new_expense.json'):
            try:
                time.sleep(0.1)
                with open(event.src_path, 'r') as file:
                    expense_data = json.load(file)
                self.expense_tracker.add_expense(expense_data)
                os.remove(event.src_path)
            except Exception as error:
                print(f"Error processing new expense: {str(error)}")

def main():
    
    # Main function to run the expense tracker
    
    tracker = ExpenseTracker()
    archive_threshold = datetime.now() - timedelta(days=365)
    tracker.archive_old_expenses(archive_threshold)

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
