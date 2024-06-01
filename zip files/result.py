from flask import Flask, render_template
import pymysql.cursors  # Assuming you're using MySQL as the database

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'airline',
    'cursorclass': pymysql.cursors.DictCursor,
}

# Route to render the HTML template with data from the database
@app.route('/')
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

if __name__ == '__main__':
    app.run(debug=True)
