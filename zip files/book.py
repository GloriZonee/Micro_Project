from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'airline'

mysql = MySQL(app)

@app.route('/')
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

if __name__ == '__main__':
    app.run(debug=True)
