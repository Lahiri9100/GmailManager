import sqlite3

DB_NAME = "gmail_manager.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deadline TEXT,
            tags TEXT,
            reply TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_email(deadline, tags, reply, summary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO email_history (deadline, tags, reply, summary)
        VALUES (?, ?, ?, ?)
    """, (deadline, tags, reply, summary))

    conn.commit()
    conn.close()

def load_emails():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT deadline, tags, reply, summary, created_at
        FROM email_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows