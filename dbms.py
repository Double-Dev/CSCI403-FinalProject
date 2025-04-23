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

#visualization function
#parameter is type from premises_type column
def generate_premises_graphics(premises_type):
    #Connect to PostgreSQL
    conn = pg8000.connect(
        user=username,
        password=getpass(),
        host="ada.mines.edu",
        port=5432,
        database="csci403"
    )
    cursor = conn.cursor()

    #Query for geographic data
    cursor.execute("""
        SELECT latitude, longitude, offence 
        FROM crimes 
        WHERE premises_type = %s 
        AND latitude IS NOT NULL 
        AND longitude IS NOT NULL
    """, (premises_type,))
    geo_data = cursor.fetchall()

    #Query for temporal analysis (crimes by hour)
    cursor.execute("""
        SELECT EXTRACT(HOUR FROM occ_date) as hour, COUNT(*) 
        FROM crimes 
        WHERE premises_type = %s
        GROUP BY hour 
        ORDER BY hour
    """, (premises_type,))
    hourly_data = cursor.fetchall()
    hours, counts = zip(*hourly_data) if hourly_data else ([], [])

    conn.close()

    #Generate Folium Map
    if geo_data:
        #Center map on mean coordinates
        lats = [float(row[0]) for row in geo_data]
        lngs = [float(row[1]) for row in geo_data]
        m = folium.Map(location=[sum(lats)/len(lats), sum(lngs)/len(lngs)], zoom_start=12)

        #Add markers
        for lat, lng, offence in geo_data:
            folium.CircleMarker(
                location=[lat, lng],
                radius=3,
                color='red',
                fill=True,
                popup=offence
            ).add_to(m)
        
        map_file = f"{premises_type}_map.html"
        m.save(map_file)
    else:
        map_file = None

    #Generate Matplotlib Bar Chart
    if hours:
        plt.figure(figsize=(10, 4))
        plt.bar(hours, counts, color='#4e79a7')
        plt.title(f"Crimes at {premises_type} by Hour of Day")
        plt.xlabel("Hour of Day (0-23)")
        plt.ylabel("Number of Crimes")
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        
        #Save to bytes for embedding (optional)
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', bbox_inches='tight')
        img_bytes.seek(0)
        chart_url = base64.b64encode(img_bytes.read()).decode('utf-8')
        plt.close()
    else:
        chart_url = None

    return {
        "map_file": map_file, #Path to HTML map
        "chart_image": chart_url, #Base64-encoded chart for web
        "premises_type": premises_type,
        "total_crimes": sum(counts) if counts else 0
    }