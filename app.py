import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from alert import send_alert

app = Flask(__name__)

# Use a consistent path for the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "accidents.db")


# Connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Create the accidents table if it doesn't exist
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS accidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            vehicle_number TEXT,
            date_time TEXT,
            status TEXT,
            latitude TEXT,
            longitude TEXT
        )
    """)

    conn.commit()
    conn.close()


# Initialize the database
create_table()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Search accident records
@app.route("/search", methods=["GET", "POST"])
def search():
    accidents = []

    if request.method == "POST":
        vehicle_number = request.form.get("vehicle_number", "").strip()

        conn = get_db_connection()

        try:
            accidents = conn.execute(
                """
                SELECT * FROM accidents
                WHERE vehicle_number = ?
                """,
                (vehicle_number,)
            ).fetchall()
        finally:
            conn.close()

    return render_template("search.html", accidents=accidents)


# View all accident records
@app.route("/view_database")
def view_database():
    conn = get_db_connection()

    try:
        accidents = conn.execute(
            "SELECT * FROM accidents ORDER BY id DESC"
        ).fetchall()
    finally:
        conn.close()

    return render_template(
        "view_database.html",
        accidents=accidents
    )


# Enter accident information
@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "POST":

        location = request.form.get("location", "").strip()
        vehicle_number = request.form.get("vehicle_number", "").strip()
        status = request.form.get("status", "").strip()
        latitude = request.form.get("latitude", "").strip()
        longitude = request.form.get("longitude", "").strip()

        # Validate required form fields
        if not all([
            location,
            vehicle_number,
            status,
            latitude,
            longitude
        ]):
            return "Please fill in all accident details.", 400

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()

        try:
            conn.execute(
                """
                INSERT INTO accidents
                (location, vehicle_number, date_time, status,
                 latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    location,
                    vehicle_number,
                    date_time,
                    status,
                    latitude,
                    longitude
                )
            )

            conn.commit()

        finally:
            conn.close()

        # Send the alert after saving the record
        try:
            send_alert(
                location,
                latitude,
                longitude,
                vehicle_number,
                status
            )
        except Exception:
            app.logger.exception("Failed to send accident alert")

        return render_template("success.html")

    return render_template("detect.html")


# Delete an accident record
@app.route("/delete/<int:record_id>", methods=["POST"])
def delete(record_id):
    conn = get_db_connection()

    try:
        cursor = conn.execute(
            "DELETE FROM accidents WHERE id = ?",
            (record_id,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return "Accident record not found.", 404

    finally:
        conn.close()

    return redirect(url_for("view_database"))


if __name__ == "__main__":
    app.run(debug=False)