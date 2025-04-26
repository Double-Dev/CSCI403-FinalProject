import requests as rq
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('major-crime-indicators.csv')

key = '&api_key=68001ed089ffb524504774xwb615f13'
url = 'https://geocode.maps.co/search?q='
address = "27 Breen Crescent, Toronto, Canada" #input the address in question
distance = 3 #input radius to observe, in miles
lat_buff = distance/69
long_buff = distance/42.4

while True:
    address = input("Enter your Toronto address: ")+", Toronto, Canada"
    query = url+address+key
    res = rq.get(query)

    while (res.status_code == 401) or len(res.json()) < 1:
    
        print("Invalid address. Try again.")
        address = input("Enter your Toronto address: ")
        query = url+address+key
        res = rq.get(query)

    distance = input("Show crimes within how many miles? (Suggested 3): ")
    

    lat = float(res.json()[0]['lat'])
    long = float(res.json()[0]['lon'])

    dff = df[((lat-lat_buff<df['LAT_WGS84']) & (lat+lat_buff>df['LAT_WGS84'])) & ((long-long_buff<df['LONG_WGS84']) & (long+long_buff>df['LONG_WGS84']))]

    colors, unique = pd.factorize(dff['MCI_CATEGORY'])
    figure, ax = plt.subplots()
    ax.scatter(dff['LONG_WGS84'],dff['LAT_WGS84'],c=colors,s=1)
    ax.scatter([long],[lat],s=50,c='r')
    plt.show()