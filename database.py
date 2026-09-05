import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

DB_FILE = 'atm.db'

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_number TEXT UNIQUE NOT NULL,
        pin_hash TEXT NOT NULL,
        name TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0.0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        description TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def create_user(card_number, pin, name):
    conn = get_connection()
    cursor = conn.cursor()
    pin_hash = generate_password_hash(pin)
    try:
        cursor.execute('''
        INSERT INTO users (card_number, pin_hash, name)
        VALUES (?, ?, ?)
        ''', (card_number, pin_hash, name))
        user_id = cursor.lastrowid
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verify_pin(card_number, pin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT pin_hash FROM users WHERE card_number = ?', (card_number,))
    row = cursor.fetchone()
    conn.close()
    
    if row and check_password_hash(row[0], pin):
        return True
    return False

def get_accounts(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, account_type, balance FROM accounts WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    accounts = []
    for row in rows:
        accounts.append({
            'id': row[0],
            'account_type': row[1],
            'balance': row[2]
        })
    return accounts

def log_transaction(account_id, trans_type, amount, description):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
    INSERT INTO transactions (account_id, type, amount, timestamp, description)
    VALUES (?, ?, ?, ?, ?)
    ''', (account_id, trans_type, amount, timestamp, description))
    conn.commit()
    conn.close()

def authenticate_user(card_number, pin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, pin_hash FROM users WHERE card_number = ?', (card_number,))
    row = cursor.fetchone()
    conn.close()
    
    if row and check_password_hash(row[1], pin):
        return row[0]
    return None
