#!/usr/bin/env python3
#
#
#  Data from IOS-net:
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
                    "Mauritius Meteorological Station",
                    "Vacoas",
                    "./Sample_data/IOS-net/Vacoas",
                    "WD_nf01_Avg",
                    "WS_nf01_Avg",
                    0.50,
                    "(wind_df['timestamp'] < '2022-02-17 00:00:00') | ((wind_df['timestamp'] > '2022-03-09 23:59:00') & (wind_df['timestamp'] < '2022-05-29 00:00:00')) | (wind_df['timestamp'] > '2022-12-06 23:59:00')"
                   ],
                   [
                     "MRT",
                     "Bras d'Eau",
                     "./Sample_data/IOS-net/Bras_dEau",
                     "WD_mk01_Avg",
                     "WS_mk01_Avg",
                     0.20,
                     "(wind_df['timestamp'] < '2020-03-19 00:00:00') | ((wind_df['timestamp'] > '2020-05-18 23:59:00') & (wind_df['timestamp'] < '2022-01-14 00:00:00')) | (wind_df['timestamp'] > '2022-05-17 23:59:00')"
                   ],
                   [
                     "Reserves Tortues",
                     "Rodrigues",
                     "./Sample_data/IOS-net/Rodrigues",
                     "WD_mo01_Avg",
                     "WS_mo01_Avg",
                     0.50,
                     "(wind_df['timestamp'] < '2022-09-03 00:00:00') | (wind_df['timestamp'] > '2022-11-30 23:59:00')"
                   ],
                   [
                     "Réduit",
                     "UoM FoA rooftop, Réduit",
                     "./Sample_data/IOS-net/Reduit",
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
mask = (wind_df['timestamp'] < '2022-02-17') | ((wind_df['timestamp'] > '2022-03-09') & (wind_df['timestamp'] < '2022-05-29')) | (wind_df['timestamp'] > '2022-12-06')

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
fig, ax = plt.subplots(4,1)

fig.autofmt_xdate()
x_axis_format = mdates.DateFormatter('%b')

##  2019  ##
ax[0].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[0].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[0].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[0].set_ylabel("u (m/s)")
ax[0].grid(True, which='minor', axis='x')
ax[0].grid(True, which='major', axis='y')

mask = (new_df['timestamp'] >= '2019-01-01') & (new_df['timestamp'] <= '2019-12-31')
ax[0].set_xlim(date(year=2019, month=1, day=1), date(year=2019, month=12, day=31))
ax[0].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[0].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='blue')

##  2020  ##
ax[1].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[1].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[1].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[1].set_ylabel("u (m/s)")
ax[1].grid(True, which='minor', axis='x')
ax[1].grid(True, which='major', axis='y')

mask = (new_df['timestamp'] >= '2020-01-01') & (new_df['timestamp'] <= '2020-12-31')
ax[1].set_xlim(date(year=2020, month=1, day=1), date(year=2020, month=12, day=31))
ax[1].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[1].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='gold')

##  2021  ##
ax[2].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[2].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[2].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[2].set_ylabel("u (m/s)")
ax[2].grid(True, which='minor', axis='x')
ax[2].grid(True, which='major', axis='y')

mask = (new_df['timestamp'] >= '2021-01-01') & (new_df['timestamp'] <= '2021-12-31')
ax[2].set_xlim(date(year=2021, month=1, day=1), date(year=2021, month=12, day=31))
ax[2].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[2].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='green')

##  2022  ##
ax[3].xaxis.set_major_locator( mdates.MonthLocator(bymonthday=15) )
ax[3].xaxis.set_minor_locator( mdates.MonthLocator(bymonthday=1) )
ax[3].xaxis.set_major_formatter( mdates.DateFormatter('%b') )
ax[3].set_ylabel("u (m/s)")
ax[3].grid(True, which='minor', axis='x')
ax[3].grid(True, which='major', axis='y')

mask = (new_df['timestamp'] >= '2022-01-01') & (new_df['timestamp'] <= '2022-12-31')
ax[3].set_xlim(date(year=2022, month=1, day=1), date(year=2022, month=12, day=31))
ax[3].set_ylim(0.0, 1.1*new_df[ IOSnet_stations[stationIdx][4] ].loc[mask].max())
ax[3].plot(new_df['timestamp'].loc[mask], new_df[ IOSnet_stations[stationIdx][4] ].loc[mask], linewidth=2.0, marker='o', color='darkorchid')


fig.tight_layout()


#print("Saving plot with filename {:s} ... \n\n".format("IOSnet_raw_Vacoas.eps"))
#plt.savefig("IOSnet_raw_Vacoas.eps", format='eps')

#print("Saving plot with filename {:s} ... \n\n".format("IOSnet_raw_Vacoas.png"))
#plt.savefig("IOSnet_raw_Vacoas.png", format='png')
# ------------------------------------------------------------------

plt.show()

###  END Plot  ###


print()
exit(0)
