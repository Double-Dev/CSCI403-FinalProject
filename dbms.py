import pg8000
import requests as rq
import math
from datetime import date
from datetime import datetime

connection = None
cursor = None

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

def select(table):
    global cursor
    # Cannot parameterize column or table names!
    # cursor.execute("SELECT * FROM %s LIMIT 3;", (table,))
    cursor.execute("SELECT * FROM "+table+" LIMIT 3;")
    # cursor.execute("SELECT * FROM crimes_in_toronto LIMIT 3;")
    results = cursor.fetchall()
    return 0, results

def crimesInArea(address, horiKm, vertKm):
    key = '&api_key=68001ed089ffb524504774xwb615f13'
    url = 'https://geocode.maps.co/search?q='
    query = url+address+key
    res = rq.get(query)
    if (res.status_code == 401) or len(res.json()) < 1:
        return 1, {}
    lat = float(res.json()[0]['lat'])
    long = float(res.json()[0]['lon'])
    latDist = horiKm / 110.574
    cursor.execute("""
        SELECT lat_wgs84, long_wgs84 FROM toronto_crimes WHERE 
            (lat_wgs84 >= %s AND lat_wgs84 <= %s) AND
            (long_wgs84 >= %s AND long_wgs84 <= %s);
        """, (lat-latDist, lat+latDist, long-vertKm/(111.32*math.cos(lat-latDist)), long+vertKm/(111.32*math.cos(lat+latDist))))
    return 0, cursor.fetchall()

def insert(ucr, offense, mciCategory, occuranceDate, occuranceHour, address, hoodCode, hoodName, premiseType, locationType):
    global cursor
    # Checking if occurance date is in DB and adding it if it's not:
    # cursor.execute("SELECT * FROM occurance_date WHERE report_full_date = %s;", (occuranceDate))
    # if cursor.fetchall().count() == 0:
    cursor.execute("INSERT INTO occurance_date VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (occurance_full_date) DO NOTHING;;",
                    (occuranceDate,
                    occuranceDate.year,
                    occuranceDate.month,
                    occuranceDate.day,
                    occuranceDate.timetuple().tm_yday,
                    occuranceDate.weekday()))
    
    # Checking if report date is in DB and adding it if it's not:
    reportDate = date.today()
    # cursor.execute("SELECT * FROM occurance_date WHERE report_full_date = %s;", (reportDate))
    # if cursor.fetchall().count() == 0:
    cursor.execute("INSERT INTO report_date VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (report_full_date) DO NOTHING;",
            (reportDate,
            reportDate.year,
            reportDate.month,
            reportDate.day,
            reportDate.timetuple().tm_yday,
            reportDate.weekday()))
    
    # Checking if location type is in DB and adding it if it's not:
    cursor.execute("INSERT INTO location_type VALUES (%s, %s) ON CONFLICT (premis_type) DO NOTHING;",
            (premiseType, locationType))
    
    # Checking if location is in DB and adding it if it's not:
    key = '&api_key=68001ed089ffb524504774xwb615f13'
    url = 'https://geocode.maps.co/search?q='
    query = url+address+key
    res = rq.get(query)
    if (res.status_code == 401) or len(res.json()) < 1:
        return 1, {}
    lat = float(res.json()[0]['lat'])
    long = float(res.json()[0]['lon'])
    cursor.execute("INSERT INTO report_date VALUES (%s, %s, %s, %s, %s) ON CONFLICT (long_wgs84, lat_wgs84) DO NOTHING;",
        (long, lat, premiseType, hoodCode, hoodName))

    # Checking if crime_info is in DB and adding it if it's not:
    cursor.execute("INSERT INTO crime_info VALUES (%s, %s, %s) ON CONFLICT (ucr) DO NOTHING;",
        (ucr, offense, mciCategory))
    
    # Inserting crime into main crime table:
    cursor.execute("INSERT INTO toronto_crimes VALUES (%s, %s, %s, %s, %s, NULL, %s, %s);",
        (ucr, reportDate, occuranceDate, long, lat, datetime.now().hour, occuranceHour))


def destroy():
    global connection
    global cursor
    # Commit changes to DB
    if connection != None:
        connection.commit()
        cursor.close()
        connection.close()