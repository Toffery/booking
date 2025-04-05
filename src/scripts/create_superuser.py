#!/usr/bin/env python
import asyncio
import sys
import os
import getpass


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.exceptions import ObjectAlreadyExistsException
from src.utils.db_manager import DBManager


from src.database import async_session_maker
from src.services.auth import AuthService
from src.users.schemas import SuperUserCreate


async def create_superuser(username: str, password: str, email: str):
    hashed_password = AuthService().get_password_hash(password)
    async with DBManager(session_factory=async_session_maker) as db:
        try:
            await db.auth.add(
                SuperUserCreate(username=username, hashed_password=hashed_password, email=email)
            )
            await db.commit()
            print(f"Superuser created successfully: {username}")
        except ObjectAlreadyExistsException:
            print("Error creating superuser: Email or username already exists")
        except Exception as e:
            print(f"Error creating superuser: {e}")


def main():
    print("=== Create Superuser ===")

    username = input("Enter username: ").strip()
    while not username:
        print("Username cannot be empty.")
        username = input("Enter username: ").strip()

    password = getpass.getpass("Enter password: ")
    while not password:
        print("Password cannot be empty.")
        password = getpass.getpass("Enter password: ")

    confirm_password = getpass.getpass("Confirm password: ")
    while password != confirm_password:
        print("Passwords do not match.")
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")

    email = input("Enter email: ").strip()
    while not email:
        print("Email cannot be empty.")
        email = input("Enter email: ").strip()

    print("\nAbout to create superuser with:")
    print(f"Username: {username}")
    print(f"Email: {email}")
    confirm = input("Proceed? (y/n): ").strip().lower()

    if confirm == "y":
        asyncio.run(create_superuser(username, password, email))
    else:
        print("Operation cancelled.")


if __name__ == "__main__":
    main()
