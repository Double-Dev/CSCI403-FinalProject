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
    try:
        connection = pg8000.connect(
            user=username,
            password=password,
            host="ada.mines.edu",
            port=5432,
            database="csci403"
        )
        cursor = connection.cursor()
        cursor.execute("SET search_path TO group8;")
        return 0
    except Exception as e:
        return 1

def select(table):
    global cursor
    # Cannot parameterize column or table names!
    # cursor.execute("SELECT * FROM %s LIMIT 3;", (table,))
    cursor.execute("SELECT * FROM "+table+" LIMIT 3;")
    # cursor.execute("SELECT * FROM crimes_in_toronto LIMIT 3;")
    results = cursor.fetchall()
    return 0, results

def addressToLatLong(address):
    key = '&api_key=68001ed089ffb524504774xwb615f13'
    url = 'https://geocode.maps.co/search?q='
    query = url+address+key
    res = rq.get(query)
    if (res.status_code == 401) or len(res.json()) < 1:
        return None, None
    lat = float(res.json()[0]['lat'])
    long = float(res.json()[0]['lon'])
    return lat, long

def crimesInArea(lat, long, horiKm, vertKm):
    try:
        latDist = horiKm / 110.574
        longDist = vertKm/(111.32*math.cos(lat-latDist))
        cursor.execute("""
            SELECT lat_wgs84, long_wgs84, mci_category FROM toronto_crimes
                JOIN crime_info ON toronto_crimes.ucr = crime_info.ucr
                WHERE (lat_wgs84 >= %s AND lat_wgs84 <= %s) AND
                (long_wgs84 >= %s AND long_wgs84 <= %s);
            """, (lat-latDist, lat+latDist, long-longDist, long+longDist))
        return 0, cursor.fetchall()
    except:
        return 1, {}

def insert(ucr, offense, mciCategory, occuranceDate, occuranceHour, address, hoodCode, hoodName, premiseType, locationType, division):
    global cursor
    try:
        # Checking if occurance date is in DB and adding it if it's not:
        # cursor.execute("SELECT * FROM occurance_date WHERE report_full_date = %s;", (occuranceDate))
        # if cursor.fetchall().count() == 0:
        cursor.execute("""
                    INSERT INTO occurance_date (occurance_full_date, occ_year, occ_month, occ_day, occ_doy, occ_dow)
                    VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (occurance_full_date) DO NOTHING;
                    """,
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
        cursor.execute("""
                    INSERT INTO report_date (report_full_date, report_year, report_month, report_day, report_doy, report_dow)
                    VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (report_full_date) DO NOTHING;
                    """,
                (reportDate,
                reportDate.year,
                reportDate.month,
                reportDate.day,
                reportDate.timetuple().tm_yday,
                reportDate.weekday()))
        
        # Checking if location type is in DB and adding it if it's not:
        cursor.execute("INSERT INTO location_type (premis_type, location_type) VALUES (%s, %s) ON CONFLICT (premis_type) DO NOTHING;",
                (premiseType, locationType))
        
        # Checking if location is in DB and adding it if it's not:
        lat, long = addressToLatLong(address)
        cursor.execute("""
                    INSERT INTO location (long_wgs84, lat_wgs84, premis_type, hood_158, neighborhood_158)
                    VALUES (%s, %s, %s, %s, %s) ON CONFLICT (long_wgs84, lat_wgs84) DO NOTHING;
                    """,
            (long, lat, premiseType, hoodCode, hoodName))

        # Checking if crime_info is in DB and adding it if it's not:
        cursor.execute("""
                    INSERT INTO crime_info (ucr, offense, mci_category)
                    VALUES (%s, %s, %s) ON CONFLICT (ucr) DO NOTHING;
                    """,
            (ucr, offense, mciCategory))
        
        # Inserting crime into main crime table:
        cursor.execute(
            """
            INSERT INTO toronto_crimes
            (event_unique_id, report_date, occ_date, report_hour, occ_hour, division, ucr, long_wgs84, lat_wgs84)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            ("Testing", reportDate, occuranceDate, datetime.now().hour, occuranceHour, division, ucr, long, lat))
        
        return 0
    except Exception as e:
        return 1

def searchForDelete(dateVal):
    try:
        cursor.execute("""
        SELECT COUNT(*) FROM toronto_crimes WHERE occ_date BETWEEN %s AND %s;
        """, (dateVal, dateVal))
        return 0, cursor.fetchall()
    except:
        return 1, {}

def delete(dateVal):
    try:
        cursor.execute("""
        DELETE FROM toronto_crimes WHERE occ_date BETWEEN %s AND %s;
        """, (dateVal, dateVal))
        return 0
    except:
        return 1

def destroy():
    global connection
    global cursor
    # Commit changes to DB
    if connection != None:
        connection.commit()
        cursor.close()
        connection.close()
