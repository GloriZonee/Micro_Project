from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Configure MySQL
db = pymysql.connect(host='localhost',
                     user='root',
                     password='1234',
                     database='airline')

def execute_query(query, values=None):
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()

@app.route('/')
def cancel_tickets():
    return render_template('cancel.html')

@app.route('/cancel_seat', methods=['POST'])
def cancel_seat():
    # Assuming you have a form with a hidden input field named 'seat_id'
    seat_id = request.form.get('seat_id')
    
    # Remove the seat from the seats table
    query = "DELETE FROM seats WHERE seat = %s"
    execute_query(query, (seat_id,))
    
    return render_template('cancel.html', seat_canceled=True)

if __name__ == '__main__':
    app.run(debug=True)
