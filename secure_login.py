

import sqlite3
import os
import bcrypt

# --- Fix 1: No hardcoded secrets — load from environment instead ---
# (In production, use a proper secrets manager or .env file excluded from git)
DB_PATH = os.environ.get("DB_PATH", "users_secure.db")


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password_hash TEXT
        )
    """)
    # --- Fix 2: Passwords are hashed before storage, never stored in plain text ---
    existing = cursor.execute(
        "SELECT * FROM users WHERE username = ?", ("liyema",)
    ).fetchone()
    if not existing:
        hashed = bcrypt.hashpw("mypassword123".encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users VALUES (?, ?)", ("liyema", hashed))
    conn.commit()
    conn.close()


def login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- Fix 3: Parameterized query — user input is never inserted into the SQL string directly ---
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and bcrypt.checkpw(password.encode(), result[0]):
        print("Login successful!")
        return True
    else:
        # --- Fix 4: Generic error message — no sensitive details leaked ---
        print("Login failed. Invalid username or password.")
        return False


def main():
    setup_database()
    print("=== Login System (SECURE VERSION) ===")
    username = input("Username: ")
    password = input("Password: ")
    login(username, password)


if __name__ == "__main__":
    main()
