
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
app = Flask(__name__, template_folder='templates', static_folder='static')
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Database initialization
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='airline'
)

cursor = db_connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        name VARCHAR(100) NOT NULL,
        dob DATE NOT NULL,
        gender VARCHAR(10),
        age INT,
        phone_no VARCHAR(15),
        password VARCHAR(255) NOT NULL
    )
''')
db_connection.commit()
db_connection.close()

@app.route('/')
def main_page():
    return render_template('mainpage.html') # flag = 0 <-initialize
                                            #this should run in an if condition  when seats are full, flag = 1;

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        dob = request.form['birth-date']
        gender = request.form['gender']
        age = request.form['age']
        phone_number = request.form['phone-number']
        password = request.form['password']

        # Database insertion
        db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='airline'
        )

        cursor = db_connection.cursor()
        try:
            print(f"SQL Query: INSERT INTO users (email, name, dob, gender, age, phone_no, password) VALUES ({email}, {name}, {dob}, {gender}, {age}, {phone_number}, {password})")
            cursor.execute('''
                INSERT INTO users (email, name, dob, gender, age, phone_no, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (email, name, dob, gender, age, phone_number, password))
        
# ... (similar print statements for other form fields)

            db_connection.commit()
        except Exception as e:
            print(f"Error during insertion: {e}")
            db_connection.rollback()
        finally:
            db_connection.close()


        return redirect(url_for('signin'))

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email and password match in the database
        db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='airline'
        )

        cursor = db_connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
        user = cursor.fetchone()
        db_connection.close()

        if user and bcrypt.check_password_hash(user[6], password):  # Assuming password is at index 6
            # Redirect to a welcome or dashboard page
            return "Welcome, " + user[2]  # Assuming user[2] is the 'name' field
        else:
            return "Invalid login credentials"

@app.route('/signup')
def sign_up():
    return render_template('signup1.html')

@app.route('/signin')
def sign_in():
    return render_template('signin.html')



@app.route('/index')
def index():
    return render_template('book.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        from_city = request.form['from']
        to_city = request.form['to']
        departure_date = request.form['departure']
        arrival_date = request.form['arrival']

        # Perform database insertion
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO flight_reserve (departure_loc, arrival_loc, departure_date, arrival_date) VALUES (%s, %s, %s, %s)",
            (from_city, to_city, departure_date, arrival_date)
        )
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('searchresult'))

@app.route('/searchresult')
def searchresult():
    return render_template('flightresult.html')


# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'airline',
    'cursorclass': pymysql.cursors.DictCursor,
}

# Route to render the HTML template with data from the database
@app.route('/flight_results')
def flight_results():
    # Connect to the database
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Perform the SQL query to get data from the database
            sql = "SELECT * FROM flight_reserve;"
            cursor.execute(sql)

            # Fetch all the results
            flights = cursor.fetchall()

    finally:
        # Close the database connection
        connection.close()

    # Render the HTML template with the data
    return render_template('flightresult.html', flights=flights)

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

db = pymysql.connect(host='localhost',
                     user='root',
                     password='1234',
                     database='airline')

def execute_query(query, values=None):
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()

@app.route('/cancel_tickets')
def cancel_tickets():
    return render_template('confirmation.html')

@app.route('/cancel_seat', methods=['POST'])
def cancel_seat():
    # Assuming you have a form with a hidden input field named 'seat_id'
    seat_id = request.form.get('seat_id')
    
    # Remove the seat from the seats table
    query = "DELETE FROM seats WHERE seat = %s"
    execute_query(query, (seat_id,))
    
    return render_template('cancel', seat_canceled=True)

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run(debug=True)
