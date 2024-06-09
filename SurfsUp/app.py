# Import the dependencies.
from flask import Flask, jsonify
import warnings
warnings.filterwarnings('ignore')
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
import pandas as pd
import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    #List all routes needed
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2015-01-01<br/>"
        f"/api/v1.0/2010-08-25/2014-08-25<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    """Return a dictionary of last 12 months of precipitation data including date, and inches of precipitation"""
    #Get the last 12 months of data
    most_recent_date = dt.datetime(2017,8,23)
    last_12 = most_recent_date - dt.timedelta(days=365)
    twelve_month_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= last_12).\
    order_by(measurement.date).all()
    #Dictionary of results with date as key and prcp as value
    precip_dict = [{date:prcp} for date, prcp in twelve_month_prcp]
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    #Query station id and name and put in list  of dictionaries
    """Return a list of stations from dataset"""
    stations_query = session.query(station.station, station.name).all()
    station_list = [{station:name} for station, name in stations_query]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temps():
    """Return a list of temperature observations for the last 12 months for the most active station."""
    #Query to find the most active station and its ID
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).\
        first()
    most_active_id = most_active_station[0]
    
    #Find most recent date
    most_recent_date = dt.datetime(2017,8,23)
    last_12 = most_recent_date - dt.timedelta(days=365)
    
    #Query temps for last 12 months with most active ID
    twelve_month_temp = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= last_12).\
        filter(measurement.station == most_active_id).all()

    #Convert to list of dictionaries
    temps_list = [{"date": date, "tobs": tobs} for date, tobs in twelve_month_temp]
    
    return jsonify(temps_list)

@app.route("/api/v1.0/2015-01-01")
def start_date():
    """Return min,max,avg temps for dates greater than specified start date."""
    start_dt = dt.datetime(2015,1,1)
    #Query to get stats for dates specified
    start_query = session.query(func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
                            filter(measurement.date >= start_dt).all()
    #Take queries and put into a list of dictionaries
    start_list = [{"TMIN": query[0], "TAVG": query[1], "TMAX": query[2]} for query in start_query]
    return jsonify(start_list)

@app.route("/api/v1.0/2010-08-25/2014-08-25")
def start_end_date():
    """Return min,max,avg temps between start and end date."""
    start_dt = dt.datetime(2010,8,25)
    end_dt = dt.datetime(2014,8,25)
    #Query to get stats for dates specified
    stats_query = session.query(func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
              filter(measurement.date >= start_dt).\
              filter(measurement.date <= end_dt).all()
    #Take queries and put into a list of dictionaries
    start_end_list = [{"TMIN": query[0], "TAVG": query[1], "TMAX": query[2]} for query in stats_query]
    
    return jsonify(start_end_list)


if __name__ == "__main__":
    app.run(debug=True)