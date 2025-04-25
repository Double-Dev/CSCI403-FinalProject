import matplotlib.pyplot as plt
import pandas as pd


def make_map(lat, long, lats, longs, crimes):
    crime_types = ['Assault','Auto Theft','Break and Enter','Robbery','Theft Over']
    crime_colors = [(186/255, 129/255, 30/255),(58/255, 126/255, 166/255),'Yellow',(127/255,240/255,70/255),(159/255, 123/255, 176/255)]
    figure, ax = plt.subplots()

    dff = pd.DataFrame({'Longs':longs,'Lats':lats,'Crimes':crimes})

    for idx, ct in enumerate(crime_types):  
        dfff = dff[(dff['Crimes'] == ct)]
        ax.scatter(dfff['Longs'],dfff['Lats'],color=crime_colors[idx],s=1,marker='o',label=ct)

    ax.scatter([long],[lat],s=100,c='r',marker='*')
    ax.legend(markerscale=6)
    ax.set_facecolor((250/255,1,1))
    plt.savefig("output_map.jpg")
    return "output_map.jpg"