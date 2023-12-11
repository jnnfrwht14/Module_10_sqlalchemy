# Import the dependencies.
import numpy as np
import datetime as dt
from datetime import date

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()
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
def home():
#     """List all available API routes"""
    return (
        f"Welcome to Hawaii's climate API <br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/precipitation </br>"
        f"/api/v1.0/tobs </br>"
        f"/api/v1.0/enter_start_date <br/>"
        f"/api/v1.0/enter_start_date/enter_end_date <br/>"
        F"Please enter dates in YYYY-mm-dd format"
    )

@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Station.id, Station.name, Station.elevation, Station.station, Station.latitude, Station.longitude).all()
    
    # Close the session
    session.close()
    
    # Convert list of tuples into normal list
    station_list = []
    for id, name, elevation, station, latitude, longitude in station_data:
        station_dict = {}
        station_dict["ID"] = id
        station_dict["Name"] = name
        station_dict["Elevation"] = elevation
        station_dict["Station"] = station
        station_dict["Latitude"] = latitude
        station_dict["Longitude"] = longitude
        station_list.append(station_dict)
    
    # Return a JSON list of stations from the dataset.
    return jsonify(station_list)


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    year_data = dt.date(2017, 8, 23)-dt.timedelta(days=365)

    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_data)

    session.close()

    # Create a dictionary from the row data
    all_prcp = []
    for date, prcp in prcp_scores:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation (in)"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/tobs")
def tobs():
    year_data = dt.date(2017, 8, 23)-dt.timedelta(days=365)

    TOBS_data = session.query(Measurement.date, Measurement.tobs).filter_by(station = "USC00519281").\
        filter(Measurement.date >= year_data).all()
    
    session.close()

    all_tobs = []
    for date, prcp in TOBS_data:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temp Observation F"] = prcp
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    start_date = date.fromisoformat(start)

    query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()

    session.close()

    temp_data = []
    for min, max, avg in query:    
        temp_dict = {}
        temp_dict["Minimum Temperature F degrees"] = min
        temp_dict["Maximum Temperature F degrees"] = max
        temp_dict["Average Temperature"] = avg
        temp_data.append(temp_dict)

    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def se_date(start, end):

    session = Session(engine)

    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)

    query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    session.close()

    temp_data = []
    for min, max, avg in query:    
        temp_dict = {}
        temp_dict["Minimum Temperature F degrees"] = min
        temp_dict["Maximum Temperature F degrees"] = max
        temp_dict["Average Temperature"] = avg
        temp_data.append(temp_dict)

    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)