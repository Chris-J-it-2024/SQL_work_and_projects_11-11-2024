# Import required libraries for database operations, file handling, and environment configuration

import json
import os
import time
from datetime import datetime, timedelta
from watchdog.observers import Observer  # Used for monitoring file system changes
from watchdog.events import FileSystemEventHandler  # Handles file system events
import mysql.connector  # MySQL database connector
from mysql.connector import Error  # MySQL error handling
from dotenv import load_dotenv  # Environment variable management

# Load environment variables from .env file
# This keeps sensitive data like database credentials secure and configurable

load_dotenv()

class ExpenseTracker:
    def __init__(self):
        """
        Initialize the expense tracker with configuration and connections
        using 
        - Sets up file paths from environment variables or defaults
        - Establishes database connection
        - Defines valid expense categories
        - Loads existing expenses from database
        """
        # Configure file paths from environment variables with fallback defaults
        
        self.expenses_file = os.getenv('EXPENSES_FILE', 'expenses.json')
        self.summary_file = os.getenv('SUMMARY_FILE', 'expense_summary.json')
        
        # Define valid expense categories to ensure data integrity
        
        self.valid_categories = {'food', 'transport', 'entertainment', 'utilities', 'other'}
        
        # Establish database connection and load existing expenses
        
        self.db_connection = self.connect_to_database()
        self.load_expenses()

    def connect_to_database(self):
        """
        Establishes connection to MySQL database using credentials from environment variables
        Returns:
            mysql.connector.connection: Active database connection or None if connection fails
        
        Note: Database connection parameters are read from environment variables for security
        """
        # Create connection using environment variables with localhost default
        
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'expense_tracker'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        
        """  
        connection = mysql.connector.connect(host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'expense_tracker'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'))
        
        # Establishing a MySQL database connection using mysql.connector
        # This code creates a connection object that handles all database communications - DOES THIS WORK IN SHELL ENVIRO
                                                                                            THE SAME WAY AS IT WOULD WORK
                                                                                            IF NOT IN AN ENVIRO ? INVESTIGATE !!
        # mysql.connector.connect() creates a new connection instance with the following parameters:
c       #  Connection = mysql.connector.connect(
        # host: Specifies the database server location
        # os.getenv('DB_HOST', 'localhost') does two things:
        # 1. Attempts to get 'DB_HOST' value from environment variables
        # 2. Falls back to 'localhost' if DB_HOST isn't found in environment - LOCAL HOST COULD BE A PROBLEM FOR PRESENTATION
        # - 'localhost' typically means the database is on the same machine - AGAIN, IS THIS GOING TO WORK FROM GitHub
        # - Could also be an IP address or domain name for remote databases - THIS COULD RESOLVE THE POTENTIAL PROBELEM ???
        host=os.getenv('DB_HOST', 'localhost'),

        # database: Specifies which database to connect to on the server
        # os.getenv('DB_NAME', 'expense_tracker'):
        # 1. Tries to get database name from DB_NAME environment variable
        # 2. Uses 'expense_tracker' as fallback if DB_NAME isn't set - THIS IS CORRECT SAFETY PROCESS IN ACTUAL ( says Marvin... )
        # - This determines which set of tables the code can access - SIMILAR TO ORACLE I THINK
        database=os.getenv('DB_NAME', 'expense_tracker'),

        # user: Database username for authentication
        # os.getenv('DB_USER'):
        # 1. Gets username from DB_USER environment variable
        # 2. No fallback provided - will be None if not set
        # - Critical security practice: username should never be hardcoded
        # - Will raise an error if DB_USER environment variable isn't set
        user=os.getenv('DB_USER'),

        # password: Database password for authentication
        # os.getenv('DB_PASSWORD'):
        # 1. Gets password from DB_PASSWORD environment variable
        # 2. No fallback provided - will be None if not set
        # - Critical security practice: password should never be hardcoded
        # - Will raise an error if DB_PASSWORD environment variable isn't set
        password=os.getenv('DB_PASSWORD')
)

    # Security Considerations:
    # - Credentials are loaded from environment variables, not hardcoded
    # - No sensitive data appears in the source code
    # - Follows security best practices for database access

    # Error Handling Notes:
    # - Connection will raise mysql.connector.Error if:
    
#   * Host is unreachable
#   * Database doesn't exist
#   * Username/password are incorrect
#   * Required environment variables are missing

    # Connection Management:
    # - Returns a connection object if successful
    # - Connection should be closed when no longer needed
    # - Best practice: Use with connection pooling for production

    # Environment Variables Required:
    # - DB_HOST (optional, defaults to 'localhost')
    # - DB_NAME (optional, defaults to 'expense_tracker')
    # - DB_USER (required)
    # - DB_PASSWORD (required)

    # Usage Example in .env file:
    # DB_HOST=mydatabase.server.com
    # DB_NAME=production_expenses
    # DB_USER=expense_admin
    # DB_PASSWORD=secure_password123

    # Common Connection Parameters Not Shown Here:
    # - port: Default is 3306 for MySQL
    # - charset: Default is 'utf8mb4'
    # - use_pure: Whether to use pure Python or C extension
    # - auth_plugin: Authentication method to use
    # - ssl_ca: Path to SSL certificate authority file
    # - connect_timeout: Timeout in seconds (default: 10)
    # - pool_name: For connection pooling
    # - pool_size: Number of connections to maintain in pool
        
        """
    Connection = mysql.connector.connect()
        #RETURNS:
         #   _type_: _description_
        
        try:
            # Verify connection is active and working
            
            if connection.is_connected():
                print("Successfully connected to MySQL database")
                return connection
        except Error as e:
            
            # Log connection errors for debugging
            
            print(f"Error connecting to MySQL database: {e}")
            return None

    def load_expenses(self):
        """
        Loads all expenses from database into memory
        - Uses dictionary cursor for easier data handling
        - Sorts expenses by date in descending order
        - Stores results in self.expense_list for quick access
        """
        self.expense_list = []
        if self.db_connection:
            try:
                # Use dictionary cursor to get results as dictionaries. No tuples yet
                
                cursor = self.db_connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
                self.expense_list = cursor.fetchall()
                cursor.close()
            except Error as e:
                print(f"Error loading expenses: {e}")

    def save_expense(self, expense_data):
        """
        Saves a new expense record to the database
        
        Args:
            expense_data (dict): Dictionary containing expense details
                Required keys: user_id, category, amount, description, date
        
        Returns:
            bool: True if save successful, False otherwise
        
        Note: Uses parameterized queries to prevent SQL injection
        """
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                
                # Use subquery to get category_id from categories table
                
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
        """
        Archives expenses older than specified date
        - Moves old records to archived_expenses table
        - Deletes archived records from main expenses table
        
        Args:
            archive_date (datetime): Date threshold for archiving
            
        Note: Uses transaction to ensure data integrity during archive process
        """
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                
                # First insert old records into archive table
                
                query = """
                INSERT INTO archived_expenses (user_id, category_id, amount, description, date)
                SELECT user_id, category_id, amount, description, date 
                FROM expenses 
                WHERE date < %s
                """
                cursor.execute(query, (archive_date,))
                self.db_connection.commit()
                
                # Then delete archived records from main table
                
                delete_query = "DELETE FROM expenses WHERE date < %s"
                cursor.execute(delete_query, (archive_date,))
                self.db_connection.commit()
                cursor.close()
                print(f"Archived and deleted expenses older than {archive_date}")
            except Error as e:
                print(f"Error archiving expenses: {e}")

    def validate_expense(self, expense_data):
        """
        Validates expense data before saving
        
        Args:
            expense_data (dict): Expense data to validate
        
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
            
        Validates:
        - Amount is positive number
        - Category is valid
        - Description is not empty
        - All required fields are present
        """
        try:
            
            # Check amount is positive number
            
            if not isinstance(expense_data['amount'], (int, float)) or expense_data['amount'] <= 0:
                return False, "Amount must be positive"
            
            # Verify category is in allowed list
            
            if expense_data['category'] not in self.valid_categories:
                return False, "Invalid category"
            
            # Ensure description is not empty
            
            if not expense_data['description'].strip():
                return False, "Description cannot be empty"
            
            return True, ""
        except KeyError as error:
            
            # Catch missing required fields
            
            return False, f"Missing required field: {str(error)}"

    def update_summary(self):
        """
        Updates summary file with current expense data
        - Calculates summary statistics
        - Writes formatted JSON to summary file
        - Used by frontend to display expense overview
        
        Note: Creates pretty-printed JSON with indent=2 for readability
        """
        summary_data = self.calculate_summary()
        if summary_data:
            try:
                with open(self.summary_file, 'w') as file:
                    json.dump(summary_data, file, indent=2)
            except Exception as e:
                print(f"Error writing summary file: {e}")

class NewExpenseHandler(FileSystemEventHandler):
    """
    Handles file system events for new expense submissions
    - Monitors for new expense JSON files
    - Processes and saves new expenses
    - Removes processed files
    
    Inherits from FileSystemEventHandler to handle file events
    """
    def __init__(self, expense_tracker):
        """
        Initialize handler with reference to expense tracker instance
        
        Args:
            expense_tracker (ExpenseTracker): Instance to handle expense processing
        """
        self.expense_tracker = expense_tracker

    def on_created(self, event):
        """
        Handles creation of new expense files
        
        Args:
            event (FileSystemEvent): Event object containing file details
            
        Note: Includes small delay to ensure file is completely written
        """
        if event.src_path.endswith('new_expense.json'):
            try:
                
                # Small delay to ensure file is fully written. Samsung 980pro SSD for-the-win
                
                time.sleep(0.1)
                with open(event.src_path, 'r') as file:
                    expense_data = json.load(file)
                self.expense_tracker.add_expense(expense_data)
                os.remove(event.src_path)  # Clean up processed file
            except Exception as error:
                print(f"Error processing new expense: {str(error)}")

def main():
    """
    Main function to run the expense tracker
    - Initializes tracker and file system observer
    - Archives old expenses
    - Runs continuous monitoring loop
    - Handles graceful shutdown
    """
    # Initialize tracker and archive old records
    
    tracker = ExpenseTracker()
    archive_threshold = datetime.now() - timedelta(days=365)
    tracker.archive_old_expenses(archive_threshold)

    # Set up file system monitoring
    
    event_handler = NewExpenseHandler(tracker)
    file_observer = Observer()
    file_observer.schedule(event_handler, path='.', recursive=False)
    file_observer.start()

    print("Expense tracker is running. Press Ctrl+C to exit.")
    try:
        # Keep program running until interrupted
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        
        # Graceful shutdown
        
        file_observer.stop()
        if tracker.db_connection:
            tracker.db_connection.close()
    file_observer.join()

# Entry point of the program

if __name__ == "__main__":
    main()