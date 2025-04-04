#!/usr/bin/env python
import asyncio
import sys
import os
import getpass

from psycopg2 import IntegrityError

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database import async_session_maker
from src.users.models import User
from src.services.auth import AuthService
from src.users.schemas import UserCreate


async def create_superuser(username: str, password: str, email: str):
    """
    Create a superuser with the given username, password, and email.
    
    Args:
        username: The username for the superuser
        password: The password for the superuser
        email: The email for the superuser
    """
    # Create a session
    async with async_session_maker() as session:
        # Create an auth service
        auth_service = AuthService()
        auth_service.session = session
        
        # Hash the password
        hashed_password = auth_service.get_password_hash(password)
        
        # Create a user
        user = UserCreate(
            username=username,
            email=email,
            hashed_password=hashed_password,
        )
        
        # Add the user to the database
        try:
            # Create a new user with superuser privileges
            new_user = User(
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                is_superuser=True,
                is_admin=True
            )
            
            # Add the user to the database
            session.add(new_user)
            await session.commit()
            
            print(f"Superuser created successfully: {username}")
        except IntegrityError as e:
            print(f"Error creating superuser: Email or username already exists")
            await session.rollback()
        except Exception as e:
            print(f"Error creating superuser: {e}")
            await session.rollback()


def main():
    print("=== Create Superuser ===")
    
    # Get username
    username = input("Enter username: ").strip()
    while not username:
        print("Username cannot be empty.")
        username = input("Enter username: ").strip()
    
    # Get password (hidden input)
    password = getpass.getpass("Enter password: ")
    while not password:
        print("Password cannot be empty.")
        password = getpass.getpass("Enter password: ")
    
    # Confirm password
    confirm_password = getpass.getpass("Confirm password: ")
    while password != confirm_password:
        print("Passwords do not match.")
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
    
    # Get email
    email = input("Enter email: ").strip()
    while not email:
        print("Email cannot be empty.")
        email = input("Enter email: ").strip()
    
    # Confirm creation
    print(f"\nAbout to create superuser with:")
    print(f"Username: {username}")
    print(f"Email: {email}")
    confirm = input("Proceed? (y/n): ").strip().lower()
    
    if confirm == 'y':
        asyncio.run(create_superuser(username, password, email))
    else:
        print("Operation cancelled.")


if __name__ == "__main__":
    main()
