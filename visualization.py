import pg8000
from getpass import getpass
import folium
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import io
import base64

username = input("Please enter username: ")

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

# Example usage
if __name__ == "__main__":
    results = generate_premises_graphics("Commercial")
    print(f"Generated {results['map_file']}")