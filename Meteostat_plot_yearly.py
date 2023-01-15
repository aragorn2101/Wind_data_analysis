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
DataPath = "./Sample_data/Meteostat/Plaisance_20180101_-_20221231.csv"

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

# Resample
new_df = wind_df.resample(timedelta(days=2), axis=0, on='date').mean()
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
print("{:s}  ->  {:s}".format(new_df['date'].min().strftime("%d.%m.%Y"), new_df['date'].max().strftime("%d.%m.%Y")))
print("for Meteostat weather station at Plaisance, Mauritius")
print("------------------------------------------------------------")
print("\n\n")


# Set size of figure for laptop screen (1600 x 900 pixels)
plt.rcParams["figure.figsize"] = [12.00,7.85]

# ------------------------------------------------------------------
fig, ax = plt.subplots(5,1)

fig.autofmt_xdate()
x_axis_format = mdates.DateFormatter('%b')

##  2018  ##
ax[0].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[0].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[0].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[0].set_ylabel("u (m/s)")
ax[0].grid(True, which='minor', axis='x')
ax[0].grid(True, which='major', axis='y')

mask = (new_df['date'] >= '2018-01-01') & (new_df['date'] <= '2018-12-31')
ax[0].set_xlim(date(year=2018, month=1, day=1), date(year=2018, month=12, day=31))
ax[0].set_ylim(0.0, 1.1*new_df['wspd'].loc[mask].max())
ax[0].plot(new_df['date'].loc[mask], new_df['wspd'].loc[mask], linewidth=2.0, marker='o', color='red')

##  2019  ##
ax[1].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[1].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[1].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[1].set_ylabel("u (m/s)")
ax[1].grid(True, which='minor', axis='x')
ax[1].grid(True, which='major', axis='y')

mask = (new_df['date'] >= '2019-01-01') & (new_df['date'] <= '2019-12-31')
ax[1].set_xlim(date(year=2019, month=1, day=1), date(year=2019, month=12, day=31))
ax[1].set_ylim(0.0, 1.1*new_df['wspd'].loc[mask].max())
ax[1].plot(new_df['date'].loc[mask], new_df['wspd'].loc[mask], linewidth=2.0, marker='o', color='blue')

##  2020  ##
ax[2].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[2].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[2].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[2].set_ylabel("u (m/s)")
ax[2].grid(True, which='minor', axis='x')
ax[2].grid(True, which='major', axis='y')

mask = (new_df['date'] >= '2020-01-01') & (new_df['date'] <= '2020-12-31')
ax[2].set_xlim(date(year=2020, month=1, day=1), date(year=2020, month=12, day=31))
ax[2].set_ylim(0.0, 1.1*new_df['wspd'].loc[mask].max())
ax[2].plot(new_df['date'].loc[mask], new_df['wspd'].loc[mask], linewidth=2.0, marker='o', color='gold')

##  2021  ##
ax[3].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[3].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[3].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[3].set_ylabel("u (m/s)")
ax[3].grid(True, which='minor', axis='x')
ax[3].grid(True, which='major', axis='y')

mask = (new_df['date'] >= '2021-01-01') & (new_df['date'] <= '2021-12-31')
ax[3].set_xlim(date(year=2021, month=1, day=1), date(year=2021, month=12, day=31))
ax[3].set_ylim(0.0, 1.1*new_df['wspd'].loc[mask].max())
ax[3].plot(new_df['date'].loc[mask], new_df['wspd'].loc[mask], linewidth=2.0, marker='o', color='green')

##  2022  ##
ax[4].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[4].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[4].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[4].set_ylabel("u (m/s)")
ax[4].grid(True, which='minor', axis='x')
ax[4].grid(True, which='major', axis='y')

mask = (new_df['date'] >= '2022-01-01') & (new_df['date'] <= '2022-12-31')
ax[4].set_xlim(date(year=2022, month=1, day=1), date(year=2022, month=12, day=31))
ax[4].set_ylim(0.0, 1.1*new_df['wspd'].loc[mask].max())
ax[4].plot(new_df['date'].loc[mask], new_df['wspd'].loc[mask], linewidth=2.0, marker='o', color='darkorchid')


fig.tight_layout()
# ------------------------------------------------------------------


plt.show()

###  END Plot  ###


print()
exit(0)
