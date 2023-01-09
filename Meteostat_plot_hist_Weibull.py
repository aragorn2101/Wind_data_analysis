#!/usr/bin/env python3
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
#  The histogram data is fitted with a Weibull distribution whose
#  parameters are calculated using the following methods:
#
#  1. Empirical method/standard deviation method (Justus et al., 1978)
#  2. Lysen empirical method (Lysen, 1983)
#  3. Graphical Method - midpoints (Rohatgi & Nelson, 1994)
#  4. Graphical Method - upper edges (Rohatgi & Nelson, 1994)
#  5. Maximum likelihood method (Stevens & Smulders, 1979)
#  6. Modified maximum likelihood method (Seguro & Lambert, 2000)
#  7. Method of moments (Bowden et al. 1983)
#  8. Power density method (Akdag & Dinler, 2009)
#  9. Energy pattern factor method (Akdag & Guler, 2015)
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

bin_size = 1.5  # m/s
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

# Array containing abscissa for plotting Weibull curve using estimates of
# k and c
u = np.linspace(0.0, ceil_ws, 100)  # numpy array


#---------------------------------------------------------------------#
#  Empirical method/standard deviation method (Justus et al., 1978)
k = (ws_stddev / ws_mean)**-1.086
c = ws_mean / gamma(1.0 + 1.0/k)

print("Empirical method: k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
EMJ = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Lysen empirical method (Lysen, 1983)
k = (ws_stddev / ws_mean)**-1.086
c = ws_mean * ( 0.568 + 0.434/k )**(-1.0/k)

print("Lysen empirical method: k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
EML = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)
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
GM1 = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)


# upper edges
x = np.log( hist_edges[1 : 1+len(y)] )

den = (x * x).sum() - (len(x) * x.mean() * x.mean())

num = (x * y).sum() - (len(x) * x.mean() * y.mean())
k = num / den
num = (y.mean() * (x * x).sum()) - (x.mean() * (x * y).sum())
c = np.e**(-1.0 * (num / den) / k)

print("Graphical method (using histogram's upper edges): k = {:.2f}\tc = {:.2f}".format(k,c))

# Calculate curve
GM2 = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)

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
ML = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)
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
MML = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)
#---------------------------------------------------------------------#


#---------------------------------------------------------------------#
#  Method of moments (Bowden et al. 1983)
k = ( (0.9874*ws_mean) / ws_stddev )**1.0983
c = ws_mean / gamma(1.0 + 1.0/k)

print("Method of moments: k = {:.2f}\tc = {:.2f}".format(k,c))

MM = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)
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

PDM = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)
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

EPF = (k/c) * (u/c)**(k-1) * np.exp(-1.0 * (u/c)**k)
#---------------------------------------------------------------------#

###  END parameter estimation  ###


print()


###  BEGIN Plot  ###

# Set size of figure for laptop screen (1600 x 900 pixels)
plt.rcParams["figure.figsize"] = [12.00,7.85]

# maximum y ordinate
ceil_y = 1.1 * np.max([ws_P.max(), EMJ.max(), EML.max(), GM1.max(), GM2.max(), ML.max(), MML.max(), MM.max(), PDM.max(), EPF.max()])

fig, ax = plt.subplots(1,1)

#ax.set_xlim(0.0, 9.0)
ax.set_xlim(0.0, ceil_ws)
ax.set_ylim( 0.0, ceil_y)
ax.set_xlabel("Wind speed (m/s)")
ax.set_ylabel("Probability density")
ax.bar(hist_edges[:-1], ws_P, align='edge', width=bin_size, color='whitesmoke', edgecolor='black', linewidth=1.5)
ax.plot(u, EMJ,  linewidth=2.0, marker='o', color='red', label="EMJ")
ax.plot(u, EML,  linewidth=2.0, marker='v', color='chocolate', label="EML")
ax.plot(u, GM1,  linewidth=2.0, marker='+', color='olive', label="GM1")
ax.plot(u, GM2,  linewidth=2.0, marker='D', color='darkorchid', label="GM2")
ax.plot(u, ML,   linewidth=2.0, marker='^', color='goldenrod', label="ML")
ax.plot(u, MML,  linewidth=2.0, marker='x', color='gold', label="MML")
ax.plot(u, MM,   linewidth=2.0, marker='s', color='steelblue', label="MM")
ax.plot(u, PDM,  linewidth=2.0, marker='1', color='green', label="PDM")
ax.plot(u, EPF,  linewidth=2.0, marker='|', color='purple', label="EPF")

ax.legend(loc="upper right", bbox_to_anchor=(0.90,0.90), frameon=True).get_frame().set_alpha(1.0)
fig.tight_layout()

plt.show()

###  END Plot  ###


print()
exit(0)
