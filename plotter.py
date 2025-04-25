import matplotlib.pyplot as plt
import pandas as pd


def make_map(lat, long, lats, longs, crimes):
    figure, ax = plt.subplots()
    colors, unique = pd.factorize(pd.Series(crimes))
    ax.scatter(longs,lats,c=colors,s=1)
    ax.scatter([long],[lat],s=50,c='r')
    plt.savefig("output_map.jpg")
    return "output_map.jpg"