import sqlite3
import pandas as pd
import os
import hashlib
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- DATABASE CONFIG ---
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'shop_data.db'))

def get_connection():
    """Returns a connection object based on environment settings."""
    if DB_TYPE == "mysql":
        import mysql.connector
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
    else:
        # Default SQLite
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        return sqlite3.connect(DB_PATH)

def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Auto-increment syntax differs between MySQL and SQLite
    ai_syntax = "AUTO_INCREMENT" if DB_TYPE == "mysql" else "AUTOINCREMENT"
    pk_type = "INT PRIMARY KEY" if DB_TYPE == "mysql" else "INTEGER PRIMARY KEY"

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS transactions (
            id {pk_type} {ai_syntax},
            gender VARCHAR(10),
            age INT,
            category VARCHAR(50),
            quantity INT,
            price DECIMAL(10,2),
            payment_method VARCHAR(20),
            invoice_date VARCHAR(20),
            shopping_mall VARCHAR(50)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) PRIMARY KEY,
            password_hash VARCHAR(255)
        )
    ''')
    
    # Insert admin if not exists
    if DB_TYPE == "mysql":
        cursor.execute("SELECT username FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", 
                           ("admin", _hash_password("admin123")))
    else:
        cursor.execute("INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)", 
                       ("admin", _hash_password("admin123")))
    
    conn.commit()
    conn.close()

def register_user(username, password):
    if not username or not password: return False
    conn = get_connection()
    cursor = conn.cursor()
    try:
        q = "INSERT INTO users (username, password_hash) VALUES (%s, %s)" if DB_TYPE == "mysql" else "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        cursor.execute(q, (username.strip().lower(), _hash_password(password)))
        conn.commit()
        success = True
    except Exception as e:
        success = False 
    conn.close()
    return success

def verify_user(username, password):
    if not username or not password: return False
    conn = get_connection()
    cursor = conn.cursor()
    q = "SELECT password_hash FROM users WHERE username = %s" if DB_TYPE == "mysql" else "SELECT password_hash FROM users WHERE username = ?"
    cursor.execute(q, (username.strip().lower(),))
    row = cursor.fetchone()
    conn.close()
    if row and row[0] == _hash_password(password):
        return True
    return False

def save_transaction(data_dict):
    conn = get_connection()
    df = pd.DataFrame([data_dict])
    # to_sql handles engine detection automatically for most cases
    df.to_sql('transactions', conn, if_exists='append', index=False)
    conn.close()

def load_all_transactions():
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM transactions", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

if __name__ == "__main__":
    init_db()
    print(f"Database ({DB_TYPE.upper()}) initialized successfully.")
