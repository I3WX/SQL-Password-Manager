# Password Manager

A simple Python-based password manager using MySQL for storing encrypted passwords and the `cryptography` library for encryption.

## Features

- Save new passwords
- Retrieve and display existing passwords
- Update existing passwords
- Delete passwords

## Requirements

- Python 3.6 or higher
- `cryptography` library for encryption and decryption
- `mysql-connector-python` library for MySQL interaction
- MySQL database server

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/password-manager.git
    cd password-manager
    ```

2. **Install the required Python libraries:**

    ```bash
    pip install cryptography mysql-connector-python
    ```

3. **Set up the MySQL database:**

    - Create a MySQL database called `PasswordManager`.
    - Ensure you have a MySQL user with appropriate permissions to access and modify the `PasswordManager` database.

4. **Configure the database connection:**

    Edit the connection settings in the script (`Host`, `db_username`, `db_password`, and `database`) to match your MySQL setup.

    ```python
    Host = "localhost"
    db_username = "root"
    db_password = "Admin"
    database = "PasswordManager"
    ```

## Usage

1. **Run the script:**

    ```bash
    python password_manager.py
    ```

2. **Follow the on-screen menu:**

    - **Save new password**: Enter username, password, and platform to save the encrypted password.
    - **Check password**: Retrieve and display the password for a specific username and platform.
    - **Update password**: Change the password for a specific username and platform.
    - **Delete password**: Remove the password entry for a specific username and platform.
    - **Exit**: Close the application.

## Database Schema

When a new platform is added, a table is created in the `PasswordManager` database with the following schema:

```sql
CREATE TABLE platform_name (
    No INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64),
    password BLOB,
    encryption_key BLOB
);


Replace platform_name with the actual platform name.

Security Considerations
Encryption: Passwords are encrypted using Fernet from the cryptography library, ensuring they are stored securely.
Sanitization: Platform names are validated to prevent SQL injection.
Environment: Avoid hardcoding sensitive information like database credentials in production. Use environment variables or secure vaults instead.
Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or suggestions, please reach out to utkarshs7828@gmail.com.




### Explanation

- **Title and Features**: Clearly state the purpose of the project.
- **Requirements**: List the necessary software and libraries.
- **Installation**: Provide step-by-step instructions to set up the environment.
- **Usage**: Explain how to run the script and what each menu option does.
- **Database Schema**: Describe the database structure.
- **Security Considerations**: Include notes on security practices.
- **Contributing**: Invite contributions from others.
- **License**: Mention the licensing.
- **Contact**: Provide a way to get in touch for questions or feedback.

Feel free to customize the email and GitHub URL with your actual contact information and repository link.
