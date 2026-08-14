import sqlite3

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM stats")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()