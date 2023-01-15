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
                "./Sample_data/Weather_Underground/Quatres_Bornes_IPLAINEW2",
               ],
               ["IPLAIN36",
                "Bout du Monde, Ebene",
                "./Sample_data/Weather_Underground/Ebene_IPLAIN36",
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



###  BEGIN Refining data  ###

# Resample
new_df = wind_df.resample(timedelta(days=2), axis=0, on='Date').mean()
new_df.reset_index(inplace=True)


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



###  BEGIN Plot  ###

print("\n\n")
print("------------------------------------------------------------")
print("Plotting wind speed data for period:")
print("{:s}  ->  {:s}".format(new_df['Date'].min().strftime("%d.%m.%Y"), new_df['Date'].max().strftime("%d.%m.%Y")))
print("for WU weather station at {:s} ({:s})".format(WU_stations[stationIdx][1], WU_stations[stationIdx][0]))
print("------------------------------------------------------------")
print("\n\n")


# Set size of figure for laptop screen (1600 x 900 pixels)
plt.rcParams["figure.figsize"] = [12.00,7.85]

# ------------------------------------------------------------------
fig, ax = plt.subplots(2,1)

fig.autofmt_xdate()
x_axis_format = mdates.DateFormatter('%b')


##  2021  ##
ax[0].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[0].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[0].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[0].set_ylabel("u (m/s)")
ax[0].grid(True, which='minor', axis='x')
ax[0].grid(True, which='major', axis='y')

mask = (new_df['Date'] >= '2021-01-01') & (new_df['Date'] <= '2021-12-31')
ax[0].set_xlim(date(year=2021, month=1, day=1), date(year=2021, month=12, day=31))
ax[0].set_ylim(0.0, 1.1*new_df['Avg'].loc[mask].max())
ax[0].plot(new_df['Date'].loc[mask], new_df['Avg'].loc[mask], linewidth=2.0, marker='o', color='green')

##  2022  ##
ax[1].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[1].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[1].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[1].set_ylabel("u (m/s)")
ax[1].grid(True, which='minor', axis='x')
ax[1].grid(True, which='major', axis='y')

mask = (new_df['Date'] >= '2022-01-01') & (new_df['Date'] <= '2022-12-31')
ax[1].set_xlim(date(year=2022, month=1, day=1), date(year=2022, month=12, day=31))
ax[1].set_ylim(0.0, 1.1*new_df['Avg'].loc[mask].max())
ax[1].plot(new_df['Date'].loc[mask], new_df['Avg'].loc[mask], linewidth=2.0, marker='o', color='darkorchid')


fig.tight_layout()
# ------------------------------------------------------------------


plt.show()

###  END Plot  ###


print()
exit(0)
