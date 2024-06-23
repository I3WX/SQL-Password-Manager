from cryptography.fernet import Fernet
import mysql.connector
from mysql.connector import Error
import re

# Database configuration
Host = "localhost"
db_username = "root"
db_password = "Admin"
database = "PasswordManager"

# Establish a connection to the MySQL database
try:
    conn = mysql.connector.connect(
        host=Host, user=db_username, password=db_password, database=database
    )
    cursor = conn.cursor()
    print("Connected to the MySQL database successfully.")
except Error as e:
    print(f"Error connecting to MySQL: {e}")
    conn = None  # Ensure conn is set to None if connection fails


def get_key():
    """
    Generate a new Fernet key for encryption.

    Returns:
        bytes: The generated key.
    """
    return Fernet.generate_key()


def encrypt_password(password, key):
    """
    Encrypt the given password using the provided Fernet key.

    Args:
        password (str): The password to encrypt.
        key (bytes): The encryption key.

    Returns:
        bytes: The encrypted password.
    """
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password, key):
    """
    Decrypt the given encrypted password using the provided Fernet key.

    Args:
        encrypted_password (bytes): The encrypted password.
        key (bytes): The encryption key.

    Returns:
        str: The decrypted password.
    """
    cipher_suite = Fernet(key)
    password = cipher_suite.decrypt(encrypted_password).decode()
    return password


def sanitize_platform_name(name):
    """
    Validate and sanitize the platform name to ensure it contains only
    alphanumeric characters and underscores.

    Args:
        name (str): The platform name to sanitize.

    Returns:
        str: The sanitized platform name.

    Raises:
        ValueError: If the platform name is invalid.
    """
    if re.match("^[A-Za-z0-9_]+$", name):
        return name
    else:
        raise ValueError("Invalid platform name.")


def get_data_from_user():
    """
    Prompt the user to input their username and password.

    Returns:
        tuple: The username and password entered by the user.
    """
    print("Enter your Details")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    return username, password


def display_available_platform():
    """
    Display the list of available platforms from the database.

    Returns:
        list: A list of available platform names.
    """
    query = "SHOW TABLES;"
    cursor.execute(query)
    platforms = cursor.fetchall()
    individual_platforms = [platform[0] for platform in platforms]
    for platform in individual_platforms:
        print(platform)
    return individual_platforms


def get_platform(allow_new_platform_input=True):
    """
    Prompt the user to select a platform or add a new one.

    Args:
        allow_new_platform_input (bool): Whether to allow adding a new platform.

    Returns:
        str: The selected or newly created platform name.
    """
    while True:
        individual_platforms = display_available_platform()
        if allow_new_platform_input:
            platform = input("Enter your platform (a to add a new platform): ").strip()
        else:
            platform = input("Enter your platform: ").strip()

        if platform in individual_platforms:
            return platform
        elif allow_new_platform_input and platform == "a":
            try:
                new_platform = sanitize_platform_name(
                    input("Enter name of new platform: ").strip()
                )
                query = f"CREATE TABLE {new_platform} (No INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64), password BLOB, encryption_key BLOB);"
                cursor.execute(query)
                print("New Platform Added")
                return new_platform
            except ValueError as e:
                print(e)
        else:
            print("Error in choosing platform, try again...")


def save_data(username, password, platform):
    """
    Save the given username and encrypted password for the specified platform.

    Args:
        username (str): The username to save.
        password (str): The password to save.
        platform (str): The platform name.
    """
    key = get_key()
    encrypted_password = encrypt_password(password, key)
    query = f"INSERT INTO {platform} (username, password, encryption_key) VALUES (%s, %s, %s)"
    data = (username, encrypted_password, key)
    cursor.execute(query, data)
    conn.commit()
    print(f"User {username} and password successfully saved for {platform}.")


def get_user_data(username, platform):
    """
    Retrieve and decrypt the password for the given username and platform.

    Args:
        username (str): The username to retrieve the password for.
        platform (str): The platform name.

    Returns:
        str: The decrypted password or None if no data is found.
    """
    query = f"SELECT password, encryption_key FROM {platform} WHERE username=%s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        encrypted_password, key = result
        password = decrypt_password(encrypted_password, key)
        return password
    else:
        print(f"No data found for user {username} in {platform}.")
        return None


def update_password(username, old_password, new_password, platform):
    """
    Update the password for the given username and platform if the old password matches.

    Args:
        username (str): The username to update the password for.
        old_password (str): The old password.
        new_password (str): The new password.
        platform (str): The platform name.
    """
    current_password = get_user_data(username=username, platform=platform)
    if current_password is None:
        return

    if current_password == old_password:
        key = get_key()
        encrypted_new_password = encrypt_password(new_password, key)
        query = (
            f"UPDATE {platform} SET password=%s, encryption_key=%s WHERE username=%s"
        )
        cursor.execute(query, (encrypted_new_password, key, username))
        conn.commit()
        print(f"Password for user {username} successfully updated for {platform}.")
    else:
        print("Old password does not match.")


def delete_password(username, password, platform):
    """
    Delete the password entry for the given username and platform if the password matches.

    Args:
        username (str): The username to delete the password for.
        password (str): The password to verify before deletion.
        platform (str): The platform name.
    """
    current_password = get_user_data(username=username, platform=platform)
    if current_password is None:
        return

    if current_password == password:
        query = f"DELETE FROM {platform} WHERE username=%s"
        cursor.execute(query, (username,))
        conn.commit()
        print(f"Password for {username} deleted successfully.")
    else:
        print("Password didn't match the existing database.")


def display_menu():
    """
    Display the main menu of the password manager.
    """
    print("MENU")
    print("1. Save new password")
    print("2: Check password")
    print("3: Update password")
    print("4: Delete password")
    print("5: Exit")


def main():
    """
    Main function to run the password manager application.
    """
    if not conn:
        return

    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        if choice == 1:
            platform = get_platform()
            username, password = get_data_from_user()
            save_data(username=username, password=password, platform=platform)
            print(f"Username and password saved successfully in {platform}.")
        elif choice == 2:
            platform = get_platform(allow_new_platform_input=False)
            username = input("Enter your username: ").strip()
            password = get_user_data(username, platform)
            if password:
                print(f"Password of {username} in {platform} is {password}")
        elif choice == 3:
            platform = get_platform(allow_new_platform_input=False)
            username = input("Enter your username: ").strip()
            old_password = input("Enter old password: ").strip()
            new_password = input("Enter new password: ").strip()
            update_password(
                username=username,
                old_password=old_password,
                new_password=new_password,
                platform=platform,
            )
        elif choice == 4:
            platform = get_platform(allow_new_platform_input=False)
            username = input("Enter your username: ").strip()
            password = input("Enter old password: ").strip()
            delete_password(username=username, password=password, platform=platform)
        elif choice == 5:
            break


if __name__ == "__main__":
    main()
