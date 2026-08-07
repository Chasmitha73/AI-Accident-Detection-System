import sqlite3
def delete_record(record_id):
    connection= sqlite3.connect("accidents.db")
    cursor=connection.cursor()
    cursor.execute("DELETE FROM accidents WHERE id=?",(record_id,))
    connection.commit()
    if cursor.rowcount>0:
        print("record deleted successfully")
    else:
        print("NO record found.")
    connection.close()