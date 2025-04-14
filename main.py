import pg8000
from getpass import getpass

print("Welcome to Toronto Crime Statistics")
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

table = input("Select a table to query: ")
cursor.execute("SELECT * FROM %s;", table)

# Commit changes to DB
connection.commit()
cursor.close()
connection.close()