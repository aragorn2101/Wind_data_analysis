#!/usr/bin/env python3
#
#  Copyright (c) 2022 Nitish Ragoomundun, Mauritius
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.
#
#
#	Column	Description
#	date	Date
#	tavg	Avg. Temperature
#	tmin	Min. Temperature
#	tmax	Max. Temperature
#	prcp	Total Precipitation
#	snow	Snow Depth
#	wdir	Wind Direction
#	wspd	Wind Speed
#	wpgt	Peak Gust
#	pres	Air Pressure
#	tsun	Sunshine Duration
#
#


from sys import argv
from os import path,listdir
import numpy as np
from scipy.special import gamma
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
rcParams['font.size'] = 16.0


###  Path for UoM Farm data files  ###
DataPath = "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_Meteostat/20180101_-_20221231.csv"

# Check if given path for weather station data is indeed a directory
if not path.isfile(DataPath):
    print("Cannot access {:s}!".format(DataPath))
    exit(1)


###  BEGIN Open files and load relevant data into arrays  ###

print("Opening CSV file {:s} ...".format(DataPath))

tmp_df = pd.read_csv(DataPath, parse_dates=['date'])

# Filter only date and wind data, and eliminate nulls
wind_df = tmp_df[['date', 'wdir', 'wspd']].dropna(axis=0, how='any')

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



###  BEGIN Refining data  ###

# Set up mask excluding gaps in the data and apply mask
mask = (wind_df['date'] > '2018-02-01 23:59:00')
new_df = wind_df.loc[ mask ]

print()
print("------------------------------------------------------------")
print("type(new_df):")
print(type(new_df))
print("------------------------------------------------------------")
print("new_df.info():")
print(new_df.info())
print("------------------------------------------------------------")
print(new_df.iloc[:20])
print(". . .")
print(new_df.iloc[-20:])
print("------------------------------------------------------------")

###  END Refining data  ###



###  BEGIN Make histogram and probability distribution  ###

# Convert wind speed series to numpy array
avg_ws = new_df[['wspd']].to_numpy().T[0]

bin_size = 1.0  # m/s
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
