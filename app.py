
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData, Table, inspect, select, desc
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session, sessionmaker
import sqlite3
import sqlalchemy
import json
import datetime

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
connection = engine.connect()

# reflect existing database into new model
Base = automap_base()
# reflect the tables
#Base.prepare(engine, autoload_with=engine) method returned error
Base.prepare(engine, reflect=True)

# Access reflected tables as classes/Save references to each table/Define models
Measurement = Base.classes.measurement
Station = Base.classes.station

# Statements needed to identify all tables and all columns within tables of sqlite db:
# Create MetaData object/Define metadata
metadata = MetaData()
# Reflect database tables into MetaData/ Reflect table from database
metadata.reflect(bind=engine)
# View all classes that automap found
Base.classes.keys()

# Statements needed to identify table and column names in sqlite db:
# https://bootcampspot.instructure.com/courses/4981/external_tools/313
# Create inspector
inspector = inspect(engine)
# Get list of table names in database
table_names = inspector.get_table_names()
# Create Session Object to Connect Python to DB
Session = sessionmaker(bind=engine)
session = Session()
# Access 'measurement' and 'station' tables
Measurement = metadata.tables['measurement']
Station = metadata.tables['station']
#################################################
# Flask Setup
#################################################
# Import Flask
from flask import Flask, jsonify, request
app = Flask(__name__)
###############################################
# Flask Routes
#################################################
# Define what to do when user hits index route
# Start at the homepage and list all available routes

# Assistance with temperature date range routes statements provided by Daewon Kwon, Lori Ka, and Margaret Thorpe
@app.route("/")
def home():
    return (
        f"Hello, Hawaii weather data seekers! Welcome to the home page.<br/>"
        f"These are the available routes you can take from here:<br/>"
        f"/api.v1.0/precipitation<br/>"
        f"/api.v1.0/stations<br/>"
        f"/api.v1.0/tobs<br/>"
        f"/api.v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/trip/YYYY-MM-DD/YYYY-MM-DD<br>"
             )

# Define the /api.v1.0/precipitation route
import datetime
@app.route("/api.v1.0/precipitation")
def precipitation():   
    # Convert date value to datetime object to find max date
    #https://bootcampspot.instructure.com/courses/4981/external_tools/313 provided correct syntax
    
    # Call all date values from database
    date_values = session.query(Measurement.c.date).all()
    # Convert date strings to datetime objects
    date_objects = [datetime.strptime(date[0], '%Y-%m-%d') for date in date_values]
    #Find maximum date in database
    max_date_obj = max(date_objects)
    
    #Subtract timedelta object from datetime object
    last_12_months_data = session.query(Measurement.c.date, Measurement.c.prcp).filter(Measurement.c.date >= (max_date_obj - timedelta(days=365))).all()
    #Convert 'None' to 0.0 for days with no precipitation
    last_12_months_data_fixed = [(date, 0.0 if prcp is None else prcp) for date, prcp in last_12_months_data]
 
    # Convert query results to list of dictionaries
    twelvemonthsdata_list = []
    for row in last_12_months_data_fixed:
        data_dict = {'date': row[0],'precipitation': row[1]}
        twelvemonthsdata_list.append(data_dict) 
    return jsonify(twelvemonthsdata_list)

# Define the /api.v1.0/stations route
@app.route("/api.v1.0/stations")
def stations():
    # Count number of instances unique value of 'station' appears in table:
    station_ids = session.query(Measurement.c.station).group_by(Measurement.c.station).all()  
    # Extract station IDs from query result
    station_ids_list = [id[0] for id in station_ids]
    # Return list of station IDs as JSON response
    return jsonify(station_ids_list)  
 
# Define the /api.v1.0/tobs route
import datetime
@app.route("/api.v1.0/tobs")
def tobs():
    # Convert date value to datetime object to find max date
    #https://bootcampspot.instructure.com/courses/4981/external_tools/313 provided correct syntax
    
    # Call date values from database
    date_values = session.query(Measurement.c.date).all()
    # Convert date strings to datetime objects
    date_objects = [datetime.strptime(date[0], '%Y-%m-%d') for date in date_values]
    #Find maximum date in database
    max_date_obj = max(date_objects)

    # Count number of instances unique value of 'station' appears in table:
    counts_by_station = session.query(Measurement.c.station, func.count(Measurement.c.station))\
        .group_by(Measurement.c.station).order_by(func.count(Measurement.c.station).desc()).all()  #order in descending order

    # Convert query result to list of dictionaries
    counts_by_station_dict = [{'station': row[0], 'count': row[1]} for row in counts_by_station]
 
    # Find station in 'counts_by_station_dict' with highest count value
    # extract only station with highest 'count' value in list of dictionaries, can't pass dictionary to query below
    #https://bootcampspot.instructure.com/courses/4981/external_tools/313 provided correct syntax
    station_with_highest_count = max(counts_by_station_dict, key=lambda x: x['count'])['station']

    # Query for most recent year's worth of temperature observations for station with highest observation count
    #Subtract timedelta object from datetime object:
    #last_12_months_tobs = session.query(measurement.columns.date, measurement.columns.tobs).filter((measurement.columns.date >= (max_date - timedelta(days=365)), measurement.columns.station == station_with_highest_count)).all()
    last_12_months_tobs = session.query(Measurement.c.date, Measurement.c.tobs).filter(Measurement.c.date >= (max_date_obj - timedelta(days=365)), Measurement.c.station == station_with_highest_count).all()

    # Convert 'None' to 0.0 for days with no tobs measurement
    last_12_months_tobs_fixed = [(date, 0 if tobs is None else tobs) for date, tobs in last_12_months_tobs]
    
    # Convert query results to list of dictionaries
    last12tobs_list = []
    for row in last_12_months_tobs_fixed:
        data_dict = {'date': row[0],'temperature': row[1]}
        last12tobs_list.append(data_dict) 
    return jsonify(last12tobs_list) 
 
# Define the /api.v1.0/start route
from flask import Flask
from datetime import datetime
@app.route("/api.v1.0/<start>")
def get_start(start):
    # Validate format of start date
    try:
        # Attempt to parse start date in 'YYYY-MM-DD' format
        datetime.strptime(start, '%Y-%m-%d')
    #Return error message if start date isn't in 'YYYY-MM-DD' format
    except ValueError:
        return "Invalid date format. Please provide the date in 'YYYY-MM-DD' format.", 400
 
    min_temp = session.query(func.min(Measurement.c.tobs)).filter(Measurement.c.date >= start).scalar()
    max_temp = session.query(func.max(Measurement.c.tobs)).filter(Measurement.c.date >= start).scalar()
    mean_temp = session.query(func.avg(Measurement.c.tobs)).filter(Measurement.c.date >= start).scalar()    
    return jsonify({"Minimum Temperature": min_temp, "Maximum Temperature": max_temp, "Mean Temperature": mean_temp})

# Define the /api.v1.0/trip/<start>/<end> route
from flask import Flask
from datetime import datetime
@app.route("/api/v1.0/trip/<start>/<end>")
def get_start_end(start, end):
    # Validate format of start date
    try:
        # Attempt to parse start and end dates in 'YYYY-MM-DD' format
        datetime.strptime(start, '%Y-%m-%d')
        datetime.strptime(end, '%Y-%m-%d')
    #Return error message if start date isn't in 'YYYY-MM-DD' format
    except ValueError:
        return "Invalid date format. Please provide the date in 'YYYY-MM-DD' format.", 400    
    min_temp = session.query(func.min(Measurement.c.tobs)).filter(Measurement.c.date >= start, Measurement.c.date <= end).scalar()
    max_temp = session.query(func.max(Measurement.c.tobs)).filter(Measurement.c.date >= start,Measurement.c.date <= end).scalar()
    mean_temp = session.query(func.avg(Measurement.c.tobs)).filter(Measurement.c.date >= start,Measurement.c.date <= end).scalar()   
   
    return jsonify({"Minimum Temperature": min_temp, "Maximum Temperature": max_temp, "Mean Temperature": mean_temp})
 
 # Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

session.close()    