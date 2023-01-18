# Wind data analysis

This repository contains a few Python scripts to perform operations on wind data.

We had the project of installing a wind turbine on the campus of our university, and we needed to perform certain feasibility studies. An important study is to measure wind speeds at different heights (ideally 5 m, 10 m, 20 m & 30 m) for different locations, and assess the wind power potential of each site. Since wind is a highly variable resource, both in terms of speed and direction, its speed or direction probability distributions cannot be characterized directly with analytical functions. Instead, we adapt parametric mathematical functions to the data distributions by determining values for the parameters which best fit the given data. As a result, the probability distribution for one site does not necessarily fit the data from another site. Furthermore, the methods for determining the parameters for best fit differ in both their applications and their results. Considering all these different factors, data from several distinct places and different sources have been analysed.

We are sharing the scripts here hoping that it benefits the science. Python is hugely popular in data science, as is working with CSV files and dataframes. Firstly, the scripts serve as examples of how to work with CSV files and transforming to NumPy arrays. In a few places we also deal with missing data, NaN values and infinity in calculations. Secondly, there's the wind data analysis itself, with parameter estimation methods for the Weibull function. Finally, there's a bit of data visualization using Matplotlib.

## Script naming convention

Firstly, the name of each script gives hints about the data sources and tasks performed. The first few letters/syllables of the script name define the data source which is concerned. The different terminologies are described below:

__IOSnet :__ Indian Ocean Solar network project data. </br>
__Meteostat :__ data from Meteostat centralized platform for meteorological data. </br>
__UoM\_Farm :__ data from the Department of Physics weather station at University of Mauritius Farm. </br>
__WU :__ Weather Underground data from their world wide network of independent weather stations. </br>

_More details are given about the data sources in the next section below. A few sample data files are given in the __Sample\_data__ directory in this repository.

The following words in the script name briefly describe the tasks which the latter performs.

__...\_plot\_hist.py :__ script to plot the wind speed distribution histogram for the corresponding data source.

__...\_plot\_hist\_Weibull.py :__ plots the Weibull curves (calculated using all the different parameter estimation methods), overlaid on the histogram. The histogram is scaled so that the area of each bar corresponds to the probability of the wind speed falling in the corresponding bin.

__...\_plot\_yearly\_... :__ the script generates 1-year plots of the raw speed data. The data values are averaged over 2-day intervals for clear visualization.

__...\_calc\_Weibull\_diff.py :__ this script calculates the Weibull approximations using the different parameter estimation methods. Then, the statistical difference between each curve obtained for every pair of parameters (k, c) is computed and printed out.


## The IOS-net project data

The Indian Ocean Solar network ([IOS-net](https://galilee.univ-reunion.fr)) project is a regional initiative, funded by the European Union, to establish a network of meteorological research and data sharing among the islands including and surround Reunion Island. The objectives of this project involve the assessment of renewable energy potential on the islands, the study of photovoltaic panels in their working environment, research on meteorological forecasting models for renewable energy applications, assessment of the impact of climate change on renewable resources, and adaptation to the impacts caused by climate change. The IOS-net project is also very valuable for the region as it encourages the sharing of information and collaboration between scientists and engineers of the Indian Ocean islands. An aspect of this initiative is the installation of weather stations on the islands and the sharing of the meteorological data freely via web services ([https://galilee.univ-reunion.fr/thredds/catalog.html](https://galilee.univ-reunion.fr/thredds/catalog.html)) and a mobile application.

There are four IOS-net weather stations installed on the territory of the Republic of Mauritius.  Three are found in Mauritius with one in Rodrigues. The first one installed in Mauritius is found in Bras d'Eau, at the Mauritius Radio Telescope.  The second one is at Vacoas, in the compound of the Mauritius Meteorological Services.  The third one was installed in 2022 on the campus of the University of Mauritius. The latter is found on the roof of the UoM FoA building. All the data from every weather station is averaged over 1 minute.

There are many other stations on the other Indian Ocean islands, on Reunion island, Madagascar and Seychelles. Check out the IOS-net website: [https://galilee.univ-reunion.fr](https://galilee.univ-reunion.fr) for more details.


## Weather Underground

Weather Underground is a platform conceived by a community of amateur meteorologists who place the free sharing of data at the centre of their activities. They operate an open access website: [https://www.wunderground.com](https://www.wunderground.com). Anybody who possesses a weather station can register into the database, connect their device and upload data automatically. The website then constitutes a centralized platform where the data collected by thousands of independent weather stations around the world can be accessed. The equipment and protocols are more or less standardized to ensure a minimum of data quality. There are many weather stations in Mauritius which are registered with Weather Underground. There are two such stations quite close to Réduit. The closest one is at Bout du Monde, Ebène (code IPLAIN36: [https://www.wunderground.com/dashboard/pws/IPLAIN36](https://www.wunderground.com/dashboard/pws/IPLAIN36)). And, the other one is found at Quatres-Bornes (code IPLAINEW2: [https://www.wunderground.com/dashboard/pws/IPLAINEW2](https://www.wunderground.com/dashboard/pws/IPLAINEW2)). The data obtained from the database are daily averages.


## Meteostat: Plaisance

Meteostat is a platform which regroups data from public domains. The difference with Weather Underground is that Meteostat's sources are institutions which strictly abide by the norms set by the World Meteorological Organization. These sources include the National Oceanic and Atmospheric Administration (NOAA) of the United States, the Deutscher Wetterdienst of Germany and meteorological data from European Data Portal among many other sources. The platform is accessible through the webpage: [https://meteostat.net](https://meteostat.net), where long term data can be obtained for thousands of stations around the world.  Meteostat has two registered data sources for Mauritius. One station is in Plaisance and the other one in Vacoas. The Vacoas station only has data available from 2021 whereas the Plaisance station has data available from 2018 to date. The wind speed data obtained from the database are daily averages. We used only the data from the Plaisance station so that we complemented the IOS-net and Weather Underground data.


## Parameter estimation techniques implemented for the Weibull approximations


### Empirical method or standard deviation method (EMJ)

The approximation for k is given by (Justus et al., 1978). This method is also known as the standard deviation method.

$$   k ~=~ \Bigg( \frac{\sigma_U}{\bar{U}} \Bigg)^{-1.086} $$

This gives good results for cases where k lies between 1 and 10 (Manwell et al., 2009). Then, c is found using the following equation,

$$ c ~=~ \frac{ \bar{U} }{ \Gamma \left( 1 + 1/k \right) } $$


### Lysen empirical method (EML)

In this empirical method $k$ is determined using the following equation, devised by Justus et al. (1978). Then, $c$ is calculated using an approximation for the gamma function giving rise to the following expression (Lysen, 1983):

$$ \frac{c}{\bar{U}} ~=~ \Bigg( 0.568 ~+~ \frac{0.434}{k} \Bigg)^{ -\frac{1}{k} } $$


### Graphical method or least squares method (GM)

The _cumulative probability distribution_ corresponding to a particular Weibull function, characterized by parameters $k$ and $c$, is

$$ F(U) ~=~ 1 ~-~ \exp\left[ -\left(\frac{U}{c}\right)^{k} \right] $$

Taking the logarithm of the cumulative distribution yields:

$$ \ln \left\{ -\ln \left[ 1 - F(U) \right] \right\} ~=~ k\ln U ~-~ k\ln c $$

By plotting $\ln \left[ 1 - F(U) \right]$ against $U$ using log-log scales (Rohatgi & Nelson, 1994), the gradient of the line provides a way to find parameter $k$, and $c$ is subsequently determined using the y-intercept. Least squares regression is used to perform the calculation to minimize errors (Trustum & Jayatilaka, 1979).

It has often been shown that this method yields poor results. However, Deep et al. (2020) states that the poor results are due to a wrong definition of the cumulative probability density function. If $F(U_i)$ is actually the probability that a wind speed data value is less or equal to $U_i$, and $U_i$ is the value of wind speed at the upper edge (or middle value) of the histogram bar $i$. Then, we compare the linear relation $y_i ~=~ \text{gradient}.x_i + \text{y-intercept}$, with the following equation.

$$ \ln \big{ -\ln \left[ 1 - F(U_i) \right] \big} ~=~ k\ln U_i ~-~ k\ln c $$

Applying linear regression (Kenney & Keeping, 1962),

$$ \text{gradient} ~=~ \frac{\sum_{i=1}^n x_i y_i ~-~ n\bar{x}\bar{y}}{\sum_{i=1}^n x_i^2 ~-~ n\bar{x}^2} $$

$$ \text{y-intercept} ~=~ \frac{\bar{y}\sum_{i=1}^n x_i^2 ~-~ \bar{x}\sum_{i=1}^n x_i y_i}{\sum_{i=1}^n x_i^2 ~-~ n\bar{x}^2} $$


_to be continued_


## References

Deep, S., Sarkar, A., Ghawat, M., & Rajak, M. K. (2020). Estimation of the wind energy potential for coastal locations in India using the Weibull model. Renewable Energy, vol. 161, pp. 319–339, URL: [https://www.sciencedirect.com/science/article/pii/S0960148120311307](https://www.sciencedirect.com/science/article/pii/S0960148120311307).

Justus, C. G., Hargraves, W. R., Mikhail, A., & Graber, D. (1978). Methods for Estimating Wind Speed Frequency Distributions. Journal of Applied Meteorology (1962-1982), vol. 17, 3, pp. 350–353, URL: [http://www.jstor.org/stable/26178009](http://www.jstor.org/stable/26178009).

Kenney, J. F. & Keeping, E. S. (1962). Mathematics of Statistics, Part 1, 3rd Edition, chap. 15. Princeton, NJ: Van Nostrand.

Lysen, E. H. (1983). Introduction to Wind Energy - CWD 82-1. Consultancy Services Wind Energy Developing Countries, Amersfoort, Netherlands.

Manwell, J. F., McGowan, J. G., & Rogers, A. L. (2009). Wind Energy Explained, 2nd Edition. John Wiley & Sons, Ltd., West Sussex, United Kingdom, ISBN 9781119994367, doi:10.1002/9781119994367, URL: [https://onlinelibrary.wiley.com/doi/book/10.1002/9781119994367](https://onlinelibrary.wiley.com/doi/book/10.1002/9781119994367).

Rohatgi, J. S. & Nelson, V. (1994). Wind Characteristics: An Analysis for the Generation of Wind Power. Alternative Energy Institute, West Texas A&M University, Canyon, Texas, United States, ISBN 9780808714781.

Trustrum, K. & Jayatilaka, A. D. S. (1979). On estimating the Weibull modulus for a brittle material. Journal of Materials Science, vol. 14, 5, pp. 1080–1084.

