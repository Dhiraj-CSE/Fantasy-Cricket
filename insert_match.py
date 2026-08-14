import sqlite3

conn = sqlite3.connect("cricket.db")
cur = conn.cursor()

cur.execute("DELETE FROM match")

matches = [

("Kohli",82,60,8,2,0,0,0,0,1,0,0),
("Rohit",65,48,6,3,0,0,0,0,1,0,0),
("Gill",45,38,5,1,0,0,0,0,0,0,0),
("Rahul",55,42,4,2,0,0,0,0,1,0,0),
("Surya",72,40,7,5,0,0,0,0,0,0,0),

("Dhoni",28,20,2,1,0,0,0,0,2,1,0),
("Pant",60,41,6,2,0,0,0,0,1,0,0),
("Samson",48,35,4,3,0,0,0,0,1,0,0),

("Jadeja",35,30,2,1,8,1,40,3,2,0,1),
("Hardik",50,32,3,3,6,0,35,2,1,0,0),
("Axar",22,18,1,0,10,0,28,2,0,0,0),

("Ashwin",12,10,1,0,10,1,32,4,0,0,0),
("Bumrah",5,7,0,0,10,2,25,3,1,0,0),
("Shami",7,8,0,0,10,0,30,3,0,0,0),
("Kuldeep",8,6,0,0,10,1,27,4,0,0,0)

]

cur.executemany(
    "INSERT INTO match VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
    matches
)

conn.commit()
conn.close()

print("Match data inserted successfully")