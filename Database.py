import sqlite3

conn = sqlite3.connect("cricket.db")
cur = conn.cursor()

# Stats table
cur.execute("""
CREATE TABLE IF NOT EXISTS stats(
player TEXT,
matches INTEGER,
runs INTEGER,
hundreds INTEGER,
fifties INTEGER,
value REAL,
ctg TEXT
)
""")

# Match table
cur.execute("""
CREATE TABLE IF NOT EXISTS match(
player TEXT,
scored INTEGER,
faced INTEGER,
fours INTEGER,
sixes INTEGER,
bowled INTEGER,
maidens INTEGER,
givenruns INTEGER,
wickets INTEGER,
catches INTEGER,
stumping INTEGER,
runout INTEGER
)
""")

# Teams table
cur.execute("""
CREATE TABLE IF NOT EXISTS teams(
name TEXT,
players TEXT,
value REAL,
points INTEGER
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")