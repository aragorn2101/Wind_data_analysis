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
#  Data from IOSnet:
#  https://galilee.univ-reunion.fr/thredds/catalog/dataTextfiles/catalog.html
#
#
#  Vocabulary [CF Standard Name Table v67]:
#      diffuse_horizontal_irradiance (W m-2) = surface_diffuse_downwelling_shortwave_flux_in_air = DHI (DHI_qo01_Avg)
#      dew_point_temperature (degree Celsius) = dew_point_temperature = DP (DP_nf01_Avg)
#      global_horizontal_irradiance (W m-2) = surface_downwelling_shortwave_flux_in_air = GHI (GHI_qo01_Avg)
#      air_pressure (hPA) = air_pressure = Patm (PA_nf01_Avg)
#      relative_humidity (%RH) = relative_humidity = RH (RH_nf01_Avg)
#      rainfall (mm) = thickness_of_rainfall_amount = Rain (RR_nf01_Avg)
#      air_temperature (degree Celsius) = air_temperature = Temp (TA_nf01_Avg)
#      datalogger_intern_temperature (degree Celsius) = T_2XX_Avg (TI_dw01_Avg)
#      solar_panel_back_surface_temperature (degree Celsius) = T_4XX_Avg (TSP_va01_Avg)
#      minimum_datalogger_voltage (degree Celsius) = = U (UD_dw01_Min)
#      UV_irradiance_on_A_and_B_band (W m-2) = solar_irradiance = UV_0XX_Avg (UVAB_qk01_Avg)
#      wind_direction (degree) = wind_from_direction = WD (WD_nf01_Avg)
#      standard_deviation_of_wind_direction (degree) = WD_StdDev (WD_nf01_Std)
#      wind_speed_max_of_gust (m s-1) = wind_speed_of_gust = WSmax (WSG_nf01_Max)
#      wind_speed (m s-1) = wind_speed = WS (WS_nf01_Avg)
#      thermocouple_box_temperature (degree Celsius) = T_1XX_Avg ()
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
# 0 : Vacoas
# 1 : MRT, Bras d'Eau
# 2 : Réserve Tortues, Rodrigues
# 3 : UoM FoA rooftop, Réduit
#
#
stationIdx = 1

#
#  NOTE:
#  First 2 strings describes weather station and location, 3rd string is the
#  path to the data. 4th and 5th strings are keywords for the CSV data. 6th
#  item is the bin size (in m/s) to use for the histogram.  Finally, the last
#  string in each sublist is the mask to apply to each data series due to gaps
#  in the collection.
#
IOSnet_stations = [[
                    "Vacoas",
                    "Mauritius Meteorological Station, Vacoas",
                    "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_IOSnet/Vacoas",
                    "WD_nf01_Avg",
                    "WS_nf01_Avg",
                    0.50,
                    "(wind_df['timestamp'] < '2022-02-17 00:00:00') | ((wind_df['timestamp'] > '2022-03-09 23:59:00') & (wind_df['timestamp'] < '2022-05-29 00:00:00')) | (wind_df['timestamp'] > '2022-12-06 23:59:00')"
                   ],
                   [
                     "MRT",
                     "Bras d'Eau",
                     "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_IOSnet/Bras_dEau",
                     "WD_mk01_Avg",
                     "WS_mk01_Avg",
                     0.20,
                     "(wind_df['timestamp'] < '2020-03-19 00:00:00') | ((wind_df['timestamp'] > '2020-05-18 23:59:00') & (wind_df['timestamp'] < '2022-01-14 00:00:00')) | (wind_df['timestamp'] > '2022-05-17 23:59:00')"
                   ],
                   [
                     "Reserves Tortues",
                     "Reserves Tortues, Rodrigues",
                     "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_IOSnet/Rodrigues",
                     "WD_mo01_Avg",
                     "WS_mo01_Avg",
                     0.50,
                     "(wind_df['timestamp'] < '2022-09-03 00:00:00') | (wind_df['timestamp'] > '2022-11-30 23:59:00')"
                   ],
                   [
                     "Réduit",
                     "UoM FoA rooftop, Réduit",
                     "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_IOSnet/Reduit",
                     "WD_mp01_Avg",
                     "WS_mp01_Avg",
                     0.50,
                     "(wind_df['timestamp'] > '2022-12-05 23:59:00')"
                   ]]



# Check if given path for weather station data is indeed a directory
if not path.isdir(IOSnet_stations[stationIdx][2]):
    print("{:s} is not a directory!".format(IOSnet_stations[stationIdx][2]))
    exit(1)



###  BEGIN Open files and load relevant data into arrays  ###

##  Weather station data
filelist = sorted( listdir(IOSnet_stations[stationIdx][2]) )

print("\nSuccessfully accessed directory")
print(IOSnet_stations[stationIdx][2])
print("\nContent of directory:")
print(filelist)

print()

for i in range(len(filelist)):
    print("Opening CSV file {:s} ...".format(IOSnet_stations[stationIdx][2] + "/" + filelist[i]))

    tmp_df = pd.read_csv(IOSnet_stations[stationIdx][2] + "/" + filelist[i], header=0)


    # Create new data frame with timestamp and wind data only,
    # and drop NaN values.
    #
    # WD_xxxx_Avg: average wind direction (degrees)
    # WS_xxxx_Avg: wind speed
    #
    if (i == 0):
        wind_df = tmp_df[['timestamp', IOSnet_stations[stationIdx][3], IOSnet_stations[stationIdx][4]]].dropna(axis=0, how='any')

    else:
        # Concatenate into main dataframe, wind_df
        wind_df = pd.concat([wind_df,
                             tmp_df[['timestamp', IOSnet_stations[stationIdx][3], IOSnet_stations[stationIdx][4]]].dropna(axis=0, how='any')],
                             axis=0)

###  END Open files and load relevant data into arrays  ###



print("Converting time stamps to datetime objects ...")
wind_df['timestamp'] = pd.to_datetime( wind_df['timestamp'], format="%Y-%m-%dT%H:%M:%SZ" )

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
mask = eval( IOSnet_stations[stationIdx][6] )
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
avg_ws = new_df[[ IOSnet_stations[stationIdx][4] ]].to_numpy().T[0]

bin_size = IOSnet_stations[stationIdx][5]  # m/s
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
