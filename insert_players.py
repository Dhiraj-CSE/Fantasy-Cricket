import sqlite3

conn = sqlite3.connect("cricket.db")
cur = conn.cursor()

# Remove old players
cur.execute("DELETE FROM stats")

players = [

# BATSMEN
("Kohli", 102, 5788, 8, 23, 120, "BAT"),
("Rohit", 80, 3455, 10, 21, 100, "BAT"),
("Gill", 55, 2200, 6, 10, 95, "BAT"),
("Rahul", 70, 2900, 4, 18, 90, "BAT"),
("Surya", 60, 2500, 5, 15, 95, "BAT"),

# WICKET KEEPERS
("Dhoni", 75, 2573, 3, 19, 75, "WK"),
("Pant", 65, 2400, 5, 14, 95, "WK"),
("Samson", 50, 1800, 4, 12, 85, "WK"),

# ALL ROUNDERS
("Jadeja", 85, 1914, 0, 10, 85, "AR"),
("Hardik", 78, 2100, 2, 13, 100, "AR"),
("Axar", 60, 950, 0, 5, 80, "AR"),

# BOWLERS
("Ashwin", 110, 750, 0, 2, 110, "BWL"),
("Bumrah", 90, 250, 0, 0, 120, "BWL"),
("Shami", 88, 320, 0, 1, 100, "BWL"),
("Kuldeep", 72, 180, 0, 0, 90, "BWL")

]

cur.executemany(
    "INSERT INTO stats VALUES(?,?,?,?,?,?,?)",
    players
)

conn.commit()
conn.close()

print("Players Added Successfully")