import mysql.connector as mysql
from utility import execute_query

def insertViewer(conn, uid, email, 
                  nickname, street,city,
                  state,zip_code,genres,
                  joined_date,first,last,subscription):
    try:
        inserting_viewer = f"""
        INSERT INTO Viewers (uid, subscription, first_name, last_name)
        VALUES ('{uid}', '{subscription}', '{first}', '{last}');
        """
        execute_query(conn, inserting_viewer)

        inserting_user = f"""
        INSERT INTO Users (uid, email, joined_date, nickname, street, city, state, zip, genres)
        VALUES ('{uid}', '{email}', '{joined_date}', '{nickname}', '{street}', '{city}', '{state}', '{zip_code}', '{genres}');
        """
        execute_query(conn, inserting_user)
        return True
    except mysql.Error as err:
        print("Fail: ", err)
    finally:
        conn.close()


def addGenre(conn, uid, genre):
    try:
        cursor = conn.cursor()
        select_genre = "SELECT genres FROM users WHERE uid = %s;"
        cursor.execute(select_genre, (uid,))
        result = cursor.fetchone()

        if result:
            current_genres = result[0]
            result_list= result[0].lower().split(';')
            if genre.lower() in result_list:
                return True
            else:
                append_genre = current_genres + ';' + genre if current_genres else genre 
                update_genre = "UPDATE Users SET genres = %s WHERE uid = %s;"
                cursor.execute(update_genre, (append_genre, uid))
                conn.commit()
                return True
        cursor.close()
    except mysql.Error as err:
        print("Fail: ", err)
    finally:
        conn.close()


def deleteViewer(conn, uid):
    try:
        deleViewerQuerry = f"DELETE FROM Viewers WHERE uid = {uid}"
        execute_query(conn, deleViewerQuerry)

        deleteUserQuerry = f"DELETE FROM Users WHERE uid = {uid}"
        execute_query(conn, deleteUserQuerry)

        print("Deleted")
        return True
    except mysql.Error as err:
        print("Fail: ", err)
