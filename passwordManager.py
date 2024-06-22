from sys import platform
from cryptography.fernet import Fernet
import mysql.connector

Host = "localhost"
username = "root"
password = "Admin"
database = "PasswordManager"

conn = mysql.connector.connect(
    host=Host, user=username, password=password, database=database
)
cursor = conn.cursor()


def get_key():
    return Fernet.generate_key()


def encrypt_password(password, key):
    cipher_suite = Fernet(key=key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password


def get_data_from_user():
    print("Enter your Details")
    username = str(input("Enter your username: "))
    password = str(input("Enter your password: "))
    return username, password


def display_available_platform():
    query = f"SHOW TABLES;"
    cursor.execute(query)
    platforms = cursor.fetchall()
    individual_platforms = [platform[0] for platform in platforms]
    for platform in individual_platforms:
        print(platform)
    return individual_platforms


def get_platform():
    individual_platforms = display_available_platform()
    platform = str(input("Enter your platform (a to add a new platform) : "))
    if platform in individual_platforms:
        return platform
    elif platform == "a":
        new_platform = input("Enter name of new platform : ")
        query = f"CREATE TABLE {new_platform} (No INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64), password BLOB, encryption_key BLOB );"
        cursor.execute(query)
        print("new Platform Added")
        return new_platform


def save_data(username, password, platform):
    key = get_key()
    encrypted_password = encrypt_password(password=password, key=key)
    query = f"INSERT INTO {platform} (username, password, encryption_key) VALUES (%s, %s, %s)"
    data = (username, encrypted_password, key)
    cursor.execute(query, data)
    conn.commit()
    print(f"User {username} and password successfully saved for {platform}.")


def display_menu():
    print("MENU")
    print("1. Save new password")
    print("2: Check password")
    print("3: Update password")
    print("4: Delete password")
    print("5: Exit")


def main():
    while True:
        display_menu()
        x = int(input("Enter your choice (1-5): "))
        if x == 1:
            username, password = get_data_from_user()
            platform = get_platform()
            save_data(username=username, password=password, platform=platform)
            print(f"Username and password saved successfully in {platform}.")
        elif x == 2:
            print("Check password feature is not implemented yet.")
        elif x == 3:
            print("Update password feature is not implemented yet.")
        elif x == 4:
            print("Delete password feature is not implemented yet.")
        elif x == 5:
            break


main()
