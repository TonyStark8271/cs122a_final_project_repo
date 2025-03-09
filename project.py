import sys
import os
import mysql.connector as mysql
import csv
import re

""" Connecting to database : 
    -- I appreciate the work on ed, but the code has no comment...<T_T>
    -- So, I decide we are going to use the lame version connector.

    This part is mainly the connector part:
    -- DB_CONFIG is the connection details
    #  DO NOT TOUCH ANYTHING IN IT UNTIL YOU REALLY SURE ABOUT WHAT YOUR ARE DOING #
    #  IF U REALLY SURE ABOUT SOMTHING: SAVE THE CHANGES BEFORE YOU PUSH #
    #  REMEMBER TO CHANGE THIS PART AFTER ALL CODE DONE FOR SUBMISSION #

    :)

    __ For submission:
        user: 'test',
        password: 'password',
        database: 'cs122a'
"""
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

def execute_query(conn, query, params=None):
    """Executes a given SQL query and commit the changes"""
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        cursor.close()
    except mysql.Error as err:
        print("Failed to execute query")
        sys.exit(1)

def drop_all_tables():
    """Delete all exsting table, and close the cursor"""
    conn = connect_db()

    try:
        cursor = conn.cursor()

        #Disable FOREIGN key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # Get all table names
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE();")
        tables = cursor.fetchall()

        # Drop all the existing tables, sanitise the database
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
        
        # Re-Enable FOREIGN key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print("Previous data deleted, database cleaned up")
    except mysql.Error as err:
        print("Failed: ", err)
    finally:
        cursor.close()
        conn.close()

def detect_data_type(line):
    """determains which type the data should be"""
    if line.isdigit():
        return "INT"
    try:
        float(line)
        return "FLOAT"
    except:
        pass

    if re.match(r"^\d{4}-\d{2}-\d{2}$", line):
        return "DATE"
    elif re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", line):
        return "DATETIME"
    else:
        return "VARCHAR(1000)"

def read_columns(file):
    """Read from the data file to get the column names"""
    with open(file, newline = '') as f:
        reader = csv.reader(f)
        headers = next(reader)

        line_for_check = next(reader)
        data_types = []
        for line in line_for_check:
            data_types.append(detect_data_type(line))

    return headers, data_types

def import_data(path):
    drop_all_tables()
    conn = connect_db()

    try:
        cursor = conn.cursor()
        for file in os.listdir(path):
            if file.endswith(".csv"):
                file_path = os.path.join(path, file)
                table = file.replace(".csv", "") # Get table name

                print(f"creating {table}")
                headers, data_types = read_columns(file_path)

                create_table_query = f"CREATE TABLE `{table}` ({', '.join(f'`{col}` {type}'for col, type in zip(headers, data_types))});"
                cursor.execute(create_table_query)
                print(f"Table '{table}' created")

                import_data_query = f"LOAD DATA LOCAL INFILE '{file_path}' INTO TABLE `{table}` FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;"
                cursor.execute(import_data_query)
                print(f"Table '{table}' imported data from '{file_path}'")
    except mysql.Error as err:
        print("Failed: ", err)
    finally:
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    path = sys.argv[2]
    import_data(path)