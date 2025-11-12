import psycopg2
from psycopg2 import DatabaseError


connect_params = {
    "dbname": "task_management",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

sql_ddl = """
          DROP TABLE IF EXISTS tasks;
          DROP TABLE IF EXISTS users;
          DROP TABLE IF EXISTS status;

          CREATE TABLE status \
          ( \
              id   SERIAL PRIMARY KEY, \
              name VARCHAR(50) UNIQUE NOT NULL
          );

          CREATE TABLE users \
          ( \
              id       SERIAL PRIMARY KEY, \
              fullname VARCHAR(100)        NOT NULL, \
              email    VARCHAR(100) UNIQUE NOT NULL
          );

          CREATE TABLE tasks \
          ( \
              id          SERIAL PRIMARY KEY, \
              title       VARCHAR(100) NOT NULL, \
              description TEXT, \
              status_id   INTEGER      NOT NULL, \

              FOREIGN KEY (status_id) \
                  REFERENCES status (id) \
                  ON DELETE RESTRICT,

              FOREIGN KEY (user_id) \
                  REFERENCES users (id) \
                  ON DELETE CASCADE
          );

          INSERT INTO status (name) \
          VALUES ('new'), \
                 ('in progress'), \
                 ('completed'); \
          """


def create_tables(conn):
    """ Function to create tables in the database """
    cur = conn.cursor()
    try:
        cur.execute(sql_ddl)
        conn.commit()
        print("Tables 'users', 'status', and 'tasks' created successfully")
        print("Statuses ('new', 'in progress', 'completed') added")
    except (Exception, DatabaseError) as error:
        print(f"Error while creating tables: {error}")
        conn.rollback()
    finally:
        cur.close()


def main():
    conn = None
    try:
        conn = psycopg2.connect(**connect_params)
        create_tables(conn)
    except psycopg2.OperationalError as e:
        print(f"Unable to connect: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()
            print("Connection closed")


if __name__ == "__main__":
    main()