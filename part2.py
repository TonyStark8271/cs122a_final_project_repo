import mysql.connector as mysql
from utility import execute_query, connect_db
#(5)Insert a new movie in the appropriate table(s)
def insertMovie(conn, rid, website_url):
    try:
        execute_query(conn, "ALTER TABLE Movies ADD CONSTRAINT u_rid UNIQUE (rid);")
        if rid == None:
            return False
        website_url if website_url else None
        execute_query(conn, f"""
        INSERT INTO Movies(rid, website_url) VALUES ('{rid}', '{website_url}');
        """)
        print("Success")
        return True
    except mysql.Error as err:
        print("Fail: ", err)
        return False
    finally:
        conn.close()
#(6)Insert a new session that was played by a specific viewer which streamed a specific video.
def insertSession(conn, sid, uid, rid, ep_num, initiate_at,leave_at, quality, device):
    try:
        execute_query(conn, "ALTER TABLE Sessions ADD CONSTRAINT u_sid UNIQUE (sid);")
        if sid == None:
            return False
        ep_num if ep_num else None
        initiate_at if initiate_at else None
        leave_at if leave_at else None
        quality if quality else None
        device if device else None
        execute_query(conn, 
        f"""
        INSERT INTO Sessions(sid, uid, rid, ep_num, initiate_at, leave_at, quality, device)
        VALUES ('{sid}', '{uid}', '{rid}', '{ep_num}', '{initiate_at}', '{leave_at}', '{quality}', '{device}');
        """)
        print("Success")
        return True        
    except mysql.Error as err:
        print("Fail: ", err)
        return False
    finally:
        conn.close()
#(7)Update the title of a release
def updateRelease(conn, rid, title):
    try:
        cursor = conn.cursor()
        select_release = "SELECT 1 FROM Releases WHERE rid = %s;"
        cursor.execute(select_release, (rid,))
        result = cursor.fetchone()
        if result:
            execute_query(conn, f"UPDATE Releases SET title = '{title}' WHERE rid = '{rid}';")
            print("Success")
            return True
        else:
            print("Fail")
            return False
    except mysql.Error as err:
        print("Fail: ", err)
        return False
    finally:
        conn.close()
#(8)Given a viewer ID, list all the unique releases the viewer has reviewed in ASCENDING order on the release title
def listReleases(uid):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        if uid is None:
            return []
        cursor.execute("SELECT DISTINCT r.rid, r.genre, r.title\n" +
                        "FROM Releases r, Reviews rvs\n" + 
                        f"WHERE r.rid  = rvs.rid AND rvs.uid = '{uid}'\n" +
                        "ORDER BY r.title ASC;")
        rows = cursor.fetchall()
        for row in rows:
            print(",".join(map(str, row)))
    except mysql.Error as err:
        print("Fail: ", err)
        return []
    finally:
        conn.close()
