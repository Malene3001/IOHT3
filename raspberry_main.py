import socket
import sqlite3
import time

#Set up UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 12345)
udp_socket.bind(server_address)

#Set up SQLite database
db_connection = sqlite3.connect('sensor_data.db')
db_cursor = db_connection.cursor()

#Drop the existing table if it exists
db_cursor.execute('DROP TABLE IF EXISTS sensor_data')

#Recreate the table with the new column name
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        message TEXT
    )
''')
db_connection.commit()

while True:
    data, addr = udp_socket.recvfrom(1024)
    message = data.decode()

    # Store the entire message in the SQLite database
    db_cursor.execute('INSERT INTO sensor_data (message) VALUES (?)', (message,))
    db_connection.commit()

    # Additional logic based on your application requirements
    print(f"Received from {addr}: {message}")

    time.sleep(1)