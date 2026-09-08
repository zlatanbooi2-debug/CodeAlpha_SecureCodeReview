

import sqlite3

# --- Flaw 1: Hardcoded credentials / secrets ---
ADMIN_PASSWORD = "admin123"
DB_PATH = "users.db"


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
    """)
    # --- Flaw 2: Storing passwords in plain text ---
    cursor.execute("INSERT INTO users VALUES ('liyema', 'mypassword123')")
    conn.commit()
    conn.close()


def login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- Flaw 3: SQL Injection ---
    # User input is inserted directly into the query string.
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        print("Login successful!")
        return True
    else:
        # --- Flaw 4: Verbose error messages ---
        print(f"Login failed for username: {username}, password: {password}")
        return False


def main():
    setup_database()
    print("=== Login System (VULNERABLE VERSION) ===")
    username = input("Username: ")
    password = input("Password: ")
    login(username, password)


if __name__ == "__main__":
    main()
