#!/usr/bin/env python3
#
#
#  Data from Weather Underground.
#  https://www.wunderground.com
#
#  CSV columns:
#
#  Date        Wind speed
#             Max  Avg  Min
#
#  NOTE: wind speeds are in mi/h
#
#
#  Power curve for mini-FARWIND csv file:
#     speed,power
#      m/s    W
#
#


from os import path,listdir
import numpy as np
from scipy.special import gamma
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
rcParams['font.size'] = 16.0


###  Weather station index to calculate for  ###
#
# 0 : Quatres Bornes
# 1 : Bout du Monde, Ebene
#
#
stationIdx = 0


WU_stations = [["IPLANEW2",
                "Quatres Bornes",
                "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_WU/Quatres-Bornes_IPLANEW2",
                0.5
               ],
               ["IPLAIN36",
                "Bout du Monde, Ebene",
                "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_WU/Bout_du_Monde_IPLAIN36",
                0.5
               ]]



# Check if given path for weather station data is indeed a directory
if not path.isdir(WU_stations[stationIdx][2]):
    print("{:s} is not a directory!".format(WU_stations[stationIdx][2]))
    exit(1)



###  BEGIN Open files and load relevant data into arrays  ###

##  Weather station data
filelist = sorted( listdir(WU_stations[stationIdx][2]) )

print("\nSuccessfully accessed directory")
print(WU_stations[stationIdx][2])
print("\nContent of directory:")
print(filelist)

print()

for i in range(len(filelist)):
    print("Opening CSV file {:s} ...".format(WU_stations[stationIdx][2] + "/" + filelist[i]))

    tmp_df = pd.read_csv(WU_stations[stationIdx][2] + "/" + filelist[i], parse_dates=['Date'])

    if (i == 0):
        wind_df = tmp_df[['Date', 'Avg']].dropna(axis=0, how='any')

    else:
        # Concatenate into main dataframe, wind_df
        wind_df = pd.concat([wind_df,
                             tmp_df[['Date', 'Avg']].dropna(axis=0, how='any')],
                            axis=0)

###  END Open files and load relevant data into arrays  ###



print()
print("------------------------------------------------------------")
print("type(wind_df):")
print(type(wind_df))
print("------------------------------------------------------------")
print("wind_df.info():")
print(wind_df.info())
print("------------------------------------------------------------")
print(wind_df.iloc[:20])
print(". . .")
print(wind_df.iloc[-20:])
print("------------------------------------------------------------")



###  BEGIN Make histogram and probability distribution  ###

# Convert wind speed series to numpy array
avg_ws = wind_df[['Avg']].to_numpy().T[0]

bin_size = WU_stations[stationIdx][3]  # m/s
ceil_ws = np.ceil(avg_ws.max())
hist_w8ts, hist_edges = np.histogram( avg_ws, bins=int(ceil_ws / bin_size), range=(0.0, ceil_ws) )

# Probability density, mean and standard deviation
ws_P = (hist_w8ts / hist_w8ts.sum()) / bin_size
cumul_P = (ws_P * bin_size).cumsum()
ws_mean = avg_ws.mean()
ws_stddev = np.std(avg_ws)
ws_midpts = np.zeros( hist_w8ts.shape )

for i in range(len(ws_midpts)):
    ws_midpts[i] = 0.5 * (hist_edges[i] + hist_edges[i+1])

print("\nHistogram weights:")
print(hist_w8ts)
print("len(Histogram weights) = {:d}".format(len(hist_w8ts)))
print("\nHistogram edges:")
print(hist_edges)
print("len(Histogram edges) = {:d}".format(len(hist_edges)))
print("\nHistogram midpoints:")
print(ws_midpts)
print("len(Histogram midpoints) = {:d}".format(len(ws_midpts)))
print("\nProbability density:")
print(ws_P)
print("len(ws_P) = {:d}".format(len(ws_P)))
print("\nCumulative probability:")
print(cumul_P)
print("len(cumul_P) = {:d}".format(len(cumul_P)))
print()

print("\nHistrogram data:")
for i in range(len(hist_w8ts)):
    print("{:7.4f}\t-\t{:7d}\t-\t{:7.4f}\t{:7.4f}".format(ws_midpts[i], hist_w8ts[i], ws_P[i], cumul_P[i]))

print()

###  END Make histogram and probability distribution  ###



###  BEGIN Plot  ###

# Set size of figure for laptop screen (1600 x 900 pixels)
plt.rcParams["figure.figsize"] = [12.00,7.85]

fig, ax = plt.subplots(1,1)

# maximum y ordinate
ceil_y = 1.1 * hist_w8ts.max()

ax.set_xlim(0.0, ceil_ws)
ax.set_ylim(0.0, ceil_y)
ax.set_xlabel("Wind speed (m/s)")
ax.set_ylabel("Weight")
ax.bar(hist_edges[:-1], hist_w8ts, align='edge', width=bin_size, color='whitesmoke', edgecolor='black', linewidth=1.5)
fig.tight_layout()

plt.show()

###  END Plot  ###


print()
exit(0)
