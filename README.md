# SpendSmart

SpendSmart is a simple personal finance management application focusing on saving goals, built using Python and Tkinter. It allows users to track their transactions, categorize expenses, and stay within their monthly spending limit.

## Features

- **User Authentication**: Sign up and log in with a secure, hashed password.
- **Transaction Management**: Add and view transactions categorized as income or expenses.
- **Spending Limit Enforcement**: Automatically checks and enforces a user's monthly spending limit for expenses.
- **Category Management**: Dynamically adds new categories for transactions.

## Requirements

To run this project, ensure you have the following installed:

- Python 3.x
- MySQL database server
- Required Python libraries

## Setup Instructions
1. **Configure MySQL Database**
-Create a database named SpendSmart.
-Execute the SQL statements to set up the necessary tables i.e run backend.sql
2. **Configure Database Connection**
-In the frontend.py script, update the db configuration with your MySQL credentials
3. **Run the Application**
Run the SpendSmartApp script: python frontend.py
