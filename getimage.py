import pandas as pd
import matplotlib.pyplot as plt
import sys

df = pd.read_csv('major-crime-indicators.csv')

lat = float(sys.argv[1])
long = float(sys.argv[2])
distance = float(sys.argv[3])
lat_buff = distance/69
long_buff = distance/42.4

dff = df[((lat-lat_buff<df['LAT_WGS84']) & (lat+lat_buff>df['LAT_WGS84'])) & ((long-long_buff<df['LONG_WGS84']) & (long+long_buff>df['LONG_WGS84']))]

colors, unique = pd.factorize(dff['MCI_CATEGORY'])
figure, ax = plt.subplots()
ax.scatter(dff['LONG_WGS84'],dff['LAT_WGS84'],c=colors,s=1)
ax.scatter([long],[lat],s=50,c='r')
plt.savefig("output_map.jpg")