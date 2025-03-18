import sys
import mysql.connector as mysql

DB_CONFIG = {
    "user": "root",
    "password": "Sixersinseven09",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "zotstreaming",
}

def connect_db():
    """Function to establish connection to MySQL database"""
    try:
        conn = mysql.connect(**DB_CONFIG)
        return conn
    except mysql.Error as err:
        print("Failed to connect to the MySQL database:", err)
        sys.exit(1)

# Task 9: Get Most Popular Releases
def popularRelease(conn, N):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT r.rid, r.title, COUNT(rv.rid) AS reviewCount "
        "FROM `Release` r "
        "LEFT JOIN Review rv ON r.rid = rv.rid "
        "GROUP BY r.rid, r.title "
        "ORDER BY reviewCount DESC, r.rid DESC "
        "LIMIT %s;",
        (N,)
    )
    results = cursor.fetchall()
    for row in results:
        print(",".join(map(str, row)))
    cursor.close()

# Task 10: Get Release Title
def releaseTitle(conn, sid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT r.rid, r.title AS release_title, r.genre, v.title AS video_title, "
        "v.ep_num, v.length "
        "FROM Session s "
        "JOIN Video v ON s.rid = v.rid AND s.ep_num = v.ep_num "
        "JOIN `Release` r ON v.rid = r.rid "
        "WHERE s.sid = %s "
        "ORDER BY r.title ASC;",
        (sid,)
    )
    results = cursor.fetchall()
    for row in results:
        print(",".join(map(str, row)))
    cursor.close()

# Task 11: Get Active Viewers
def activeViewer(conn, N, start_date, end_date):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT v.uid, v.first_name, v.last_name "
        "FROM Viewer v "
        "JOIN Session s ON v.uid = s.uid "
        "WHERE s.initiate_at BETWEEN %s AND %s "
        "GROUP BY v.uid, v.first_name, v.last_name "
        "HAVING COUNT(s.sid) >= %s "
        "ORDER BY v.uid ASC;",
        (start_date, end_date, int(N))
    )
    results = cursor.fetchall()
    if results:
        for row in results:
            print(",".join(map(str, row)))
    else:
        print("No results found.")
    cursor.close()

# Task 12: Get Videos Viewed
def videosViewed(conn, rid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT v.rid, v.ep_num, v.title, v.length, COUNT(DISTINCT s.uid) AS viewer_count "
        "FROM Video v "
        "LEFT JOIN Session s ON v.rid = s.rid AND v.ep_num = s.ep_num "
        "WHERE v.rid = %s "
        "GROUP BY v.rid, v.ep_num, v.title, v.length "
        "ORDER BY v.rid DESC;",
        (rid,)
    )
    results = cursor.fetchall()
    for row in results:
        print(",".join(map(str, row)))
    cursor.close()

# Main Execution
if __name__ == "__main__":
    conn = connect_db()
    command = sys.argv[1]

    if command == "popularRelease":  # Task 9
        N = int(sys.argv[2])
        popularRelease(conn, N)

    elif command == "releaseTitle":  # Task 10
        sid = int(sys.argv[2])
        releaseTitle(conn, sid)

    elif command == "activeViewer":  # Task 11
        N = int(sys.argv[2])
        start_date = sys.argv[3]
        end_date = sys.argv[4]
        activeViewer(conn, N, start_date, end_date)

    elif command == "videosViewed":  # Task 12
        rid = int(sys.argv[2])
        videosViewed(conn, rid)

    conn.close()
