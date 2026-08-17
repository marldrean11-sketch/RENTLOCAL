from database.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash


def register_user(name, email, password, role="renter"):
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "All fields are required."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if role not in ("renter", "owner"):
        return False, "Invalid role."

    connection = get_db_connection()

    existing_user = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user:
        connection.close()
        return False, "An account with this email already exists."

    password_hash = generate_password_hash(password)

    connection.execute(
        """
        INSERT INTO users (
            name,
            email,
            password_hash,
            role
        )
        VALUES (?, ?, ?, ?)
        """,
        (name, email, password_hash, role)
    )

    connection.commit()
    connection.close()

    return True, "Account created successfully."


def login_user(email, password):
    email = email.strip().lower()

    if not email or not password:
        return False, None, "Email and password are required."

    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT id, name, email, password_hash, role, is_active
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if not user:
        return False, None, "Invalid email or password."

    if not user["is_active"]:
        return False, None, "This account is inactive."

    if not check_password_hash(user["password_hash"], password):
        return False, None, "Invalid email or password."

    return True, user, "Login successful."