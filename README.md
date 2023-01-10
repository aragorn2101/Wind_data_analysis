# Wind data analysis

This repository contains a few Python scripts to perform operations on wind data.

We had the project of installing a wind turbine on the campus of our university, and we needed to perform certain feasibility studies. An important study is to measure wind speeds at different heights (ideally 5 m, 10 m, 20 m & 30 m) for different locations, and assess the wind power potential of each site. Since wind is a highly variable resource, both in terms of speed and direction, its speed or direction probability distributions cannot be characterized directly with analytical functions. Instead, we adapt parametric mathematical functions to the data distributions by determining values for the parameters which best fit the given data. As a result, the probability distribution for one site does not necessarily fit the data from another site. Furthermore, the methods for determining the parameters for best fit differ in both their applications and their results. Considering all these different factors, data from several distinct places and different sources have been analysed.

We are sharing the scripts here hoping that it benefits the science. Python is hugely popular in data science, as is working with CSV files and dataframes. Firstly, the scripts serve as examples of how to work with CSV files and transforming to NumPy arrays. In a few places we also deal with missing data, NaN values and infinity in calculations. Secondly, there's the wind data analysis itself, with parameter estimation methods for the Weibull function. Finally, there's a bit of data visualization using Matplotlib.

Below are short descriptions of the data sets. A few samples are given in the Sample_data directory in this repository.

_ _ to be continued _ _

