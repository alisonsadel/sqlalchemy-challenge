
# 1. Import Modules
####################################
from flask import Flask, jsonify, make_response
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from scipy import stats as sts

# 2. Administrative Set-Up
####################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# Produce a declarative automap_base to reflect existing database into new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Reflect Database 'measurement' and 'station' into ORM class
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)


# 3. Create the app
####################################
app = Flask(__name__)

# 4. Create Flask routes
####################################

@app.route("/")
def homepage():
    # List all available API routes
    return (
    f"<h1> Welcome to the Surfs Up API! </h1><br/>"
    "<h2>Available Routes:</h2>"

    "<strong>Precipitation Data</strong>"
    "<br/>"
    "/api/v1.0/precipitation<br/>"
    "<br/>"

    "<strong>A list of all weather observation stations</strong>"
    "<br/>"
    "/api/v1.0/stations<br/>"
    "<br/>"

    "<strong>Temperature Observations</strong>"
    "<br/>"
    "/api/v1.0/tobs<br/>"
    "<br/>"

    "<strong>A JSON list of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date</strong>"
    "<br/>"
    '/api/v1.0/"(start_date)"<br/>'
    "<br/>"

    "<strong>A JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range</strong>"
    "<br/>"
    '/api/v1.0/"(start_date)"/"(End_Date)"<br/>'
    "<br/>"
    "Date Formatting: enter as YYYY-MM-DD/YYYY-MM-DD" 
    ) 

# API route - api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_twelve = (dt.date(2017,8,23) - dt.timedelta(days=365))
    rain_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_twelve ).order_by(Measurement.date).all()
    rain_data_dict = {date: prcp for date, prcp in rain_data}
    return jsonify(rain_data_dict)

# API route - /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station, Station.name).all()
    station_dict = list(np.ravel(station_list))
    return jsonify(station_dict)
   
# API route - /api/v1.0/tobs
@app.route('/api/v1.0/tobs')
def tobs():
    tobs_list = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date>="2016-08-23").\
        filter(Measurement.date>="2017-08-23").all()
    tobs_dict = list(np.ravel(tobs_list))
    return jsonify(tobs_dict) 

# # API route - start date
@app.route('/api/v1.0/<start>')
def start_date(start):
    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    # Convert to normal list to be Jsonified
    start_date_list = list(start_date)
    return jsonify(start_date_list)

# # API route - end date
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    start_end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()  
    start_end_date_list = list(start_end_date)
    return jsonify(start_end_date_list)

session.close()

if __name__ == "__main__":
    app.run(debug=True)


