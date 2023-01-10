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
#
#
stationIdx = 2


IOSnet_stations = [["Vacoas",
                    "Mauritius Meteorological Station, Vacoas",
                    "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_IOSnet/Vacoas",
                    "WD_nf01_Avg",
                    "WS_nf01_Avg"],
                   ["MRT",
                    "Bras d'Eau",
                    "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_IOSnet/Bras_dEau",
                    "WD_mk01_Avg",
                    "WS_mk01_Avg"],
                   ["Reserves Tortues",
                    "Reserves Tortues, Rodrigues",
                    "/mnt/80_GiB_DATA/data/FARWIND_UoM/Data_IOSnet/Rodrigues",
                    "WD_mo01_Avg",
                    "WS_mo01_Avg"]]



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
    # WD_nf01_Avg: average wind direction (degrees)
    # WS_nf01_Avg: wind speed
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

# Mask excluding gaps in the data
mask = (wind_df['timestamp'] < '2022-09-03') | (wind_df['timestamp'] > '2022-11-30')

# Apply mask and resample
trim_df = wind_df.loc[mask]
new_df = trim_df.resample(timedelta(days=2), axis=0, on='timestamp').mean()
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
print("{:s}  ->  {:s}".format(new_df['timestamp'].min().strftime("%d.%m.%Y"), new_df['timestamp'].max().strftime("%d.%m.%Y")))
print("for IOSnet weather station at {:s}".format(IOSnet_stations[stationIdx][1]))
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

mask = (new_df['timestamp'] >= '2018-01-01') & (new_df['timestamp'] <= '2018-12-31')
ax[0].set_xlim(date(year=2018, month=1, day=1), date(year=2018, month=12, day=31))
ax[0].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[0].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='red')

##  2019  ##
ax[1].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[1].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[1].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[1].set_ylabel("u (m/s)")
ax[1].grid(True, which='minor', axis='x')
ax[1].grid(True, which='major', axis='y')

mask = (new_df['timestamp'] >= '2019-01-01') & (new_df['timestamp'] <= '2019-12-31')
ax[1].set_xlim(date(year=2019, month=1, day=1), date(year=2019, month=12, day=31))
ax[1].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[1].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='blue')

##  2020  ##
ax[2].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[2].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[2].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[2].set_ylabel("u (m/s)")
ax[2].grid(True, which='minor', axis='x')
ax[2].grid(True, which='major', axis='y')

mask = (new_df['timestamp'] >= '2020-01-01') & (new_df['timestamp'] <= '2020-12-31')
ax[2].set_xlim(date(year=2020, month=1, day=1), date(year=2020, month=12, day=31))
ax[2].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[2].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='gold')

##  2021  ##
ax[3].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[3].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[3].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[3].set_ylabel("u (m/s)")
ax[3].grid(True, which='minor', axis='x')
ax[3].grid(True, which='major', axis='y')

mask = (new_df['timestamp'] >= '2021-01-01') & (new_df['timestamp'] <= '2021-12-31')
ax[3].set_xlim(date(year=2021, month=1, day=1), date(year=2021, month=12, day=31))
ax[3].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[3].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='green')

##  2022  ##
ax[4].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[4].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[4].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[4].set_ylabel("u (m/s)")
ax[4].grid(True, which='minor', axis='x')
ax[4].grid(True, which='major', axis='y')

mask = (new_df['timestamp'] >= '2022-01-01') & (new_df['timestamp'] <= '2022-12-31')
ax[4].set_xlim(date(year=2022, month=1, day=1), date(year=2022, month=12, day=31))
ax[4].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[4].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='darkorchid')


fig.tight_layout()


#print("Saving plot with filename {:s} ... \n\n".format("IOSnet_raw_Rodrigues.eps"))
#plt.savefig("IOSnet_raw_Rodrigues.eps", format='eps')

#print("Saving plot with filename {:s} ... \n\n".format("IOSnet_raw_Rodrigues.png"))
#plt.savefig("IOSnet_raw_Rodrigues.png", format='png')
# ------------------------------------------------------------------

plt.show()

###  END Plot  ###


print()
exit(0)
