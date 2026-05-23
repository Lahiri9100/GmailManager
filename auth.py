import sqlite3
import bcrypt

DB_NAME = "gmail_manager.db"

def create_users_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (
            username,
            hashed_password
        ))

        conn.commit()

        return True

    except:
        return False

    finally:
        conn.close()

def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT password
        FROM users
        WHERE username = ?
    """, (username,))

    result = cursor.fetchone()

    conn.close()

    if result:

        stored_password = result[0]

        if bcrypt.checkpw(
            password.encode(),
            stored_password
        ):
            return True

    return False