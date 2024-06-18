import sqlite3
from connect import create_connection
from faker import Faker
import random

fake = Faker()


def create_connection():
    conn = sqlite3.connect('data_hw.db')
    return conn


def create_users(conn):
    users = [
        {'fullname': fake.name(), 'email': fake.email()},
        {'fullname': fake.name(), 'email': fake.email()},
        {'fullname': fake.name(), 'email': fake.email()}
    ]
    cursor = conn.cursor()
    for user in users:
        cursor.execute("""
            INSERT INTO users (fullname, email) VALUES (?,?)
            ON CONFLICT(email) DO NOTHING
        """, (user['fullname'], user['email']))
    conn.commit()


def create_status(conn):
    statuses = [
        {'name': 'new'},
        {'name': 'in progress'},
        {'name': 'completed'}
    ]
    cursor = conn.cursor()
    for status in statuses:
        cursor.execute("""
            INSERT INTO status (name) VALUES (?)
            ON CONFLICT(name) DO NOTHING
        """, (status['name'],))
    conn.commit()


def create_tasks(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT id FROM status")
    statuses = cursor.fetchall()

    tasks_data = []
    for _ in range(10):  # Генеруємо 10 завдань
        task = {
            'title': fake.sentence(),
            'description': fake.text(),
            'status_id': random.choice(statuses)[0],
            'user_id': random.choice(users)[0]
        }
        tasks_data.append(task)

    for task in tasks_data:
        cursor.execute("""
            INSERT INTO tasks (title, description, status_id, user_id) 
            VALUES (?,?,?,?)
        """, (task['title'], task['description'], task['status_id'], task['user_id']))
    conn.commit()


def main():
    conn = create_connection()
    create_users(conn)
    create_status(conn)
    create_tasks(conn)
    conn.close()


if __name__ == "__main__":
    main()
