import sqlite3
def search_vehicle(vehicle_number):
    connection=sqlite3.connect("accidents.db")
    cursor=connection.cursor()
    cursor.execute("SELECT*FROM accidents WHERE vehicle_number=?",(vehicle_number,))
    record=cursor.fetchone()
    if record:
        print("\nAccident Records Found:")
        print(record)
    else:
        print("\nNo accident records found.")
    connection.close()