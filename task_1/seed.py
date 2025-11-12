import psycopg2
from psycopg2 import DatabaseError
from faker import Faker
import random

connect_params = {
    "dbname": "task_management",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

NUMBER_OF_USERS = 10
NUMBER_OF_TASKS = 30

fake = Faker()


def seed_data(conn):
    cur = conn.cursor()
    try:
        users = []
        for _ in range(NUMBER_OF_USERS):
            users.append((fake.name(), fake.email()))

        insert_users_query = "INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id"
        cur.executemany(insert_users_query, users)
        user_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cur.fetchall()]

        if not status_ids:
            print("Error: 'status' table is empty. Run 'create_tables.py' first")
            return

        tasks = []
        for _ in range(NUMBER_OF_TASKS):
            tasks.append((
                fake.sentence(nb_words=6),
                fake.text() if random.choice([True, False]) else None,
                random.choice(status_ids),
                random.choice(user_ids)
            ))

        insert_tasks_query = """
                             INSERT INTO tasks (title, description, status_id, user_id)
                             VALUES (%s, %s, %s, %s) \
                             """
        cur.executemany(insert_tasks_query, tasks)

        conn.commit()
        print(f"Successfully seeded {NUMBER_OF_USERS} users and {NUMBER_OF_TASKS} tasks")

    except (Exception, DatabaseError) as error:
        print(f"Error while seeding database: {error}")
        conn.rollback()
    finally:
        cur.close()


def main():
    conn = None
    try:
        conn = psycopg2.connect(**connect_params)
        seed_data(conn)
    except psycopg2.OperationalError as e:
        print(f"Unable to connect to DB: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed")


if __name__ == "__main__":
    main()