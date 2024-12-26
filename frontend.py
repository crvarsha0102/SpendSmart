import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import bcrypt
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Connect to MySQL (replace with your own credentials)
db = mysql.connector.connect(
    host="localhost",       
    user="root",            
    password="crvarsha0102",    
    database="SpendSmart"   
)
cursor = db.cursor()

# Main application class
class SpendSmartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SpendSmart")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        # Style Configuration
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
        self.style.configure("TButton", font=("Helvetica", 12), padding=5)

        # Login Frame
        self.login_frame = ttk.Frame(self.root, padding="10")
        self.login_frame.pack(pady=20)

        # self.dashboard_frame = ttk.Frame(root)
        # self.dashboard_frame.pack(fill="both", expand=True)

        ttk.Label(self.login_frame, text="Username").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.login_frame, text="Password").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.signup_button = ttk.Button(self.login_frame, text="Sign Up", command=self.show_signup_form)
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=5)

        # self.saving_goals_button = ttk.Button(self.dashboard_frame, text="Saving Goals", command=self.show_saving_goals_form)
        # self.saving_goals_button.pack(pady=5)

        # self.signup_button = ttk.Button(self.login_frame, text="Saving Goals", command=self.show_signup_form)
        # self.signup_button.grid(row=3, column=0, columnspan=2, pady=5)

    def login(self):
        # Get values from the login form fields
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Check if either field is empty
        if not username or not password:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        # Fetch the user from the database based on the provided username
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[4]  # Assuming password is in the 4th column
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                messagebox.showinfo("Login Success", f"Welcome, {user[1]} {user[2]}")
                self.user_id = user[0]  # Save the user ID for later use
                self.show_main_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        else:
            messagebox.showerror("Login Failed", "User not found")

    def show_signup_form(self):
    # Hide the login frame and show the signup form
        self.login_frame.pack_forget()

        # Create the signup frame and fields
        self.signup_frame = ttk.Frame(self.root, padding="10")
        self.signup_frame.pack(pady=20)

        ttk.Label(self.signup_frame, text="First Name").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.signup_first_name_entry = ttk.Entry(self.signup_frame, width=30)
        self.signup_first_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.signup_frame, text="Last Name").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.signup_last_name_entry = ttk.Entry(self.signup_frame, width=30)
        self.signup_last_name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.signup_frame, text="Username").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.signup_username_entry = ttk.Entry(self.signup_frame, width=30)
        self.signup_username_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.signup_frame, text="Email").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.signup_email_entry = ttk.Entry(self.signup_frame, width=30)
        self.signup_email_entry.grid(row=3, column=1, pady=5)

        ttk.Label(self.signup_frame, text="Password").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.signup_password_entry = ttk.Entry(self.signup_frame, show="*", width=30)
        self.signup_password_entry.grid(row=4, column=1, pady=5)

        self.signup_submit_button = ttk.Button(self.signup_frame, text="Create Account", command=self.signup)
        self.signup_submit_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Corrected back button for signup frame
        self.back_button_signup = ttk.Button(self.signup_frame, text="Back", command=self.show_login_form)
        self.back_button_signup.grid(row=6, column=0, columnspan=2, pady=5)

    # New method to show the login form when the back button is clicked in signup
    def show_login_form(self):
        self.signup_frame.pack_forget()
        self.login_frame.pack(pady=20)

        # Update the _init_ method to add a back button in the login frame
        self.back_button_login = ttk.Button(self.login_frame, text="Back", command=self.root.quit)
        self.back_button_login.grid(row=4, column=0, columnspan=2, pady=5)

    def signup(self):
        # Get values from the signup form fields
        first_name = self.signup_first_name_entry.get().strip()
        last_name = self.signup_last_name_entry.get().strip()
        username = self.signup_username_entry.get().strip()
        email = self.signup_email_entry.get().strip()
        password = self.signup_password_entry.get().strip()

        # Check if any field is empty
        if not first_name or not last_name or not username or not email or not password:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        # Encrypt the password before saving
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            # Attempt to insert the new user record into the database
            cursor.execute(
                "INSERT INTO Users (first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s)", 
                (first_name, last_name, username, email, hashed_password)
            )
            db.commit()
            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            # Return to the login frame after signup
            self.signup_frame.pack_forget()
            self.login_frame.pack(pady=20)
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username or Email already exists.")
    
    def show_main_dashboard(self):
        self.login_frame.pack_forget()

        self.dashboard_frame = ttk.Frame(self.root, padding="10")
        self.dashboard_frame.pack(pady=20)

        self.add_transaction_button = ttk.Button(self.dashboard_frame, text="Add Transaction", command=self.show_transaction_form)
        self.add_transaction_button.pack(pady=5)

        self.view_transactions_button = ttk.Button(self.dashboard_frame, text="View Transactions", command=self.view_transactions)
        self.view_transactions_button.pack(pady=5)

        self.set_budget_button = ttk.Button(self.dashboard_frame, text="Set Budget", command=self.show_budget_form)
        self.set_budget_button.pack(pady=5)

        self.view_report_button = ttk.Button(self.dashboard_frame, text="View Report", command=self.view_report)
        self.view_report_button.pack(pady=5)

        self.saving_goals_button = ttk.Button(self.dashboard_frame, text="Saving Goals", command=self.show_saving_goals_form)
        self.saving_goals_button.pack(pady=5)

    def view_report(self):
        self.dashboard_frame.pack_forget()

        self.report_frame = ttk.Frame(self.root, padding="10")
        self.report_frame.pack(pady=20)

        ttk.Label(self.report_frame, text="Start Date (YYYY-MM-DD)").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.start_date_entry = ttk.Entry(self.report_frame, width=30)
        self.start_date_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.report_frame, text="End Date (YYYY-MM-DD)").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.end_date_entry = ttk.Entry(self.report_frame, width=30)
        self.end_date_entry.grid(row=1, column=1, pady=5)

        self.show_report_button = ttk.Button(self.report_frame, text="Show Report", command=self.show_income_expense_report)
        self.show_report_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.back_button = ttk.Button(self.report_frame, text="Back", command=self.cancel_report_view)
        self.back_button.grid(row=3, column=0, columnspan=2, pady=5)

    def show_income_expense_report(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        cursor.execute(
            "SELECT transaction_type, SUM(amount) "
            "FROM Transactions "
            "WHERE user_id = %s AND transaction_date BETWEEN %s AND %s "
            "GROUP BY transaction_type",
            (self.user_id, start_date, end_date)
        )
        totals = cursor.fetchall()

        transaction_types = [row[0] for row in totals]
        amounts = [row[1] for row in totals]

        cursor.execute(
            "SELECT c.category_name, SUM(t.amount) "
            "FROM Transactions t "
            "JOIN Categories c ON t.category_id = c.category_id "
            "WHERE t.user_id = %s AND t.transaction_date BETWEEN %s AND %s AND t.transaction_type = 'Expense' "
            "GROUP BY c.category_name",
            (self.user_id, start_date, end_date)
        )
        category_totals = cursor.fetchall()

        categories = [row[0] for row in category_totals]
        category_amounts = [row[1] for row in category_totals]

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)  
        plt.bar(transaction_types, amounts, color=['green', 'red'])
        plt.xlabel("Transaction Type")
        plt.ylabel("Amount")
        plt.title("Income vs Expense")

        plt.subplot(1, 2, 2)  
        plt.barh(categories, category_amounts, color='blue')
        plt.xlabel("Amount Spent")
        plt.ylabel("Category")
        plt.title("Amount Spent per Category")

        plt.tight_layout()
        plt.show()

    def cancel_report_view(self):
        self.report_frame.pack_forget()
        self.show_main_dashboard()

    def show_budget_form(self):
        self.dashboard_frame.pack_forget()

        self.budget_frame = ttk.Frame(self.root, padding="10")
        self.budget_frame.pack(pady=20)

        ttk.Label(self.budget_frame, text="Category Name").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.budget_category_entry = ttk.Entry(self.budget_frame, width=30)
        self.budget_category_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.budget_frame, text="Budget Amount").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.budget_amount_entry = ttk.Entry(self.budget_frame, width=30)
        self.budget_amount_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.budget_frame, text="Start Date (YYYY-MM-DD)").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.budget_start_date_entry = ttk.Entry(self.budget_frame, width=30)
        self.budget_start_date_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.budget_frame, text="End Date (YYYY-MM-DD)").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.budget_end_date_entry = ttk.Entry(self.budget_frame, width=30)
        self.budget_end_date_entry.grid(row=3, column=1, pady=5)

        self.submit_budget_button = ttk.Button(self.budget_frame, text="Submit Budget", command=self.submit_budget)
        self.submit_budget_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.back_button_budget_button = ttk.Button(self.budget_frame, text="Back", command=self.cancel_budget_form)
        self.back_button_budget_button.grid(row=5, column=0, columnspan=2, pady=5)

    def submit_budget(self):
        category_name = self.budget_category_entry.get()
        amount = float(self.budget_amount_entry.get())
        start_date = self.budget_start_date_entry.get()
        end_date = self.budget_end_date_entry.get()

        cursor.execute("SELECT category_id FROM Categories WHERE category_name = %s", (category_name,))
        category = cursor.fetchone()

        if not category:
            cursor.execute("INSERT INTO Categories (category_name) VALUES (%s)", (category_name,))
            db.commit()
            cursor.execute("SELECT category_id FROM Categories WHERE category_name = %s", (category_name,))
            category = cursor.fetchone()

        category_id = category[0]

        cursor.execute(
            "INSERT INTO Budgets (user_id, category_id, amount_limit, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
            (self.user_id, category_id, amount, start_date, end_date)
        )
        db.commit()

        cursor.execute(
            "SELECT SUM(t.amount) "
            "FROM Transactions t "
            "WHERE t.user_id = %s AND t.category_id = %s AND t.transaction_type = 'Expense' "
            "AND t.transaction_date BETWEEN %s AND %s",
            (self.user_id, category_id, start_date, end_date)
        )
        total_expenses = cursor.fetchone()[0] or 0  

        if total_expenses > amount:
            messagebox.showwarning("Budget Exceeded", f"Warning: You have already exceeded your budget of {amount} for the category '{category_name}'!")
        else:
            messagebox.showinfo("Success", "Budget set successfully!")

        self.budget_frame.pack_forget()
        self.show_main_dashboard()

    def cancel_budget_form(self):
        self.budget_frame.pack_forget()
        self.show_main_dashboard()

    def show_transaction_form(self):
        self.dashboard_frame.pack_forget()

        self.transaction_frame = ttk.Frame(self.root, padding="10")
        self.transaction_frame.pack(pady=20)

        ttk.Label(self.transaction_frame, text="Amount").grid(row=0, column=0 , sticky=tk.W, pady=5)
        self.transaction_amount_entry = ttk.Entry(self.transaction_frame, width=30)
        self.transaction_amount_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.transaction_frame, text="Description").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.transaction_description_entry = ttk.Entry(self.transaction_frame, width=30)
        self.transaction_description_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.transaction_frame, text="Category (Enter Category)").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.transaction_category_entry = ttk.Entry(self.transaction_frame, width=30)
        self.transaction_category_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.transaction_frame, text="Transaction Date").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.transaction_date_entry = ttk.Entry(self.transaction_frame, width=30)
        self.transaction_date_entry.grid(row=3, column=1, pady=5)

        ttk.Label(self.transaction_frame, text="Transaction Type (Income/Expense)").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.transaction_type_entry = ttk.Entry(self.transaction_frame, width=30)
        self.transaction_type_entry.grid(row=4, column=1, pady=5)

        self.submit_transaction_button = ttk.Button(self.transaction_frame, text="Submit", command=self.submit_transaction)
        self.submit_transaction_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.cancel_transaction_button = ttk.Button(self.transaction_frame, text="Back", command=self.cancel_transaction_form)
        self.cancel_transaction_button.grid(row=6, column=0, columnspan=2, pady=5)

    def submit_transaction(self):
        amount = float(self.transaction_amount_entry.get())
        description = self.transaction_description_entry.get()
        category_name = self.transaction_category_entry.get()
        transaction_date = self.transaction_date_entry.get()
        transaction_type = self.transaction_type_entry.get()

        cursor.execute("SELECT category_id FROM Categories WHERE category_name = %s", (category_name,))
        category = cursor.fetchone()

        if not category:
            cursor.execute("INSERT INTO Categories (category_name) VALUES (%s)", (category_name,))
            db.commit()
            cursor.execute("SELECT category_id FROM Categories WHERE category_name = %s", (category_name,))
            category = cursor.fetchone()

        category_id = category[0]

        cursor.execute(
            "SELECT Budgets.amount_limit, Budgets.start_date, Budgets.end_date "
            "FROM Budgets "
            "WHERE Budgets.user_id = %s AND Budgets.category_id = %s "
            "AND %s BETWEEN Budgets.start_date AND Budgets.end_date",
            (self.user_id, category_id, transaction_date)
        )
        budget = cursor.fetchone()

        if budget:
            cursor.execute(
                "SELECT SUM(Transactions.amount) "
                "FROM Transactions "
                "WHERE Transactions.user_id = %s AND Transactions.category_id = %s "
                "AND Transactions.transaction_type = 'Expense' "
                "AND Transactions.transaction_date BETWEEN %s AND %s",
                (self.user_id, category_id, budget[1], budget[2])
            )
            total_expenses = cursor.fetchone()[0] or 0

            if total_expenses + amount > budget[0]:
                messagebox.showwarning("Budget Exceeded", f"Warning: Adding this transaction will exceed your budget of {budget[0]} for the category '{category_name}'.")
                return

        cursor.execute(
            "INSERT INTO Transactions (user_id, amount, description, category_id, transaction_date, transaction_type) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (self.user_id, amount, description, category_id, transaction_date, transaction_type)
        )
        db.commit()
        messagebox.showinfo("Success", "Transaction added successfully!")
        self.transaction_frame.pack_forget()
        self.show_main_dashboard()

    def cancel_transaction_form(self):
        self.transaction_frame.pack_forget()
        self.show_main_dashboard()

    def view_transactions(self):
        self.dashboard_frame.pack_forget()
        self.transactions_frame = ttk.Frame(self.root, padding="10")
        self.transactions_frame.pack(pady=20)

        cursor.execute(
            "SELECT t.transaction_id, t.amount, t.description, c.category_name, t.transaction_date, t.transaction_type "
            "FROM Transactions t "
            "JOIN Categories c ON t.category_id = c.category_id "
            "WHERE t.user_id = %s", 
            (self.user_id,)
        )
        transactions = cursor.fetchall()

        # Create headers
        headers = ["Amount", "Description", "Category", "Date", "Type", "Action"]
        for j, header in enumerate(headers):
            ttk.Label(self.transactions_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=j)

        # Store UI elements for later removal
        self.transaction_widgets = []

        for i, transaction in enumerate(transactions, start=1):
            row_widgets = []
            for j, value in enumerate(transaction[:-1]):  # Exclude the transaction_id for display
                label = ttk.Label(self.transactions_frame, text=value)
                label.grid(row=i, column=j)
                row_widgets.append(label)

            # Create a delete button for each transaction
            delete_button = ttk.Button(self.transactions_frame, text="Delete", 
                command=lambda transaction_id=transaction[0], row_widgets=row_widgets: self.delete_transaction(transaction_id, row_widgets))
            delete_button.grid(row=i, column=len(headers) - 1)
            row_widgets.append(delete_button)  # Store the button as well

            # Store all widgets in the transaction_widgets list
            self.transaction_widgets.append(row_widgets)

        self.back_button = ttk.Button(self.transactions_frame, text="Back", command=self.go_back_to_dashboard)
        self.back_button.grid(row=len(transactions) + 1, column=2, pady=10)
    
    def go_back_to_dashboard(self):
        self.transactions_frame.pack_forget()
        self.show_main_dashboard()

    def display_expense_pie_chart(self, start_date, end_date):
        cursor.execute(
            "SELECT Categories.category_name, SUM(Transactions.amount) "
            "FROM Transactions "
            "JOIN Categories ON Transactions.category_id = Categories.category_id "
            "WHERE Transactions.user_id = %s AND Transactions.transaction_date BETWEEN %s AND %s AND Transactions.transaction_type = 'Expense' "
            "GROUP BY Categories.category_name",
            (self.user_id, start_date, end_date)
        )
        category_totals = cursor.fetchall()

        categories = [row[0] for row in category_totals]
        amounts = [row[1] for row in category_totals]

        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax.set_title("Expenses by Category")

        canvas = FigureCanvasTkAgg(fig, master=self.report_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        back_button = ttk.Button(self.report_frame, text="Back", command=self.cancel_report_view)
        back_button.pack(pady=10)

    def show_saving_goals_form(self):
        self.dashboard_frame.pack_forget()

        self.saving_goals_frame = ttk.Frame(self.root, padding="10")
        self.saving_goals_frame.pack(pady=20)

        ttk.Label(self.saving_goals_frame, text="Target Saving Amount").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.saving_amount_entry = ttk.Entry(self.saving_goals_frame, width=30)
        self.saving_amount_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.saving_goals_frame, text="Start Date (YYYY-MM-DD)").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.saving_start_date_entry = ttk.Entry(self.saving_goals_frame, width=30)
        self.saving_start_date_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.saving_goals_frame, text="End Date (YYYY-MM-DD)").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.saving_end_date_entry = ttk.Entry(self.saving_goals_frame, width=30)
        self.saving_end_date_entry.grid(row=2, column=1, pady=5)

        self.submit_saving_goal_button = ttk.Button(self.saving_goals_frame, text="Set Saving Goal", command=self.submit_saving_goal)
        self.submit_saving_goal_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.view_progress_button = ttk.Button(self.saving_goals_frame, text="View Saving Progress", command=self.view_saving_progress)
        self.view_progress_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.back_button = ttk.Button(self.saving_goals_frame, text="Back", command=self.cancel_saving_goals_form)
        self.back_button.grid(row=5, column=0, columnspan=2, pady=5)

    def submit_saving_goal(self):
        try:
            target_amount = float(self.saving_amount_entry.get())
            start_date = self.saving_start_date_entry.get()
            end_date = self.saving_end_date_entry.get()

            # Validate dates
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                return

            # Insert the saving goal into the database
            cursor.execute(
                "INSERT INTO SavingGoals (user_id, target_amount, start_date, end_date) "
                "VALUES (%s, %s, %s, %s)",
                (self.user_id, target_amount, start_date, end_date)
            )
            db.commit()
            messagebox.showinfo("Success", "Saving goal set successfully!")
            
            # Clear the entry fields after successful submission
            self.saving_amount_entry.delete(0, tk.END)
            self.saving_start_date_entry.delete(0, tk.END)
            self.saving_end_date_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def view_saving_progress(self):
        # Clear the current frame
        for widget in self.saving_goals_frame.winfo_children():
            widget.destroy()

        # Get the most recent saving goal
        cursor.execute(
            "SELECT target_amount, start_date, end_date FROM SavingGoals "
            "WHERE user_id = %s ORDER BY goal_id DESC LIMIT 1",
            (self.user_id,)
        )
        goal = cursor.fetchone()

        if not goal:
            messagebox.showinfo("No Goals", "No saving goals found. Please set a saving goal first.")
            self.show_saving_goals_form()
            return

        target_amount, start_date, end_date = goal
        target_amount = float(target_amount)

        # Calculate total income and expenses for the period
        cursor.execute(
            "SELECT transaction_type, SUM(amount) FROM Transactions "
            "WHERE user_id = %s AND transaction_date BETWEEN %s AND %s "
            "GROUP BY transaction_type",
            (self.user_id, start_date, end_date)
        )
        
        transactions = dict(cursor.fetchall())
        total_income = float(transactions.get('Income', 0) or 0)
        total_expenses = float(transactions.get('Expense', 0) or 0)
        current_savings = total_income - total_expenses

        # Calculate progress percentage
        progress_percentage = (current_savings / target_amount) * 100 if target_amount > 0 else 0
        
        # Display the results
        ttk.Label(self.saving_goals_frame, text=f"Saving Goal: Rs{target_amount:,.2f}", font=("Arial", 12, "bold")).pack(pady=5)
        ttk.Label(self.saving_goals_frame, text=f"Current Savings: Rs{current_savings:,.2f}", font=("Arial", 12)).pack(pady=5)
        
        if current_savings >= target_amount:
            ttk.Label(self.saving_goals_frame, text="Congratulations! You've reached your saving goal!", 
                    font=("Arial", 12, "bold"), foreground="green").pack(pady=5)
        else:
            remaining = target_amount - current_savings
            ttk.Label(self.saving_goals_frame, text=f"Amount still needed: Rs{remaining:,.2f}", 
                    font=("Arial", 12), foreground="red").pack(pady=5)

        # Add labels to show the total income and expenses
        ttk.Label(self.saving_goals_frame, text=f"Total Income: Rs{total_income:,.2f}", 
                font=("Arial", 12)).pack(pady=5)
        ttk.Label(self.saving_goals_frame, text=f"Total Expenses: Rs{total_expenses:,.2f}", 
                font=("Arial", 12)).pack(pady=5)

        # Show date range
        ttk.Label(self.saving_goals_frame, text=f"Time Period: {start_date} to {end_date}", 
                font=("Arial", 12)).pack(pady=5)

        # Back button to return to the saving goals form
        back_button = ttk.Button(self.saving_goals_frame, text="Back", command=self.cancel_saving_goals_form)
        back_button.pack(pady=10)

    def cancel_saving_goals_form(self):
        self.saving_goals_frame.pack_forget()
        self.show_main_dashboard()

    def delete_transaction(self, transaction_id, row_widgets):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this transaction?")
        if confirm:
            try:
                # Delete from the database
                cursor.execute("DELETE FROM Transactions WHERE transaction_id = %s", (transaction_id,))
                db.commit()
                messagebox.showinfo("Success", "Transaction deleted successfully!")

                # Remove the UI elements
                for widget in row_widgets:
                    widget.grid_forget()  # Remove the widget from the grid

                # Optionally, you can refresh the entire view if needed
                # self.view_transactions()  # Uncomment this if you want to refresh the entire view

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

# Start the application
root = tk.Tk()
app = SpendSmartApp(root)
root.mainloop()
