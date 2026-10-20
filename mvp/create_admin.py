import sys
import os

# This ensures the script can find the 'database' and 'auth' folders
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import SessionLocal
from database.models import User
from auth.auth_handler import get_password_hash

def create_initial_admin():
    db = SessionLocal()
    # Clean up old attempts
    db.query(User).filter(User.username == "admin_kene").delete()
    
    admin = User(
        username="admin_kene",
        password_hash=get_password_hash("admin123"), 
        role="admin"
    )
    
    try:
        db.add(admin)
        db.commit()
        print("✓ Secure Admin 'admin_kene' created successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()