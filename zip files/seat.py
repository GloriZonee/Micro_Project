# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Replace these values with your database configuration
db_host = 'localhost'
db_user = 'root'
db_password = '1234'
db_name = 'airline'

connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
if connection:
    print("Connected to the database")
else:
    print("Failed to connect to the database")

# Connect to the database
cursor = connection.cursor()

# Function to get all flight IDs from the flight table
def get_flight_ids():
    cursor.execute("SELECT flight_id FROM flight")
    return [row[0] for row in cursor.fetchall()]

# Function to insert seat information into the seat table
def insert_seat_data(flight_id, seat):
    cursor.execute("INSERT INTO seats (flight_id, seat) VALUES (%s, %s)", (flight_id, seat))
    connection.commit()

# Function to check if the seat is already booked
def is_seat_booked(flight_id, seat):
    cursor.execute("SELECT COUNT(*) FROM seats WHERE flight_id = %s AND seat = %s", (flight_id, seat))
    result = cursor.fetchone()
    return result[0] > 0

@app.route('/seat_selection')
def seat_selection():
    flight_ids = get_flight_ids()
    seat_ids = [f"s{i}" for i in range(1, 11)]  # Assuming seat IDs are "s1" to "s10"
    session['seat_ids'] = seat_ids  # Store seat IDs in session for later use
    return render_template('seat.html', flight_ids=flight_ids, seat_ids=seat_ids)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        flight_id = request.form['flightId']
        selected_seats = request.form.getlist('selectedSeats')

        # Book the selected seats
        for seat in selected_seats:
            if not is_seat_booked(flight_id, seat):
                insert_seat_data(flight_id, seat)

        # Redirect to the confirmation page
        return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
