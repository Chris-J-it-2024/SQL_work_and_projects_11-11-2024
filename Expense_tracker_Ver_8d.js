// Main class to handle expense tracking functionality
// Manages form submissions, data persistence, and UI updates for expense tracking
class ExpenseTracker {
    constructor() {
        // Initialize form elements by getting references to DOM elements
        // These elements are used for collecting expense input from users
        this.expense_form = document.getElementById('expense_form');
        this.amount_input = document.getElementById('amount_input');
        this.category_select = document.getElementById('category_select');
        this.description_input = document.getElementById('description_input');
        
        // Initialize display elements that show expense summaries and details
        // These elements are updated whenever new expenses are added or data is refreshed
        this.total_amount_display = document.getElementById('total_amount');
        this.category_summary = document.getElementById('category_summary');
        this.expense_list = document.getElementById('expense_list');
        
        // Set up event listener for form submission
        // Uses bind() to ensure 'this' refers to the class instance in the handler
        this.expense_form.addEventListener('submit', this.handle_form_submit.bind(this));
        
        // Initialize the display with current expense data
        this.load_summary();
        
        // Set up automatic refresh every 30 seconds to keep data current
        // Useful when multiple users might be adding expenses simultaneously
        setInterval(() => this.load_summary(), 30000);
    }

    // Handles the form submission event when a new expense is added
    // Prevents default form submission, processes the data, and updates the display
    handle_form_submit(event) {
        event.preventDefault();
        
        // Create expense object from form inputs
        // Converts amount to float and includes current timestamp
        const expense_data = {
            amount: parseFloat(this.amount_input.value),
            category: this.category_select.value,
            description: this.description_input.value,
            date: new Date().toISOString()
        };

        // Save the new expense and reset the form
        this.save_expense(expense_data);
        this.expense_form.reset();
        
        // Wait 1 second before refreshing display to allow backend processing
        // This ensures the new data is included in the summary
        setTimeout(() => this.load_summary(), 1000);
    }

    // Saves expense data by triggering a file download
    // Creates a JSON file containing the expense data that can be processed by backend
    save_expense(expense_data) {
        const download_link = document.createElement('a');
        const file_content = new Blob([JSON.stringify(expense_data)], {
            type: 'application/json'
        });
        
        // Create and trigger download of expense data
        download_link.href = URL.createObjectURL(file_content);
        download_link.download = 'new_expense.json';
        download_link.click();
        
        // Clean up to prevent memory leaks
        URL.revokeObjectURL(download_link.href);
    }

    // Fetches and displays the current expense summary
    // Makes an async request to get the latest expense data and updates UI
    async load_summary() {
        try {
            const response = await fetch('expense_summary.json');
            const data = await response.json();
            this.update_display(data);
        } catch (error) {
            console.error('Error loading summary:', error);
            this.show_error_message('Failed to load expense summary');
        }
    }

    // Updates all display elements with new expense data
    // Coordinates updates to total amount, category summary, and expense list
    update_display(data) {
        // Update the total amount display
        this.total_amount_display.textContent = this.format_currency(data.total_amount);
        
        // Update the category breakdown
        this.update_category_summary(data.category_totals);
        
        // Update the detailed list of expenses
        this.update_expense_list(data.expenses);
    }

    // Updates the category summary section with latest totals
    // Sorts categories by amount and generates HTML for each category
    update_category_summary(category_totals) {
        const sorted_categories = Object.entries(category_totals)
            .sort((a, b) => b[1] - a[1]); // Sort by amount in descending order
            
        this.category_summary.innerHTML = sorted_categories
            .map(([category, amount]) => this.create_category_item(category, amount))
            .join('');
    }

    // Creates HTML for individual category summary items
    // Includes category name, amount, and percentage of total expenses
    create_category_item(category, amount) {
        const percentage = this.calculate_percentage(amount, this.get_total_amount());
        return `
            <div class="category_item">
                <span>${this.capitalize_first_letter(category)}</span>: 
                ${this.format_currency(amount)}
                <span class="percentage">(${percentage}%)</span>
            </div>
        `;
    }

    // Calculates what percentage an amount is of the total
    // Returns 0 if total is 0 to avoid division by zero
    calculate_percentage(amount, total) {
        if (total === 0) return 0;
        return ((amount / total) * 100).toFixed(1);
    }

    // Extracts total amount from display element
    // Removes currency formatting and converts to number
    get_total_amount() {
        const total_text = this.total_amount_display.textContent;
        return parseFloat(total_text.replace(/[$,]/g, '')) || 0;
    }

    // Updates the expense list table with latest expenses
    // Generates HTML for each expense row
    update_expense_list(expenses) {
        this.expense_list.innerHTML = expenses
            .map(expense => this.create_expense_row(expense))
            .join('');
    }

    // Creates HTML for individual expense rows
    // Formats date, category, description, and amount
    create_expense_row(expense) {
        return `
            <tr>
                <td>${this.format_date(expense.date)}</td>
                <td>${this.capitalize_first_letter(expense.category)}</td>
                <td>${this.escape_html(expense.description)}</td>
                <td>${this.format_currency(expense.amount)}</td>
            </tr>
        `;
    }

    // Formats number as US currency
    // Returns string with dollar sign and proper decimal places
    format_currency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    // Formats ISO date string to user-friendly format
    // Shows date and time in local timezone
    format_date(date_string) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date_string));
    }

    // Capitalizes first letter of a string
    // Used for consistent display of categories and other text
    capitalize_first_letter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // Safely escapes HTML special characters
    // Prevents XSS attacks from user input
    escape_html(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Displays error message to user
    // Creates temporary notification that auto-removes after 5 seconds
    show_error_message(message) {
        // Create and show error notification
        const notification = document.createElement('div');
        notification.className = 'error-notification';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove notification after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Initialize the tracker once DOM is ready
// Ensures all required elements are available before creating instance
document.addEventListener('DOMContentLoaded', () => {
    new ExpenseTracker();
});