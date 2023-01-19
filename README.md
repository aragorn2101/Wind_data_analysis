# Wind data analysis

This repository contains a few Python scripts to perform operations on wind data.

We had the project of installing a wind turbine on the campus of our university, and we needed to perform certain feasibility studies. An important study is to measure wind speeds at different heights (ideally 5 m, 10 m, 20 m & 30 m) for different locations, and assess the wind power potential of each site. Since wind is a highly variable resource, both in terms of speed and direction, its speed or direction probability distributions cannot be characterized directly with analytical functions. Instead, we adapt parametric mathematical functions to the data distributions by determining values for the parameters which best fit the given data. As a result, the probability distribution for one site does not necessarily fit the data from another site. Furthermore, the methods for determining the parameters for best fit differ in both their applications and their results. Considering all these different factors, data from several distinct places and different sources have been analysed.

We are sharing the scripts here hoping that it benefits the science. Python is hugely popular in data science, as is working with CSV files and dataframes. Firstly, the scripts serve as examples of how to work with CSV files and transforming to NumPy arrays. In a few places we also deal with missing data, NaN values and infinity in calculations. Secondly, there's the wind data analysis itself, with parameter estimation methods for the Weibull function. Finally, there's a bit of data visualization using Matplotlib.

## Script naming convention

Firstly, the name of each script gives hints about the data sources and tasks performed. The first few letters/syllables of the script name define the data source which is concerned. The different terminologies are described below:

`IOSnet` : Indian Ocean Solar network project data. </br>
`Meteostat` : data from Meteostat centralized platform for meteorological data. </br>
`UoM_Farm` : data from the Department of Physics weather station at University of Mauritius Farm. </br>
`WU` : Weather Underground data from their world wide network of independent weather stations. </br>

More details are given about the data sources in the next section below. A few sample data files are given in the `Sample_data` directory in this repository.

The following words in the script name briefly describe the tasks which the latter performs.

`..._plot_hist.py` : script to plot the wind speed distribution histogram for the corresponding data source.

`..._plot_hist_Weibull.py` : plots the Weibull curves (calculated using all the different parameter estimation methods), overlaid on the histogram. The histogram is scaled so that the area of each bar corresponds to the probability of the wind speed falling in the corresponding bin.

`..._plot_yearly_...` : the script generates 1-year plots of the raw speed data. The data values are averaged over 2-day intervals for clear visualization.

`..._calc_Weibull_diff.py` : this script calculates the Weibull approximations using the different parameter estimation methods. Then, the statistical difference between each curve obtained for every pair of parameters (k, c) is computed and printed out.


## The IOS-net project data

The Indian Ocean Solar network ([IOS-net](https://galilee.univ-reunion.fr)) project is a regional initiative, funded by the European Union, to establish a network of meteorological research and data sharing among the islands including and surround Reunion Island. The objectives of this project involve the assessment of renewable energy potential on the islands, the study of photovoltaic panels in their working environment, research on meteorological forecasting models for renewable energy applications, assessment of the impact of climate change on renewable resources, and adaptation to the impacts caused by climate change. The IOS-net project is also very valuable for the region as it encourages the sharing of information and collaboration between scientists and engineers of the Indian Ocean islands. An aspect of this initiative is the installation of weather stations on the islands and the sharing of the meteorological data freely via web services ([https://galilee.univ-reunion.fr/thredds/catalog.html](https://galilee.univ-reunion.fr/thredds/catalog.html)) and a mobile application.

There are four IOS-net weather stations installed on the territory of the Republic of Mauritius.  Three are found in Mauritius with one in Rodrigues. The first one installed in Mauritius is found in Bras d'Eau, at the Mauritius Radio Telescope.  The second one is at Vacoas, in the compound of the Mauritius Meteorological Services.  The third one was installed in 2022 on the campus of the University of Mauritius. The latter is found on the roof of the UoM FoA building. All the data from every weather station is averaged over 1 minute.

There are many other stations on the other Indian Ocean islands, on Reunion island, Madagascar and Seychelles. Check out the IOS-net website: [https://galilee.univ-reunion.fr](https://galilee.univ-reunion.fr) for more details.


## Weather Underground

Weather Underground is a platform conceived by a community of amateur meteorologists who place the free sharing of data at the centre of their activities. They operate an open access website: [https://www.wunderground.com](https://www.wunderground.com). Anybody who possesses a weather station can register into the database, connect their device and upload data automatically. The website then constitutes a centralized platform where the data collected by thousands of independent weather stations around the world can be accessed. The equipment and protocols are more or less standardized to ensure a minimum of data quality. There are many weather stations in Mauritius which are registered with Weather Underground. There are two such stations quite close to Réduit. The closest one is at Bout du Monde, Ebène (code IPLAIN36: [https://www.wunderground.com/dashboard/pws/IPLAIN36](https://www.wunderground.com/dashboard/pws/IPLAIN36)). And, the other one is found at Quatres-Bornes (code IPLAINEW2: [https://www.wunderground.com/dashboard/pws/IPLAINEW2](https://www.wunderground.com/dashboard/pws/IPLAINEW2)). The data obtained from the database are daily averages.


## Meteostat: Plaisance

Meteostat is a platform which regroups data from public domains. The difference with Weather Underground is that Meteostat's sources are institutions which strictly abide by the norms set by the World Meteorological Organization. These sources include the National Oceanic and Atmospheric Administration (NOAA) of the United States, the Deutscher Wetterdienst of Germany and meteorological data from European Data Portal among many other sources. The platform is accessible through the webpage: [https://meteostat.net](https://meteostat.net), where long term data can be obtained for thousands of stations around the world.  Meteostat has two registered data sources for Mauritius. One station is in Plaisance and the other one in Vacoas. The Vacoas station only has data available from 2021 whereas the Plaisance station has data available from 2018 to date. The wind speed data obtained from the database are daily averages. We used only the data from the Plaisance station so that we complemented the IOS-net and Weather Underground data.


## Techniques implemented for estimating the Weibull parameters k and c

Eight distinct methods are used to estimate the parameters $k$ and $c$
characterizing the Weibull probability curve.


1. EMJ: Empirical method/standard deviation method (Justus et al., 1978)
2. EML: Lysen empirical method (Lysen, 1983)
3. GM: Graphical Method - midpoints (Rohatgi & Nelson, 1994) </br>
   This method is actually computed twice using different values for the
   probability predicted by the Weibull curve. One convention involved using
   midpoints of the histogram bars while the other convention used the upper
   edge of the bars.
4. MLM: Maximum likelihood method (Stevens & Smulders, 1979)
5. MMLM: Modified maximum likelihood method (Seguro & Lambert, 2000)
6. MM: Method of moments (Bowden et al. 1983)
7. PDM: Power density method (Akdag & Dinler, 2009)
8. EPF: Energy pattern factor method (Akdag & Guler, 2015)


## References

Justus, C. G., Hargraves, W. R., Mikhail, A., & Graber, D. (1978). Methods for Estimating Wind Speed Frequency Distributions. Journal of Applied Meteorology (1962-1982), vol. 17, 3, pp. 350–353, URL: [http://www.jstor.org/stable/26178009](http://www.jstor.org/stable/26178009).

Lysen, E. H. (1983). Introduction to Wind Energy - CWD 82-1. Consultancy Services Wind Energy Developing Countries, Amersfoort, Netherlands.

Rohatgi, J. S. & Nelson, V. (1994). Wind Characteristics: An Analysis for the Generation of Wind Power. Alternative Energy Institute, West Texas A&M University, Canyon, Texas, United States, ISBN 9780808714781.

Stevens, M. J. M. & Smulders, P. T. (1979). The Estimation of the Parameters of the Weibull Wind Speed Distribution for Wind Energy Utilization Purposes. Wind Engineering, vol. 3, 2, pp. 132–145, URL: [http://www.jstor.org/stable/43749134](http://www.jstor.org/stable/43749134).

