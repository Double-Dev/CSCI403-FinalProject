import pg8000
import requests as rq
from getpass import getpass

connection = None

def create(username: str, password: str):
    global connection
    global cursor
    # Connect to DB
    connection = pg8000.connect(
        user=username,
        password=password,
        host="ada.mines.edu",
        port=5432,
        database="csci403"
    )
    cursor = connection.cursor()
    cursor.execute("SET search_path TO group8;")

def select(user_data):
    global cursor
    print(cursor.execute("SELECT * FROM toronto_crimes LIMIT 1;"))
    # address = user_data.address
    # distance = user_data.distance
    # date = user_data.date
    # key = '&api_key=68001ed089ffb524504774xwb615f13'
    # url = 'https://geocode.maps.co/search?q='
    # lat_buff = distance/69
    # long_buff = distance/42.4
    # query = url+address+key
    # res = rq.get(query)
    # while (res.status_code == 401) or len(res.json()) < 1:
    #     print("Invalid address. Try again.")
    #     query = url+address+key
    #     res = rq.get(query)
    # lat = float(res.json()[0]['lat'])
    # long = float(res.json()[0]['lon'])
    # cursor.execute("SELECT * FROM toronto_crimes WHERE %s;", user_data)

def insert():
    print("Not implemented yet.")

def destroy():
    global connection
    global cursor
    # Commit changes to DB
    if connection != None:
        connection.commit()
        cursor.close()
        connection.close()