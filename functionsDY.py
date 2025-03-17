import mysql.connector as mysql
from utility import execute_query

def insertViewer(conn, uid, email, 
                  nickname, street,city,
                  state,zip_code,genres,
                  joined_date,first,last,subscription):
    try:
        inserting_viewer = f"""
        INSERT INTO Viewer (uid, subscription, first_name, last_name)
        VALUES ('{uid}', '{subscription}', '{first}', '{last}');
        """
        execute_query(conn, inserting_viewer)

        inserting_user = f"""
        INSERT INTO User (uid, email, joined_date, nickname, street, city, state, zip, genres)
        VALUES ('{uid}', '{email}', '{joined_date}', '{nickname}', '{street}', '{city}', '{state}', '{zip_code}', '{genres}');
        """
        execute_query(conn, inserting_user)
    except mysql.Error as err:
        print("Fail: ", err)
    finally:
        conn.close()
    