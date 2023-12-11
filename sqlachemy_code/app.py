# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, exc

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
        f"Available Routes: <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/precipitation </br>"
        f"/api/v1.0/tobs </br>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end <br/>"
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

@app.route("/api/v1.0/start")
def start():
    review = [Measurement.date,
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]
    
    #year_data = dt.date(2017, 8, 23)-dt.timedelta(days=365)
    year_data = dt.date(2017, 8, 23)-dt.timedelta(days=365)
    prcp_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_data)

    # start_data = session.query(*review).\
    #         filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
    #         group_by(Measurement.date).all()
    #         order_by(Measurement.date).all()    
    
    session.close()

    start_date = []
    for date, min, max, avg in start_date:
        start_dict = {}
        start_dict["date"] = date
        start_dict["Min_temp_F°"] = min
        start_dict["Max_temp_F°"] = max
        start_dict["Aver_temp_F°"] = avg
        start_date.append(start_dict)

    return jsonify(start_date)


@app.route("/api/v1.0/start/end")
def start_end(start, end):
    review = [Measurement.date,
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)]
       
    start_end_data = session.query(*review).\
            filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).\
            filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).\
            group_by(Measurement.date).\
            order_by(Measurement.date).all()    
    
    session.close()

    start_end_date = []
    for date, min, max, avg in start_end_date:
        se_dict = {}
        se_dict["date"] = date
        se_dict["Min_temp_F°"] = min
        se_dict["Max_temp_F°"] = max
        se_dict["Aver_temp_F°"] = avg
        start_end_date.append(se_dict)

    return jsonify(start_end_date)

if __name__ == "__main__":
    app.run(debug=True)