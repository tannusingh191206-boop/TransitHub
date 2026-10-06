from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

app = Flask(__name__)


# -----------------------------
# MySQL Database Connection
# -----------------------------
def get_db_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        use_pure=True
    )

    return connection


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/")
def dashboard():

    connection = get_db_connection()
    cursor = connection.cursor()

    # Count trains
    cursor.execute("SELECT COUNT(*) FROM trains")
    train_count = cursor.fetchone()[0]

    # Count buses
    cursor.execute("SELECT COUNT(*) FROM buses")
    bus_count = cursor.fetchone()[0]

    # Count today's bookings
    cursor.execute("""
        SELECT COUNT(*)
        FROM bookings
        WHERE DATE(booking_date) = CURDATE()
    """)
    booking_count = cursor.fetchone()[0]

    # Calculate today's successful revenue
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        WHERE payment_status = 'SUCCESS'
        AND DATE(payment_date) = CURDATE()
    """)
    revenue = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        train_count=train_count,
        bus_count=bus_count,
        booking_count=booking_count,
        revenue=revenue
    )


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)