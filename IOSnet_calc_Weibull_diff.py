#!/usr/bin/env python3
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
#  The histogram data is fitted with a Weibull distribution whose
#  parameters are calculated using the following methods:
#
#  1. EMJ: Empirical method/standard deviation method (Justus et al., 1978)
#  2. EML: Lysen empirical method (Lysen, 1983)
#  3. Graphical Method - midpoints (Rohatgi & Nelson, 1994)
#  4. Graphical Method - upper edges (Rohatgi & Nelson, 1994)
#  5. Maximum likelihood method (Stevens & Smulders, 1979)
#  6. Modified maximum likelihood method (Seguro & Lambert, 2000)
#  7. Method of moments (Bowden et al. 1983)
#  8. Power density method (Akdag & Dinler, 2009)
#  9. Energy pattern factor method (Akdag & Guler, 2015)
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


###  Weibull parameter estimation methods  ###
W_param_est = ["EMJ", "EML", "GM1", "GM2", "ML", "MML", "MM", "PDM", "EPF"]
Weibull_P = []


###  Weather station index to calculate for  ###
#
# 0 : Vacoas
# 1 : MRT, Bras d'Eau
# 2 : Réserve Tortues, Rodrigues
# 3 : UoM FoA rooftop, Réduit
#
#
stationIdx = 3

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
                     "Rodrigues",
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



###  BEGIN parameter estimation  ###

#---------------------------------------------------------------------#
#  Empirical method/standard deviation method (Justus et al., 1978)
k = (ws_stddev / ws_mean)**-1.086
c = ws_mean / gamma(1.0 + 1.0/k)

print("Empirical method: k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Lysen empirical method (Lysen, 1983)
k = (ws_stddev / ws_mean)**-1.086
c = ws_mean * ( 0.568 + 0.434/k )**(-1.0/k)

print("Lysen empirical method: k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Graphical Method (Rohatgi & Nelson, 1994)

y = np.log( -1.0 * np.log(1.0 - cumul_P) )

# Eliminate NaN or Inf in y array which might arise due to log(0)
y = y[ np.logical_not( np.isnan(y) ) ]
y = y[ np.logical_not( np.isinf(y) ) ]

# midpoints
x = np.log( ws_midpts[0 : len(y)] )


den = (x * x).sum() - (len(x) * x.mean() * x.mean())

num = (x * y).sum() - (len(x) * x.mean() * y.mean())
k = num / den
num = (y.mean() * (x * x).sum()) - (x.mean() * (x * y).sum())
c = np.e**(-1.0 * (num / den) / k)

print("Graphical method (using histogram's midpoints): k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )


# upper edges
x = np.log( hist_edges[1 : 1+len(y)] )

den = (x * x).sum() - (len(x) * x.mean() * x.mean())

num = (x * y).sum() - (len(x) * x.mean() * y.mean())
k = num / den
num = (y.mean() * (x * x).sum()) - (x.mean() * (x * y).sum())
c = np.e**(-1.0 * (num / den) / k)

print("Graphical method (using histogram's upper edges): k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )

#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Maximum likelihood method (Stevens & Smulders, 1979)

# Seed k using estimate from empirical method (Justus et al., 1978)
k = (ws_stddev / ws_mean)**-1.086

# Take ln(avg_ws) and replace NaN values with 0.0
log_ws = np.log(avg_ws)
np.nan_to_num(log_ws, copy=False, nan=0.0, posinf=0.0, neginf=0.0)

# Find number of non-zero wind speed data points
n = np.count_nonzero( [ avg_ws > 0.1 ] )

i=0
while True:
    ws_pow_k = avg_ws**k

    prev_k = k
    k = 1.0 / ( (ws_pow_k * log_ws).sum()/ws_pow_k.sum() - log_ws.sum()/n )
    i = i + 1

    #print("#{:3d}\tk = {:4.2f}".format(i, k))

    if (abs(k - prev_k) < 0.005):
        break

# Calculate c from best estimates for k
c = ( (avg_ws**k).sum() / n )**(1/k)

print("Maximum likelihood method: k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Modified maximum likelihood method (Seguro & Lambert, 2000)

# Seed k using estimate from empirical method (Justus et al., 1978)
k = (ws_stddev / ws_mean)**-1.086

# Take ln(avg_ws) and replace NaN values with 0.0
log_ws = np.log(ws_midpts)
np.nan_to_num(log_ws, copy=False, nan=0.0, posinf=0.0, neginf=0.0)

# Total number of bins
n = hist_w8ts.sum()

i=0
#print("\nIterating for the maximum likelihood method ...")
#print("#{:3d}\tk = {:4.2f}".format(i, k))
while True:
    ws_pow_k = ws_midpts**k

    prev_k = k
    k = 1.0 / ( (ws_pow_k * log_ws * hist_w8ts).sum()/(ws_pow_k * hist_w8ts).sum() - (log_ws * hist_w8ts).sum()/n )
    i = i + 1

    #print("#{:3d}\tk = {:4.2f}".format(i, k))

    if (abs(k - prev_k) < 0.005):
        break

# Calculate c from best estimates for k
c = ( (ws_pow_k * hist_w8ts).sum()/n )**(1/k)

print("Modified maximum likelihood method: k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Method of moments (Bowden et al. 1983)
k = ( (0.9874*ws_mean) / ws_stddev )**1.0983
c = ws_mean / gamma(1.0 + 1.0/k)

print("Method of moments: k = {:.2f}\tc = {:.2f}".format(k,c))

Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Power density method (Akdag & Dinler, 2009)

# Seed k using estimate from empirical method (Justus et al., 1978)
k = (ws_stddev / ws_mean)**-1.086

i=0
while True:
    Epf = gamma(1.0 + 3.0/k) / ( gamma(1.0 + 1.0/k)**3 )

    prev_k = k
    k = 1.0 + 3.69/(Epf*Epf)
    i = i + 1

    if (abs(k - prev_k) < 0.005):
        break

c = ws_mean / gamma(1.0 + 1.0/k)

print("Power density method: k = {:.2f}\tc = {:.2f}".format(k,c))

Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Energy pattern factor method (Akdag & Guler, 2015)

# Seed k using estimate from empirical method (Justus et al., 1978)
k = (ws_stddev / ws_mean)**-1.086

i=0
while True:
    Epf = gamma(1.0 + 3.0/k) / ( gamma(1.0 + 1.0/k)**3 )

    prev_k = k
    k = (0.59039*Epf**4 + 2.15143*Epf**3 - 5.78961*Epf*Epf + 3.27527*Epf - 0.220374) / (0.992007*Epf**4 - 0.800468*Epf**3 - 2.60973*Epf*Epf + 3.69115*Epf - 1.27285)
    i = i + 1

    if (abs(k - prev_k) < 0.005):
        break

c = ws_mean / gamma(1.0 + 1.0/k)

print("Energy pattern factor method: k = {:.2f}\tc = {:.2f}".format(k,c))

Weibull_P.append( (k/c) * (ws_midpts/c)**(k-1) * np.exp(-1.0 * (ws_midpts/c)**k) )
#---------------------------------------------------------------------#

###  END parameter estimation  ###



###  BEGIN Statistical comparison  ###

#---------------------------------------------------------------------#
#  Root Mean Square Error (RMSE)

RMSE = []
for i in range( len(W_param_est) ):
    diff = (Weibull_P[i] - ws_P) * (Weibull_P[i] - ws_P)
    RMSE.append( np.sqrt( diff.sum() / len(diff) ) )

print()
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
#  Coefficient of Determination (R^2)

Rsqrd = []
diff_den = (ws_P - ws_P.mean()) * (ws_P - ws_P.mean())
for i in range( len(W_param_est) ):
    diff_num = (Weibull_P[i] - ws_P) * (Weibull_P[i] - ws_P)
    Rsqrd.append( 1 - ( diff_num.sum() / diff_den.sum() ) )

print()
#---------------------------------------------------------------------#

#---------------------------------------------------------------------#
#  Mean Absolute Percentage Error (MAPE)

MAPE = []
for i in range( len(W_param_est) ):
    diff = np.abs(Weibull_P[i] - ws_P) / ws_P
    np.nan_to_num(diff, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
    MAPE.append( ( diff.sum() / len(diff) ) * 100.0 )

print()
#---------------------------------------------------------------------#

###  END Statistical comparison  ###


print("\n\n")
print("------------------------------------------------------------")
print()
print("Computed the Weibull curve for the wind speed data from the IOS-net project")
print("for the weather station found at")
print("{:s}, {:s}".format(IOSnet_stations[stationIdx][0], IOSnet_stations[stationIdx][1]))
print("Data ranges from {:s}  to  {:s}".format(wind_df['timestamp'].min().strftime("%d.%m.%Y"), wind_df['timestamp'].max().strftime("%d.%m.%Y")))
print()
print("------------------------------------------------------------")
print()
print("Statistical difference between actual wind speed data distribution and the")
print("Weibull curve:")
print()
print("Method \t RMSE     R squared       MAPE")
print("------------------------------------------------------------")
for i in range( len(W_param_est) ):
    print("{:s} \t {:7.5f}    {:7.5f}   {:7.5f}".format(W_param_est[i], RMSE[i], Rsqrd[i], MAPE[i]))
print("------------------------------------------------------------")


print()
exit(0)