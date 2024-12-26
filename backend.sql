-- Users Table
CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE
);

-- Categories Table
CREATE TABLE categories (
    category_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_name TEXT NOT NULL,
    category_type VARCHAR(50) DEFAULT NULL
);

-- Transactions Table
CREATE TABLE transactions (
    transaction_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    amount DOUBLE NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT DEFAULT NULL,
    user_id INT DEFAULT NULL,
    category_id INT DEFAULT NULL,
    transaction_type VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Budgets Table
CREATE TABLE budgets (
    budget_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_id INT DEFAULT NULL,
    amount_limit FLOAT DEFAULT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    user_id INT DEFAULT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- SavingGoals Table
CREATE TABLE savinggoals (
    goal_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    target_amount DECIMAL(10, 2) DEFAULT NULL,
    start_date DATE DEFAULT NULL,
    end_date DATE DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Reports Table
CREATE TABLE reports (
    report_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT NULL,
    report_type TEXT NOT NULL,
    report_date DATE NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Stored Procedure to Add New User
DELIMITER $$

CREATE PROCEDURE AddNewUser(
    IN first_name VARCHAR(255),
    IN last_name VARCHAR(255),
    IN email VARCHAR(255),
    IN password TEXT,
    IN username VARCHAR(255)
)
BEGIN
    INSERT INTO users(first_name, last_name, email, password, username)
    VALUES(first_name, last_name, email, password, username);
END$$

DELIMITER ;

-- Stored Procedure to Add a Transaction
DELIMITER $$

CREATE PROCEDURE AddTransaction(
    IN user_id INT,
    IN category_id INT,
    IN amount DOUBLE,
    IN transaction_date DATE,
    IN description TEXT,
    IN transaction_type VARCHAR(255)
)
BEGIN
    INSERT INTO transactions(user_id, category_id, amount, transaction_date, description, transaction_type)
    VALUES(user_id, category_id, amount, transaction_date, description, transaction_type);
    
    -- Call function to update budget after transaction
    CALL UpdateBudgetAfterTransaction(user_id, category_id, amount);
END$$

DELIMITER ;

-- Function to Update Budget After Transaction
DELIMITER $$

CREATE FUNCTION UpdateBudgetAfterTransaction(user_id INT, category_id INT, spent_amount DOUBLE)
RETURNS VOID
BEGIN
    DECLARE remaining_budget FLOAT;
    
    -- Get the budget for the given category and user
    SELECT amount_limit - IFNULL(SUM(amount), 0) 
    INTO remaining_budget
    FROM transactions
    WHERE user_id = user_id AND category_id = category_id;
    
    -- If remaining budget is less than the spent amount, update the budget
    IF remaining_budget < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Budget exceeded!';
    END IF;
    
    -- Otherwise, update the budget
    UPDATE budgets
    SET amount_limit = amount_limit - spent_amount
    WHERE user_id = user_id AND category_id = category_id;
    
END$$

DELIMITER ;

-- Trigger to Automatically Create Report After Adding a Transaction
DELIMITER $$

CREATE TRIGGER AfterTransactionInsert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    INSERT INTO reports(user_id, report_type, report_date)
    VALUES(NEW.user_id, CONCAT('Transaction Report for ', NEW.transaction_type), CURDATE());
END$$

DELIMITER ;

-- Function to Calculate the Total Spend per Category for a User
DELIMITER $$

CREATE FUNCTION GetTotalSpendPerCategory(user_id INT, category_id INT)
RETURNS DOUBLE
BEGIN
    DECLARE total_spent DOUBLE;
    
    SELECT IFNULL(SUM(amount), 0) INTO total_spent
    FROM transactions
    WHERE user_id = user_id AND category_id = category_id;
    
    RETURN total_spent;
END$$

DELIMITER ;

-- Trigger to Validate Budget Exceedance When Adding a Transaction
DELIMITER $$

CREATE TRIGGER BeforeTransactionInsert
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE remaining_budget FLOAT;
    
    -- Get the remaining budget for the given category and user
    SELECT amount_limit - IFNULL(SUM(amount), 0)
    INTO remaining_budget
    FROM transactions
    WHERE user_id = NEW.user_id AND category_id = NEW.category_id;
    
    -- If transaction exceeds the budget, prevent the insert
    IF remaining_budget < NEW.amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Budget exceeded!';
    END IF;
END$$

DELIMITER ;
