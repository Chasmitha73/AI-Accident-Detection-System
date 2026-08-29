import sqlite3

connection = sqlite3.connect("accidents.db")
cursor = connection.cursor()

columns = [row[1] for row in cursor.execute("PRAGMA table_info(accidents)")]

if "status" not in columns:
    cursor.execute("ALTER TABLE accidents ADD COLUMN status TEXT")

if "latitude" not in columns:
    cursor.execute("ALTER TABLE accidents ADD COLUMN latitude TEXT")

if "longitude" not in columns:
    cursor.execute("ALTER TABLE accidents ADD COLUMN longitude TEXT")

connection.commit()
connection.close()

print("Database updated successfully!")