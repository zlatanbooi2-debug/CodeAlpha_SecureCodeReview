# Secure Coding Review — Python Login System

**Project:** CodeAlpha Cybersecurity Internship — Task 3
**Application audited:** `vulnerable_login.py` (a small Python + SQLite login system)
**Method:** Manual code inspection (line-by-line review)

## Summary

This review audits a simple login application for common security vulnerabilities. Four significant flaws were identified, each of which is explained below along with the risk it poses and the recommended fix. A remediated version (`secure_login.py`) is included in this repository, addressing all four findings.

---

## Finding 1: Hardcoded Secrets

**Location:** `ADMIN_PASSWORD = "admin123"`

**Risk:** Storing credentials directly in source code means anyone with access to the codebase (including a public GitHub repo) can see them. If this code is ever pushed to a public or shared repository, the credential is permanently exposed, even if removed later (it remains in git history).

**Severity:** High

**Recommendation:** Store secrets in environment variables, a `.env` file excluded via `.gitignore`, or a dedicated secrets manager. Never commit credentials to source control.

---

## Finding 2: Plaintext Password Storage

**Location:** `cursor.execute("INSERT INTO users VALUES ('liyema', 'mypassword123')")`

**Risk:** Passwords are stored in the database exactly as entered, with no hashing. If the database is ever leaked, breached, or accessed by an unauthorized party (including a malicious insider), every user's real password is immediately exposed — and since people commonly reuse passwords, this risk extends to their other accounts too.

**Severity:** Critical

**Recommendation:** Hash passwords before storing them, using a slow, salted hashing algorithm designed for passwords (e.g., **bcrypt**, scrypt, or Argon2) — never a fast general-purpose hash like MD5 or SHA-256 alone, since those are vulnerable to brute-force cracking at scale.

---

## Finding 3: SQL Injection

**Location:**
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

**Risk:** User input is inserted directly into the SQL query string. An attacker can manipulate the query's logic by entering specially crafted input. For example, entering:
```
' OR '1'='1
```
as the password would cause the query to always evaluate as true, bypassing authentication entirely without knowing any real password.

**Severity:** Critical

**Recommendation:** Use **parameterized queries** (also called prepared statements), where user input is passed as a separate parameter rather than concatenated into the query string:
```python
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```
This ensures user input is always treated as data, never as executable SQL logic.

---

## Finding 4: Verbose Error Messages

**Location:**
```python
print(f"Login failed for username: {username}, password: {password}")
```

**Risk:** Echoing back the submitted username and password in an error message can leak sensitive information — particularly dangerous if this output ever reaches logs, screenshots, or shared error reports. It also confirms to an attacker exactly what input they submitted, which can help them fine-tune injection attempts.

**Severity:** Medium

**Recommendation:** Return generic error messages to the user (e.g., "Invalid username or password") without echoing back submitted credentials. Detailed error information, if needed for debugging, should only go to secure server-side logs — never to the end user.

---

## Overall Risk Rating: Critical

The combination of SQL injection and plaintext password storage means this application, as originally written, could allow a complete authentication bypass and full exposure of all stored credentials with minimal effort from an attacker.

## Remediation Status

All four findings have been addressed in `secure_login.py`:

| Finding | Status |
|---|---|
| Hardcoded secrets | ✅ Fixed — moved to environment variable |
| Plaintext passwords | ✅ Fixed — bcrypt hashing added |
| SQL Injection | ✅ Fixed — parameterized queries |
| Verbose error messages | ✅ Fixed — generic error response |

## Tools & Method

This review was performed via **manual code inspection**. For a production application, this should be supplemented with automated static analysis tools such as **Bandit** (Python-specific security linter) to catch additional issues at scale.
