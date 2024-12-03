// Main class to handle expense tracking functionality
class ExpenseTracker {
    constructor() {
        // Initialize form elements
        this.expense_form = document.getElementById('expense_form');
        this.amount_input = document.getElementById('amount_input');
        this.category_select = document.getElementById('category_select');
        this.description_input = document.getElementById('description_input');
        
        // Initialize display elements
        this.total_amount_display = document.getElementById('total_amount');
        this.category_summary = document.getElementById('category_summary');
        this.expense_list = document.getElementById('expense_list');
        
        // Bind event handlers
        this.expense_form.addEventListener('submit', this.handle_form_submit.bind(this));
        
        // Load initial summary
        this.load_summary();
        
        // Set up periodic refresh (every 30 seconds)
        setInterval(() => this.load_summary(), 30000);
    }

    // Handle form submission
    handle_form_submit(event) {
        event.preventDefault();
        
        const expense_data = {
            amount: parseFloat(this.amount_input.value),
            category: this.category_select.value,
            description: this.description_input.value,
            date: new Date().toISOString()
        };

        this.save_expense(expense_data);
        this.expense_form.reset();
        
        // Refresh summary after a brief delay to allow Python processing
        setTimeout(() => this.load_summary(), 1000);
    }

    // Save expense data to file
    save_expense(expense_data) {
        const download_link = document.createElement('a');
        const file_content = new Blob([JSON.stringify(expense_data)], {
            type: 'application/json'
        });
        
        download_link.href = URL.createObjectURL(file_content);
        download_link.download = 'new_expense.json';
        download_link.click();
        
        // Clean up the URL object
        URL.revokeObjectURL(download_link.href);
    }

    // Load and display expense summary
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

    // Update the display with new data
    update_display(data) {
        // Update total amount
        this.total_amount_display.textContent = this.format_currency(data.total_amount);
        
        // Update category summary
        this.update_category_summary(data.category_totals);
        
        // Update expense list
        this.update_expense_list(data.expenses);
    }

    // Update category summary section
    update_category_summary(category_totals) {
        const sorted_categories = Object.entries(category_totals)
            .sort((a, b) => b[1] - a[1]); // Sort by amount in descending order
            
        this.category_summary.innerHTML = sorted_categories
            .map(([category, amount]) => this.create_category_item(category, amount))
            .join('');
    }

    // Create HTML for a category summary item
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

    // Calculate percentage of total
    calculate_percentage(amount, total) {
        if (total === 0) return 0;
        return ((amount / total) * 100).toFixed(1);
    }

    // Get total amount from display
    get_total_amount() {
        const total_text = this.total_amount_display.textContent;
        return parseFloat(total_text.replace(/[$,]/g, '')) || 0;
    }

    // Update expense list table
    update_expense_list(expenses) {
        this.expense_list.innerHTML = expenses
            .map(expense => this.create_expense_row(expense))
            .join('');
    }

    // Create HTML for an expense row
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

    // Utility function to format currency
    format_currency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    // Utility function to format date
    format_date(date_string) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date_string));
    }

    // Utility function to capitalize first letter
    capitalize_first_letter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // Utility function to escape HTML special characters
    escape_html(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Show error message to user
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

// Initialize the expense tracker when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    new ExpenseTracker();
});