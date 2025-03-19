import mysql.connector as mysql

def popularRelease(conn, N):
    """Task 9: Get Most Popular Releases"""
    if N is None:
        return []
    cursor = conn.cursor()
    cursor.execute(
        "SELECT r.rid, r.title, COUNT(rv.rid) AS reviewCount "
        "FROM Releases r "
        "LEFT JOIN Reviews rv ON r.rid = rv.rid "
        "GROUP BY r.rid, r.title "
        "ORDER BY reviewCount DESC, r.rid DESC "
        "LIMIT %s;",
        (N,)
    )
    results = cursor.fetchall()
    return results
    cursor.close()


def releaseTitle(conn, sid):
    """Task 10: Get Release Title"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT r.rid, r.title AS release_title, r.genre, v.title AS video_title, "
        "v.ep_num, v.length "
        "FROM Sessions s "
        "JOIN Videos v ON s.rid = v.rid AND s.ep_num = v.ep_num "
        "JOIN `Releases` r ON v.rid = r.rid "
        "WHERE s.sid = %s "
        "ORDER BY r.title ASC;",
        (sid,)
    )
    results = cursor.fetchall()
    for row in results:
        print(",".join(map(str, row)))
    cursor.close()


def activeViewer(conn, N, start_date, end_date):
    """Task 11: Get Active Viewers"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT v.uid, v.first_name, v.last_name "
        "FROM Viewers v "
        "JOIN Sessions s ON v.uid = s.uid "
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


def videosViewed(conn, rid):
    """Task 12: Get Videos Viewed"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT v.rid, v.ep_num, v.title, v.length, COUNT(DISTINCT s.uid) AS viewer_count "
        "FROM Videos v "
        "LEFT JOIN Sessions s ON v.rid = s.rid AND v.ep_num = s.ep_num "
        "WHERE v.rid = %s "
        "GROUP BY v.rid, v.ep_num, v.title, v.length "
        "ORDER BY v.rid DESC;",
        (rid,)
    )
    results = cursor.fetchall()
    for row in results:
        print(",".join(map(str, row)))
    cursor.close()
