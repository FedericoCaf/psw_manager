import sqlite3

try:
    connection = sqlite3.connect('psw_manager_db.db')
    with open('create_users.sql') as f:
        connection.executescript(f.read())
        connection.commit()
finally:
    connection.close()