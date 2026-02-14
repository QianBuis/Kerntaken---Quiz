import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="quiz_app"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()

    print("Database verbinding werkt! Resultaat:", result)

except mysql.connector.Error as err:
    print("Database fout:", err)
