# sqlalchemy-challenge
Goal: Use **Python** and **SQLAlchemy** to do basic  analysis and data exploration of database

## Reflect Tables into SQLALchemy ORM

```python
  # create engine to hawaii.sqlite
  engine = create_engine("sqlite:///hawaii.sqlite"
  # reflect an existing database into a new model
  Base = automap_base()

  # reflect the tables
  Base.prepare(engine, reflect=True)

  # View all of the classes that automap found
  Base.classes.keys()

  # Save references to each table
  Measurement = Base.classes.measurement
  Station = Base.classes.station

  # Create our session (link) from Python to the DB
  session = Session(engine)
```

## Exploring Precipitation Data and Basic Analysis
- Design a query to retrieve the last 12 months of precipitation data and plot the results.

  ```python
    prcp_data=session.query(Measurement.date,Measurement.prcp)\
             .filter(Measurement.date>='2016-08-24')\
             .filter(Measurement.date<='2017-08-23').all()
  ```
  
- Convert the query results to a data frame and sort by date value
  
  ```python
    # Save the query results as a Pandas DataFrame and set the index to the date column
    prcp_df = pd.DataFrame(prcp_data).set_index('date')
    prcp_df = prcp_df.dropna()

    # Sort the dataframe by date
    prcp_df = prcp_df.sort_values(by='date')
  ```
- plot the results
  ![image](https://github.com/ludanzhan/sqlalchemy-challenge/blob/main/images/prcp.png)
 
 - Statistic Summary of the past 12 month precipitation data

    |count 	|2015|
    |------ |-----------|
    |mean 	|0.176462|
    |std 	  |0.460288|
    |min 	  |0|
    |25% 	  |0|
    |50% 	  |0.02|
    |75% 	  |0.13|
    |max 	  |6.7|
    
## Exploring Station Data and Basic Analysis
- Design a query to find the most active stations. List the stations and the counts in descending order.

  ```python
    session.query(Measurement.station, func.count(Measurement.station)).\
           group_by(Measurement.station).\
           order_by(func.count(Measurement.station).desc()).all()
  ```

- Calculate the lowest, highest, and average temperature of the most active stations

  ```python
    session.query(func.min(Measurement.tobs),\
            func.max(Measurement.tobs),\
            func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').all()
  ```

- Plot the results as a histogram
![image](https://github.com/ludanzhan/sqlalchemy-challenge/blob/main/images/hist.png)
    
## Temperature Analysis
- Define a function to return the minimum, maximum, and average temperatures for that range of dates
  ```python
    def calc_temps(start_date, end_date):
        """TMIN, TAVG, and TMAX for a list of dates.

        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d

        Returns:
            TMIN, TAVE, and TMAX
        """

        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
  ```
- Use the function `calc_temps` to calculate the tmin, tavg, and tmax for a year in the data set and  plot the result as a bar chart
![image](https://github.com/ludanzhan/sqlalchemy-challenge/blob/main/images/avg.png)

## Daily Temperature Normals
- Define a function to  calculate the daily normals (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)
  ```python
      def daily_normals(date):
        """Daily Normals.

        Args:
            date (str): A date string in the format '%m-%d'

        Returns:
            A list of tuples containing the daily normals, tmin, tavg, and tmax

        """

        sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
        return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
  ```
-  calculate the daily normals a date range push each tuple of calculations into a list called `normals`
    ```python
      normals = []

      # Set the start and end date of the trip
      start_date = '2017-08-01'
      end_date = '2017-08-07'

      # Use the start and end date to create a range of dates
      trip_dates = pd.date_range(start=start_date,end=end_date)

      # Strip off the year and save a list of strings in the format %m-%d
      trip_dates_normal = dates.strftime('%m-%d')

      # Use the `daily_normals` function to calculate the normals for each date string 
      for normal in trip_dates_normal:
          normals.append(daily_normals(normal))
      ```
-  Load the query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index

    |date  |tmin 	|tavg 	   |tmax	|
    |------|------|----------|-----|
    |08-01 |67.0 	|75.540000 	|83.0|
    |08-02 |68.0 	|75.603774 	|84.0|
    |08-03 |70.0 	|76.611111 	|85.0|
    |08-04 |69.0 	|76.711538 	|84.0|
    |08-05 |69.0 	|76.148148 	|82.0|
    |08-06 |67.0 	|76.250000 	|83.0|
    |08-07 |71.0 	|77.156863 	|83.0|

-  Plot the daily normals as an area plot with `stacked=False`
  ![image](https://github.com/ludanzhan/sqlalchemy-challenge/blob/main/images/normal.png)
