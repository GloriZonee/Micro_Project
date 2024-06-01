from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
app = Flask(__name__, template_folder='templates', static_folder='static')

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
def index():
    return render_template('signup1.html')

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

        if user:
            # Redirect to a welcome or dashboard page
            return "Welcome, " + user[2]  # Assuming user[2] is the 'name' field
        else:
            return "Invalid login credentials"

if __name__ == '__main__':
    app.run(debug=True)