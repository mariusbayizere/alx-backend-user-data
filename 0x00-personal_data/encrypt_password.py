#!/usr/bin/env python3
"""
encrypt_password module provides functions for securely hashing passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using a salt and returns the hashed password  string.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password using the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


if __name__ == "__main__":
    # Test the hash_password function
    password = "MyAmazingPassw0rd"
    print(hash_password(password))
    print(hash_password(password))
