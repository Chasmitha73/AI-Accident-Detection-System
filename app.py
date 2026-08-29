from flask import Flask, render_template, request,redirect
import sqlite3
from alert import send_alert

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    accidents = []

    if request.method == "POST":
        vehicle_number = request.form["vehicle_number"]

        conn = sqlite3.connect("accidents.db")
        conn.row_factory = sqlite3.Row

        accidents = conn.execute(
            "SELECT * FROM accidents WHERE vehicle_number = ?",
            (vehicle_number,)
        ).fetchall()

        conn.close()

    return render_template("search.html", accidents=accidents)
@app.route("/view_database")
def view_database():
    conn = sqlite3.connect("accidents.db")
    conn.row_factory = sqlite3.Row

    accidents = conn.execute(
        "SELECT * FROM accidents"
    ).fetchall()

    conn.close()

    return render_template(
        "view_database.html",
        accidents=accidents
    )

@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "POST":
        location = request.form["location"]
        vehicle_number = request.form["vehicle_number"]
        status = request.form["status"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        from datetime import datetime
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("accidents.db")

        conn.execute("""
            INSERT INTO accidents
            (location, vehicle_number, date_time, status, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            location,
            vehicle_number,
            date_time,
            status,
            latitude,
            longitude
        ))

        conn.commit()
        conn.close()

        send_alert(location, latitude, longitude, vehicle_number, status)

        return render_template("success.html")

    return render_template("detect.html")
@app.route("/delete/<int:record_id>", methods=["POST"])
def delete(record_id):
    conn = sqlite3.connect("accidents.db")

    conn.execute(
        "DELETE FROM accidents WHERE id = ?",
        (record_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/view_database")
if __name__ == "__main__":
    app.run(debug=True)