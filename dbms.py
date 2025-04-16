import pg8000
from getpass import getpass

def create():
    global connection
    global cursor
    username = input("Please enter username: ")
    # Connect to DB
    connection = pg8000.connect(
        user=username,
        password=getpass(),
        host="ada.mines.edu",
        port=5432,
        database="csci403"
    )
    cursor = connection.cursor()

def select(table):
    global cursor
    cursor.execute("SELECT * FROM %s;", table)

def insert():
    print("Not implemented yet.")

def destroy():
    global connection
    global cursor
    # Commit changes to DB
    connection.commit()
    cursor.close()
    connection.close()