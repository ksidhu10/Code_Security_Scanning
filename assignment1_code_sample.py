import os
import pymysql
import urllib.error
import subprocess
from urllib.request import urlopen

# Load database credentials from environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'default_host'),
    'user': os.getenv('DB_USER', 'default_user'),
    'password': os.getenv('DB_PASSWORD', 'default_password')
}

def get_user_input():
    return input('Enter your name: ')

def send_email(to, subject, body):
    subprocess.run(["mail", "-s", subject, to], input=body.encode())

def get_data():
    url = 'http://insecure-api.com/get-data'
    try:
        response = urlopen(url)
        return response.read().decode()
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_db(data):
    if data is None:
        print("No data to save.")
        return
    
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
        cursor.execute(query, (data, "Another Value"))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
