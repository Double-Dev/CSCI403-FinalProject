import matplotlib.pyplot as plt
import pandas as pd

# Matplotlib is not meant to be called on any thread other than the main one and can
# give numerous errors/warnings if that requirement is not satisfied. For this reason,
# we decided to construct our usage of it such that the button callbacks don't directly
# call matplotlib functions.

# Variables to store data for update.
shouldUpdate = False
updateLat = 0
updateLong = 0
updateLats = []
updateLongs = []
updateCrimes = []

# Update plot if update is needed.
def updatePlot():
    global shouldUpdate
    if not shouldUpdate:
        return False
    crime_types = ['Assault','Auto Theft','Break and Enter','Robbery','Theft Over']
    crime_colors = [(237/255, 5/255, 195/255),(45/255, 119/255, 230/255),'Yellow',(127/255,240/255,70/255),(159/255, 123/255, 176/255)]
    figure, ax = plt.subplots()

    dff = pd.DataFrame({'Longs':updateLongs,'Lats':updateLats,'Crimes':updateCrimes})

    for idx, ct in enumerate(crime_types):  
        dfff = dff[(dff['Crimes'] == ct)]
        ax.scatter(dfff['Longs'],dfff['Lats'],color=crime_colors[idx],s=1,marker='o',label=ct)

    ax.scatter([updateLong],[updateLat],s=100,c='r',marker='*')
    ax.legend(markerscale=6)
    ax.set_facecolor((250/255,1,1))
    plt.savefig("output_map.jpg")
    shouldUpdate = False
    return True

# Store data and wait for update signal from main thread.
def make_map(lat, long, lats, longs, crimes):
    global updateLat, updateLong, updateLats, updateLongs, updateCrimes, shouldUpdate
    updateLat = lat
    updateLong = long
    updateLats = lats
    updateLongs = longs
    updateCrimes = crimes
    shouldUpdate = True
