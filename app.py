from flask import Flask, render_template
import sqlite3

app = Flask(name)

def get_db_connection():
    connection = sqlite3.connect('sensor_data.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def index():
    try:
        # Retrieve messages from the database
        with get_db_connection() as db_connection:
            db_cursor = db_connection.cursor()
            db_cursor.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC')
            messages = db_cursor.fetchall()
        return render_template('index.html', messages=messages)
    except Exception as e:
        return str(e)

if name == 'main':
    app.run(debug=True)