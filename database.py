import sqlite3

def create_table():
    connection = sqlite3.connect("accidents.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accidents
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        vehicle_number TEXT,
        date_time TEXT,
        status TEXT,
        latitude TEXT,
        longitude TEXT
    )
    """)

    connection.commit()
    connection.close()


def save_accident_details(location, vehicle_number, current_time, status, latitude, longitude):
    try:
        connection = sqlite3.connect("accidents.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO accidents
        (location, vehicle_number, date_time, status, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (location, vehicle_number, current_time, status, latitude, longitude))

        connection.commit()
        connection.close()

        print("database saved successfully")

    except Exception as e:
        print("database error:", e)


create_table()