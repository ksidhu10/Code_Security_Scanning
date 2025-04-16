import os
import pymysql  # type: ignore
import urllib.error
import requests  # type: ignore
import shutil
import shlex
import subprocess  # <-- Added missing import
from urllib.request import urlopen

# Load database credentials from environment variables (Prevents hardcoding passwords)
db_config = {
    'host': os.getenv('DB_HOST', 'default_host'),
    'user': os.getenv('DB_USER', 'default_user'),
    'password': os.getenv('DB_PASSWORD', 'default_password'),
    'database': os.getenv('DB_NAME', 'default_db')  # <-- Added database name with fallback
}

def get_user_input():
    """Get user input safely."""
    return input('Enter your name: ').strip()  # <-- Added .strip() to clean up input

def send_email(to, subject, body):
    """Securely send an email using subprocess instead of os.system."""
    mail_path = shutil.which("mail")  # Get the full path of the 'mail' command
    if not mail_path:
        print("Error: 'mail' command not found.")
        return

    try:
        safe_subject = shlex.quote(subject)
        safe_to = shlex.quote(to)

        subprocess.run([mail_path, "-s", subject, to], input=body.encode(), check=True)
    except Exception as e:
        print(f"Error sending email: {e}")

def get_data():
    """Securely fetch data from an API with error handling."""
    url = "https://secure-api.com/get-data"  # Use HTTPS
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_db(data):
    """Securely insert data into the database using parameterized queries."""
    if not data:
        print("No data to save.")
        return

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:  # <-- Used context manager for cursor
            query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
            cursor.execute(query, (data, "Another Value"))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
