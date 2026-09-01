import sys
import os

# Add root folder to path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import User  # Adjust import based on your actual User model file
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_initial_admin():
    db = SessionLocal()
    try:
        username = "munene"
        password = "Admin@MSec2026"  # Put your target admin password here
        hashed_password = pwd_context.hash(password)

        existing_user = db.query(User).filter(User.username == username).first()

        if existing_user:
            existing_user.hashed_password = hashed_password
            print(f"Password for user '{username}' updated successfully.")
        else:
            admin_user = User(
                username=username,
                hashed_password=hashed_password,
                is_admin=True  # Adjust fields to match your User model schema
            )
            db.add(admin_user)
            print(f"Admin user '{username}' created successfully.")

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error creating admin: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_admin()