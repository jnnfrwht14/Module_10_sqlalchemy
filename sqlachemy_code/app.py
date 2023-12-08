# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
    """List all available API routes"""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/precipitation </br>"
        f"/api/v1.0/tobs </br>"
    )

@app.route("/api/v1.0/stations")
def stations():
    return stations

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    #all_prcp=[]
    #for ,

@app.route("/api/v1.0/tobs")
def tobs():
    return tobs


# Define what to do when a user hits the /jsonified route
@app.route("/jsonified")
def jsonified():
    return jsonify(stations)
 
results = session.query(stations.name).all()

session.close()

if __name__ == "__main__":
    app.run(debug=True)

