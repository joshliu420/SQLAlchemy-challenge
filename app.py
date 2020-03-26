import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import pandas as pd
import datetime as dt
from datetime import timedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def welcome():
    """List all available api routes."""
    return (
        f"Here Are All The Available Routes:<br/>"
        f"<br/>"
        f"For Precipitation Data in Past 12 Month:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"For All The Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"For Tobs Data in Past 12 Month:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"For General Tobs Data Since a Given Date (format: yyyy-mm-dd, between 2010-01-01 and 2017-08-23):<br/>"
        f"/api/v1.0/YourStartDate<start><br/>"
        f"<br/>"
        f"For General Tobs Data Between a Given Start & End Date (format: yyyy-mm-dd, between 2010-01-01 and 2017-08-23):<br/>"
        f"/api/v1.0/YourStartDate<start>/YourEndDate<end>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():

    """Precipitation for past 12 month"""
    # Query all past 12 month
    one_year_ago = '2016-08-23'
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date)

    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    results_list = []
    for date, prcp in results:
        results_list.append({date: prcp})
    
    return jsonify(results_list)



@app.route("/api/v1.0/stations")
def stations():
    
    """All the stations"""
    # Query all stations
    results = session.query(Station.station).all()

    return jsonify(results)



@app.route("/api/v1.0/tobs")
def tobs():
    
    """Tobs for last 12 month"""
    # Query tobs data for last 12 month
    one_year_ago = '2016-08-23'
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).order_by(Measurement.date).all()
    
    results_list = [{date: temp} for date, temp in results]

    return jsonify(results_list)



@app.route("/api/v1.0/<start>")
def temps(start):
    
    """Tobs for your date"""
    # formating the input start date
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    # Query tobs data for the given start date
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start_date).all()[0]
    
    results_list=[{'Min_Temp':results[0]}, {'Avg_Temp': results[1]}, {'Max_Temp': results[2]}]
   
    return jsonify(results_list)



@app.route("/api/v1.0/<start>/<end>")
def trips(start, end):
        
    """Tobs for your trip"""
    # formating the input start and end date
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    # Query tobs data between the given start and end date
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()[0]
    
    results_list=[{'Min_Temp':results[0]}, {'Avg_Temp': results[1]}, {'Max_Temp': results[2]}]
   
    return jsonify(results_list)
    

if __name__ == '__main__':
    app.run(debug=True)
