import logging
import psycopg2
import azure.functions as func
import os


def execute_query_from_file(conn, file_path, *args):
    """Execute SQL query from a file"""
    with open(file_path, 'r') as file:
        query = file.read()

    with conn.cursor() as cursor:
        cursor.execute(query, args)


def create_database(conn, database_name):
    """Create a new database"""
    try:
        conn = psycopg2.connect(conn)
        conn.autocommit = True
        cursor = conn.cursor()

        create_database_query = f"CREATE DATABASE {database_name};"
        cursor.execute(create_database_query)

        cursor.close()
        conn.close()

        logging.info(f"Database '{database_name}' created successfully.")
    except psycopg2.Error as e:
        logging.error(f"Error creating database: {e}")


def create_students_table(conn):
    """Create the 'students' table in the database"""
    try:
        conn = psycopg2.connect(conn)
        conn.autocommit = True

        # Load create_table.sql from file

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER,
                grade FLOAT
            )
        '''

        with conn.cursor() as cursor:
            cursor.execute(create_table_query)
            cursor.close()
        logging.info("Table 'students' created successfully.")
    except psycopg2.Error as e:
        logging.error(f"Error creating table: {e}")


def insert_students_data(conn, data):
    """Insert student data into the 'students' table"""

    try:
        conn = psycopg2.connect(conn)
        conn.autocommit = True

        insert_data_query = '''
            INSERT INTO students (name, age, grade)
            VALUES (%s, %s, %s);
        '''
        name = "karthik"
        age = 23
        grade = 9.5
        with conn.cursor() as cursor:
            cursor.execute(insert_data_query, (name, age, grade))
        logging.info("Data inserted successfully.")
    except psycopg2.Error as e:
        logging.error(f"Error inserting data: {e}")
    finally:
        conn.close()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    database_name = req.params.get('database_name')
    password = os.getenv('PGPASSWORD')
    host_name = os.getenv('PGHOST')
    user_name = os.getenv('PGUSER')
    db = "postgres"

    conn = f"host={host_name} port=5432 dbname={db} user={user_name} password={password} sslmode=require"
    create_database(conn, database_name)
    conn_new = f"host={host_name} port=5432 dbname={database_name} user={user_name} password={password} sslmode=require"
    create_students_table(conn_new)

    students_data = [
        ("John Smith", 18, 85.5),
    ]

    insert_students_data(conn_new, students_data)
