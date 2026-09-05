import sqlite3
import database

def withdraw(account_id, amount):
    if amount <= 0:
        return False, "Amount must be positive."
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        if not row:
            return False, "Account not found."
        balance = row[0]
        if balance < amount:
            return False, "Insufficient funds."
        new_balance = balance - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        conn.commit()
        database.log_transaction(account_id, 'WITHDRAWAL', amount, 'ATM Withdrawal')
        conn.close()
        return True, f"Successfully withdrew ${amount:.2f}"
    except Exception as e:
        return False, str(e)

def deposit(account_id, amount):
    if amount <= 0:
        return False, "Amount must be positive."
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        if not row:
            return False, "Account not found."
        new_balance = row[0] + amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        conn.commit()
        database.log_transaction(account_id, 'DEPOSIT', amount, 'ATM Deposit')
        conn.close()
        return True, f"Successfully deposited ${amount:.2f}"
    except Exception as e:
        return False, str(e)

def transfer(from_acc_id, to_acc_id, amount):
    if amount <= 0:
        return False, "Amount must be positive."
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_acc_id,))
        row = cursor.fetchone()
        if not row:
            return False, "Source account not found."
        if row[0] < amount:
            return False, "Insufficient funds."
            
        cursor.execute("SELECT id FROM accounts WHERE id = ?", (to_acc_id,))
        if not cursor.fetchone():
            return False, "Destination account not found."
            
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_acc_id))
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_acc_id))
        conn.commit()
        
        database.log_transaction(from_acc_id, 'TRANSFER_OUT', amount, f'Transfer to account {to_acc_id}')
        database.log_transaction(to_acc_id, 'TRANSFER_IN', amount, f'Transfer from account {from_acc_id}')
        conn.close()
        return True, f"Successfully transferred ${amount:.2f}"
    except Exception as e:
        return False, str(e)

def pay_tax(account_id, amount):
    if amount <= 0:
        return False, "Amount must be positive."
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
        row = cursor.fetchone()
        if not row:
            return False, "Account not found."
        if row[0] < amount:
            return False, "Insufficient funds."
            
        new_balance = row[0] - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        conn.commit()
        
        database.log_transaction(account_id, 'TAX_PAYMENT', amount, 'Government Tax Payment')
        conn.close()
        return True, f"Successfully paid tax of ${amount:.2f}"
    except Exception as e:
        return False, str(e)

def get_statement(account_id, limit=10):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, amount, timestamp, description FROM transactions WHERE account_id = ? ORDER BY timestamp DESC LIMIT ?", (account_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "type": r[1], "amount": r[2], "timestamp": r[3], "description": r[4]} for r in rows]

def setup_mock_data():
    conn = database.get_connection()
    cursor = conn.cursor()
    tables = ['transactions', 'accounts', 'users']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    conn.close()
    
    database.init_db()
    
    # Use create_user to properly hash PIN
    user_id = database.create_user('1111222233334444', '1234', 'John Doe')
    
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (id, user_id, account_type, balance) VALUES (?, ?, ?, ?)", (1, user_id, 'Checking', 1000.00))
    cursor.execute("INSERT INTO accounts (id, user_id, account_type, balance) VALUES (?, ?, ?, ?)", (2, user_id, 'Savings', 5000.00))
    conn.commit()
    conn.close()
