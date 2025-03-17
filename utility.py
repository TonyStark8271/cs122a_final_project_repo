import mysql.connector as mysql
import sys

DB_CONFIG = {
    "user": "root",
    "password": "",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "zotstreaming",
    "allow_local_infile": True
}


def connect_db():
    """Funciton for establish connection to the MySQL database"""
    try:
        conn = mysql.connect(**DB_CONFIG)
        print("connected")
        return conn
    except mysql.Error as err:
        print("Failed to connect to the MySql database")
        sys.exit(1)


def execute_query(conn, query):
    """Executes a given SQL query and commit the changes
        basically a helper function
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except mysql.Error as err:
        print("Failed to execute query", err)
        sys.exit(1)
    finally:
        cursor.close()