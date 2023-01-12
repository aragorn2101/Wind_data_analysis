# Wind data analysis

This repository contains a few Python scripts to perform operations on wind data.

We had the project of installing a wind turbine on the campus of our university, and we needed to perform certain feasibility studies. An important study is to measure wind speeds at different heights (ideally 5 m, 10 m, 20 m & 30 m) for different locations, and assess the wind power potential of each site. Since wind is a highly variable resource, both in terms of speed and direction, its speed or direction probability distributions cannot be characterized directly with analytical functions. Instead, we adapt parametric mathematical functions to the data distributions by determining values for the parameters which best fit the given data. As a result, the probability distribution for one site does not necessarily fit the data from another site. Furthermore, the methods for determining the parameters for best fit differ in both their applications and their results. Considering all these different factors, data from several distinct places and different sources have been analysed.

We are sharing the scripts here hoping that it benefits the science. Python is hugely popular in data science, as is working with CSV files and dataframes. Firstly, the scripts serve as examples of how to work with CSV files and transforming to NumPy arrays. In a few places we also deal with missing data, NaN values and infinity in calculations. Secondly, there's the wind data analysis itself, with parameter estimation methods for the Weibull function. Finally, there's a bit of data visualization using Matplotlib.

Below are short descriptions of the data sets. A few sample data files are given in the Sample_data directory in this repository.

## The IOS-net project data

The Indian Ocean Solar network ([IOS-net](https://galilee.univ-reunion.fr)) project is a regional initiative, funded by the European Union, to establish a network of meteorological research and data sharing among the islands including and surround Reunion Island. The objectives of this project involve the assessment of renewable energy potential on the islands, the study of photovoltaic panels in their working environment, research on meteorological forecasting models for renewable energy applications, assessment of the impact of climate change on renewable resources, and adaptation to the impacts caused by climate change. The IOS-net project is also very valuable for the region as it encourages the sharing of information and collaboration between scientists and engineers of the Indian Ocean islands. An aspect of this initiative is the installation of weather stations on the islands and the sharing of the meteorological data freely via web services ([https://galilee.univ-reunion.fr/thredds/catalog.html](https://galilee.univ-reunion.fr/thredds/catalog.html)) and a mobile application.

There are four IOS-net weather stations installed on the territory of the Republic of Mauritius.  Three are found in Mauritius with one in Rodrigues. The first one installed in Mauritius is found in Bras d'Eau, at the Mauritius Radio Telescope.  The second one is at Vacoas, in the compound of the Mauritius Meteorological Services.  The third one was installed in 2022 on the campus of the University of Mauritius. The latter is found on the roof of the UoM FoA building. All the data from every weather station is averaged over 1 minute.

There are many other stations on the other Indian Ocean islands, on Reunion island, Madagascar and Seychelles. Check out the IOS-net website: [https://galilee.univ-reunion.fr](https://galilee.univ-reunion.fr) for more details.

