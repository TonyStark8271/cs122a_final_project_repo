import mysql.connector

try:
    conn = mysql.connector.connect(
        user="root",
        password="",  # Change to correct password if needed
        host="127.0.0.1",  # Explicitly set host
        port=3306,         # Default MySQL port
        database="zotstreaming",
        allow_local_infile=True
    )
    print("Connection successful!")
    conn.close()
except mysql.connector.Error as err:
    print("Failed to connect:", err)