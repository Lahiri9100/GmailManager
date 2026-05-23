import sqlite3
from datetime import datetime

DB_NAME = "gmail_manager.db"

def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            deadline TEXT,
            tags TEXT,
            reply TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def save_email(username, deadline, tags, reply, summary):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO email_history
        (username, deadline, tags, reply, summary)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        deadline,
        tags,
        reply,
        summary
    ))

    conn.commit()
    conn.close()

def load_emails(username):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT deadline, tags, reply, summary, created_at
        FROM email_history
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    rows = cursor.fetchall()

    conn.close()

    return rows

def load_active_deadlines(username):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT deadline, tags, summary, created_at
        FROM email_history
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    rows = cursor.fetchall()

    conn.close()

    active_deadlines = []

    current_date = datetime.now()

    current_year = current_date.year

    date_formats = [

        "%B %d %Y",     # June 5 2026
        "%d %B %Y",     # 5 June 2026
        "%b %d %Y",     # Jun 5 2026
        "%d %b %Y",     # 5 Jun 2026

        "%B %d",        # June 5
        "%d %B",        # 5 June
        "%b %d",        # Jun 5
        "%d %b"         # 5 Jun
    ]

    for row in rows:

        deadline = row[0]

        cleaned_deadline = (
            deadline.replace("st", "")
                    .replace("nd", "")
                    .replace("rd", "")
                    .replace("th", "")
                    .replace(",", "")
                    .strip()
        )

        parsed_date = None

        for fmt in date_formats:

            try:

                parsed_date = datetime.strptime(
                    cleaned_deadline,
                    fmt
                )

                # add current year if missing

                if "%Y" not in fmt:

                    parsed_date = parsed_date.replace(
                        year=current_year
                    )

                break

            except:
                continue

        if parsed_date:

            if parsed_date >= current_date:

                active_deadlines.append(row)

    return active_deadlines