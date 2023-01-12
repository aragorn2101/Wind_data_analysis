#!/usr/bin/env python3
#
#  copyright (c) 2022 nitish ragoomundun, mauritius
#
#  permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "software"), to
#  deal in the software without restriction, including without limitation the
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
#  Data from UoM Farm:
#
#  Vocabulary [CF Standard Name Table v67]:
#      air_pressure (hPA) = air_pressure = BP_hPa_Avg
#      air_temperature (degree Celsius) = AirTC_Avg
#      wind_speed (m s-1) = WS_ms_Avg
#      standard_deviation_of_wind_speed (m s-1) = WS_ms_S_WVT
#      wind_direction (degree) = WindDir_D1_WVT
#      standard_deviation_of_wind_direction (degree) = WindDir_SD1_WVT
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
DataPath = "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_UoM_Farm"

# Check if given path for weather station data is indeed a directory
if not path.isdir(DataPath):
    print("{:s} is not a directory!".format(DataPath))
    exit(1)



###  BEGIN Open files and load relevant data into arrays  ###

##  Weather station data
filelist = sorted( listdir(DataPath) )

print("\nSuccessfully accessed directory")
print(DataPath)
print("\nContent of directory:")
print(filelist)

print()

for i in range(len(filelist)):
    print("Opening CSV file {:s} ...".format(DataPath + "/" + filelist[i]))

    tmp_df = pd.read_csv(DataPath + "/" + filelist[i], skiprows=[0,2,3], parse_dates=['TIMESTAMP'])

    if (i == 0):
        wind_df = tmp_df[['TIMESTAMP', 'WS_ms_Avg', 'WS_ms_S_WVT', 'WindDir_D1_WVT', 'WindDir_SD1_WVT']].dropna(axis=0, how='any')

    else:
        # Concatenate into main dataframe, wind_df
        wind_df = pd.concat([wind_df,
                             tmp_df[['TIMESTAMP', 'WS_ms_Avg', 'WS_ms_S_WVT', 'WindDir_D1_WVT', 'WindDir_SD1_WVT']].dropna(axis=0, how='any')],
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


# Resample
new_df = wind_df.resample(timedelta(days=1), axis=0, on='TIMESTAMP').mean()
new_df.reset_index(inplace=True)


###  BEGIN Plot  ###

print("\n\n")
print("------------------------------------------------------------")
print("Plotting wind speed data for period:")
print("{:s}  ->  {:s}".format(new_df['TIMESTAMP'].min().strftime("%d.%m.%Y"), new_df['TIMESTAMP'].max().strftime("%d.%m.%Y")))
print("for UoM Farm weather station.")
print("------------------------------------------------------------")
print("\n\n")


# Set size of figure for laptop screen (1600 x 900 pixels)
plt.rcParams["figure.figsize"] = [12.00,7.85]

# ------------------------------------------------------------------
fig, ax = plt.subplots(3,1)

fig.autofmt_xdate()
x_axis_format = mdates.DateFormatter('%b')

##  2015  ##
ax[0].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[0].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[0].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[0].set_ylabel("u (m/s)")
ax[0].grid(True, which='minor', axis='x')
ax[0].grid(True, which='major', axis='y')

mask = (new_df['TIMESTAMP'] >= '2015-01-01') & (new_df['TIMESTAMP'] <= '2015-12-31')
ax[0].set_xlim(date(year=2015, month=1, day=1), date(year=2015, month=12, day=31))
ax[0].set_ylim(0.0, 1.1*new_df['WS_ms_Avg'].loc[mask].max())
ax[0].plot(new_df['TIMESTAMP'].loc[mask], new_df['WS_ms_Avg'].loc[mask], linewidth=2.0, marker='o', color='blue')

##  2016  ##
ax[1].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[1].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[1].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[1].set_ylabel("u (m/s)")
ax[1].grid(True, which='minor', axis='x')
ax[1].grid(True, which='major', axis='y')

mask = (new_df['TIMESTAMP'] >= '2016-01-01') & (new_df['TIMESTAMP'] <= '2016-12-31')
ax[1].set_xlim(date(year=2016, month=1, day=1), date(year=2016, month=12, day=31))
ax[1].set_ylim(0.0, 1.1*new_df['WS_ms_Avg'].loc[mask].max())
ax[1].plot(new_df['TIMESTAMP'].loc[mask], new_df['WS_ms_Avg'].loc[mask], linewidth=2.0, marker='o', color='gold')

##  2022  ##
ax[2].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[2].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[2].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[2].set_ylabel("u (m/s)")
ax[2].grid(True, which='minor', axis='x')
ax[2].grid(True, which='major', axis='y')

mask = (new_df['TIMESTAMP'] >= '2022-01-01') & (new_df['TIMESTAMP'] <= '2022-12-31')
ax[2].set_xlim(date(year=2022, month=1, day=1), date(year=2022, month=12, day=31))
ax[2].set_ylim(0.0, 1.1*new_df['WS_ms_Avg'].loc[mask].max())
ax[2].plot(new_df['TIMESTAMP'].loc[mask], new_df['WS_ms_Avg'].loc[mask], linewidth=2.0, marker='o', color='green')


fig.tight_layout()


#print("Saving plot with filename {:s} ... \n\n".format("SWIO_raw_Vacoas.eps"))
#plt.savefig("SWIO_raw_Vacoas.eps", format='eps')
# ------------------------------------------------------------------

plt.show()

###  END Plot  ###


print()
exit(0)
