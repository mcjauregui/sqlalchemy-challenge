# sqlalchemy-challenge

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task.

Part 1: Analyze and Explore the Climate Data
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

Note that you’ll use the provided files (climate_starter.ipynb and hawaii.sqlite) to complete your climate analysis and data exploration.

Use the SQLAlchemy create_engine() function to connect to your SQLite database.
Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.
Link Python to the database by creating a SQLAlchemy session.
Remember to close your session at the end of your notebook.

Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections.

Precipitation Analysis
Find the most recent date in the dataset.  
  Answer: Most Recent Measurement Date: 2017-08-23

Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
Load the query results into a Pandas DataFrame. Explicitly set the column names. Sort the DataFrame values by "date".  
  Answer:  
        Date        Precipitation
  0     2016-08-24           0.08
  1006  2016-08-24           0.00
  1524  2016-08-24           2.15  
  702   2016-08-24           2.28
  360   2016-08-24           2.15
  ...          ...            ...
  1522  2017-08-22           0.00
  1523  2017-08-23           0.08
  359   2017-08-23           0.00
  1005  2017-08-23           0.00
  2222  2017-08-23           0.45

[2223 rows x 2 columns]

Plot the results by using the DataFrame plot method.  
![image](https://github.com/mcjauregui/sqlalchemy-challenge/assets/151464511/2dd8ee07-4f55-4c9f-8e8b-f3067d4c5bc8)

Use Pandas to print the summary statistics for the precipitation data.    
  Answer:    
         Precipitation  
  count    2223.000000
  mean        0.159951
  std         0.441220
  min         0.000000
  25%         0.000000
  50%         0.010000
  75%         0.110000
  max         6.700000


Station Analysis
Design a query to calculate the total number of stations in the dataset.  
  Answer: Distinct Station Count = 9  

Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
List the stations and observation counts in descending order.  
  Answer:   
  [('USC00519281', 2772), ('USC00519397', 2724), ('USC00513117', 2709), ('USC00519523',2669),
  ('USC00516128', 2612), ('USC00514830', 2202), ('USC00511918', 1979), ('USC00517948', 1372),
  ('USC00518838', 511)]
  
Answer the following question: which station id has the greatest number of observations?  
  Answer: USC00519281  

Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.  
  Answer:   
    Min: 59.0  
    Max: 83.0  
    Mean: 73.0968660968661  

Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:  
Filter by the station that has the greatest number of observations.  
Query the previous 12 months of TOBS data for that station.  
Plot the results as a histogram with bins=12.    
![image](https://github.com/mcjauregui/sqlalchemy-challenge/assets/151464511/1282164e-532b-435f-aa41-975699b0378b)

Close your session.

Part 2: Design Your Climate App  
Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:  
Start at the homepage.  
List all the available routes.  

/api/v1.0/precipitation  
Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.  
  Answer:  https://github.com/mcjauregui/sqlalchemy-challenge/blob/main/Screenshot%202024-03-18%20234815.png

/api/v1.0/stations
Return a JSON list of stations from the dataset.

/api/v1.0/tobs
Query the dates and temperature observations of the most-active station for the previous year of data.
Return a JSON list of temperature observations for the previous year.
Answer: https://github.com/mcjauregui/sqlalchemy-challenge/blob/main/Screenshot%202024-03-18%20234845.png


Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

/api/v1.0/<start> 
Answer: 

/api/v1.0/<start>/<end>
Answer:
