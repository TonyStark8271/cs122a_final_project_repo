import sys
import os
import mysql.connector as mysql
import csv
import re

from utility import connect_db
from datetime import datetime

from part1 import insertViewer, addGenre, deleteViewer
from part2 import insertMovie, insertSession, updateRelease, listReleases
from part3 import popularRelease, releaseTitle, activeViewer, videosViewed 
date_format = "%Y-%m-%d"


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


                file_path = file_path.replace("\\", "/")
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
    if (sys.argv[1] == "import"):
        path = sys.argv[2]
        import_data(path)

    # you can pass in the global_connect into the function as a parameter
    # just remeber to close the cursor you created or use execute_query 
    # for safety
    global_connect = connect_db()
    if (sys.argv[1] == "insertViewer"):
        insertViewer(global_connect,
                     int(sys.argv[2]), # uid
                     sys.argv[3], # email
                     sys.argv[4], # nickname
                     sys.argv[5], # street
                     sys.argv[6], # city
                     sys.argv[7], # state
                     int(sys.argv[8]), # zip_code
                     sys.argv[9], # genres
                     datetime.strptime(sys.argv[10], date_format).date(), # joined_date
                     sys.argv[11], # first
                     sys.argv[12], # last
                     sys.argv[13], #subscription
                     )
    elif (sys.argv[1] == "addGenre"):
        addGenre(global_connect, sys.argv[2], sys.argv[3])
    elif (sys.argv[1] == "deleteViewer"):
        deleteViewer(global_connect, sys.argv[2])
    elif (sys.argv[1] == "insertMovie"):
        insertMovie(global_connect,
        int(sys.argv[2]),#sid
        sys.argv[3])#website_url
    elif (sys.argv[1] == "insertSession"):
        insertSession(global_connect,
        int(sys.argv[2]),#sid,
        int(sys.argv[3]),#uid
        int(sys.argv[4]),#rid
        sys.argv[5],#ep_num
        datetime.strptime(sys.argv[6], "%Y-%m-%d %H:%M:%S" ).date(),#initiate_at
        datetime.strptime(sys.argv[7], "%Y-%m-%d %H:%M:%S" ).date(),#leave_at
        sys.argv[8],#quality
        sys.argv[9]#device
        )
    elif (sys.argv[1] == "updateRelease"):
        updateRelease(global_connect,
        int(sys.argv[2]),#rid
        sys.argv[3]#title
        )
    elif (sys.argv[1] == "listReleases"):
        listReleases(
        int(sys.argv[2])#uid
        )
    elif sys.argv[1] == "popularRelease":  # Task 9
        N = int(sys.argv[2])
        popularRelease(global_connect, N)
    elif sys.argv[1] == "releaseTitle":  # Task 10
        sid = int(sys.argv[2])
        releaseTitle(global_connect, sid)
    elif sys.argv[1] == "activeViewer":  # Task 11
        N = int(sys.argv[2])
        start_date = sys.argv[3]
        end_date = sys.argv[4]
        activeViewer(global_connect, N, start_date, end_date)
    elif sys.argv[1] == "videosViewed":  # Task 12
        rid = int(sys.argv[2])
        videosViewed(global_connect, rid)


    if (global_connect.is_connected()):
        global_connect.commit()
        global_connect.close()
