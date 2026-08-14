import sqlite3

conn = sqlite3.connect("cricket.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(stats)")

for column in cur.fetchall():
    print(column)

conn.close()