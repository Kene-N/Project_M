import hashlib
import secrets

def get_password_hash(password: str) -> str:
    """Creates a secure hash using PBKDF2 with a salt."""
    salt = secrets.token_hex(8)
    hash_gen = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return f"{salt}${hash_gen.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the stored salt and hash."""
    try:
        # Check if the password is even hashed (contains $)
        if "$" not in hashed_password:
            return False
            
        salt, stored_hash = hashed_password.split("$")
        new_hash = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt.encode(), 100000)
        return new_hash.hex() == stored_hash
    except Exception:
        return False