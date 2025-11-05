"""
Authentication Utilities - Campus Resource Hub
Password hashing and verification using bcrypt.

Per .clinerules: NEVER store plaintext passwords.
Uses werkzeug.security (Flask standard, wraps bcrypt).
"""

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt (via werkzeug).

    Args:
        password: Plain text password

    Returns:
        Hashed password string

    Security:
        - Uses pbkdf2:sha256 (secure default)
        - Automatically salted
        - Computationally expensive (prevents brute force)

    Example:
        >>> hashed = hash_password('mypassword123')
        >>> assert hashed != 'mypassword123'
        >>> assert len(hashed) > 50  # Hashed passwords are long
    """
    return generate_password_hash(password, method="pbkdf2:sha256")


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        password: Plain text password to verify
        password_hash: Hashed password from database

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = hash_password('correct_password')
        >>> assert verify_password('correct_password', hashed) is True
        >>> assert verify_password('wrong_password', hashed) is False
    """
    return check_password_hash(password_hash, password)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength.

    Requirements:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> is_valid, msg = validate_password_strength('WeakPass')
        >>> assert is_valid is False
        >>>
        >>> is_valid, msg = validate_password_strength('StrongPass123')
        >>> assert is_valid is True
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"

    return True, "Password is strong"
