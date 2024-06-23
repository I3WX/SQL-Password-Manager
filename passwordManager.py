from turtle import update
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


def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key=key)
    password = cipher_suite.decrypt(encrypted_password).decode()
    return password


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


def get_platform(allow_new_platform_input=True):
    while True:
        individual_platforms = display_available_platform()
        if allow_new_platform_input:
            platform = str(input("Enter your platform (a to add a new platform): "))
        else:
            platform = str(input("Enter your platform: "))

        if platform in individual_platforms:
            return platform
        elif allow_new_platform_input and platform == "a":
            new_platform = input("Enter name of new platform : ")
            query = f"CREATE TABLE {new_platform} (No INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(64), password BLOB, encryption_key BLOB );"
            cursor.execute(query)
            print("New Platform Added")
            return new_platform
        else:
            print("Error in choosing try again...")


def save_data(username, password, platform):
    key = get_key()
    encrypted_password = encrypt_password(password=password, key=key)
    query = f"INSERT INTO {platform} (username, password, encryption_key) VALUES (%s, %s, %s)"
    data = (username, encrypted_password, key)
    cursor.execute(query, data)
    conn.commit()
    print(f"User {username} and password successfully saved for {platform}.")


def get_user_data(username, platform):
    query = ("SELECT password, encryption_key FROM {} WHERE username=%s;").format(
        platform
    )
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        encrypted_password, key = result
        password = decrypt_password(
            encrypted_password=encrypted_password.decode(), key=key.decode()
        )
        return password


def update_password(username, old_password, new_password, platform):
    password = get_user_data(username=username, platform=platform)
    if password == old_password:
        key = get_key()
        encrypted_new_password = encrypt_password(password=new_password, key=key)
        query = (
            f"UPDATE {platform} SET password=%s, encryption_key=%s WHERE username=%s"
        )
        cursor.execute(query, (encrypted_new_password, key, username))
        conn.commit()
        print(f"User {username} and password successfully updated for {platform}.")


def Delete_password(username, password, platform):
    password = get_user_data(username=username, platform=platform)
    if password == password:
        query = f"DELETE FROM {platform} WHERE username=%s"
        cursor.execute(query, (username,))
        conn.commit()
        print(f"Password for {username} deleted successfully.")
    else:
        print("Password didn't match with exiting database")


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
            q = input("Enter q to quit else press any button : ")
            if q == "q":
                break
            else:
                continue
        elif x == 2:
            platform = get_platform(allow_new_platform_input=False)
            username = str(input("Enter your username: "))
            password = get_user_data(username, platform)
            print(f"Password of {username} in {platform} is \n {password}")
            q = input("Enter q to quit else press any button : ")
            if q == "q":
                break
            else:
                continue
        elif x == 3:
            platform = get_platform(allow_new_platform_input=False)
            username = str(input("Enter your username: "))
            old_password = str(input("Enter old password: "))
            new_password = str(input("Enter new password: "))
            update_password(username, old_password, new_password, platform)
            q = input("Enter q to quit else press any button : ")
            if q == "q":
                break
            else:
                continue
        elif x == 4:
            platform = get_platform(allow_new_platform_input=False)
            username = str(input("Enter your username: "))
            password = str(input("Enter old password: "))
            Delete_password(username=username, password=password, platform=platform)
            q = input("Enter q to quit else press any button : ")
            if q == "q":
                break
            else:
                continue
        elif x == 5:
            break


main()
