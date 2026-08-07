import sqlite3
connection=sqlite3.connect("accidents.db")
cursor=connection.cursor()
cursor.execute("SELECT*FROM accidents")
rows=cursor.fetchall()
for row in rows:
    print(row)
connection.close()