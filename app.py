import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def homepage():
    return (
        f"SQLAlchemy Challenge Website<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    a_year_ago = dt.datetime(2016, 8, 23)

    prcp = session.query(func.avg(Measurement.prcp), Measurement.date).\
    filter(Measurement.date > a_year_ago).\
    group_by(Measurement.date).all()

    session.close()

    prcp_list = []

    for number, date in prcp:
        prcp_list.append({f"{date}": number})

    return (
        jsonify(prcp_list)
    )

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    station_list = session.query(Station.station).all()

    session.close()

    return (
        jsonify(station_list)
    )

@app.route("/api/v1.0/tobs")
def tobs():

    a_year_ago = dt.datetime(2016, 8, 23)

    session = Session(engine)

    tobs = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date > a_year_ago).all()

    session.close()
    
    return (
        jsonify(tobs)
    )

@app.route("/api/v1.0/<start>")
def start_date_only(start):
    
    date = start

    session = Session(engine)

    min_tobs = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= date).all()
    avg_tobs = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= date).all()
    max_tobs = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= date).all()

    session.close()

    test = min_tobs[0][0]

    if test is None:
        return (jsonify({"error": "Please format the date as YYYY-MM-DD."}), 404)
    else:
        return (
            #jsonify(min_tobs[0][0])
            jsonify({
            "min_tobs": min_tobs,
            "avg_tobs": avg_tobs,
            "max_tobs": max_tobs})
            #f"The Minimum Tempurature on {date} was {min_tobs[0]}</br>"
            #f"The Average Tempurature on {date} was {avg_tobs[0]}</br>"
            #f"The Maximum Tempurature on {date} was {max_tobs[0]}</br>"
    )

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    date_start = start
    date_end = end

    session = Session(engine)

    min_tobs = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date <= date_end).\
        filter(Measurement.date >= date_start).all()
    avg_tobs = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date <= date_end).\
        filter(Measurement.date >= date_start).all()
    max_tobs = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date <= date_end).\
        filter(Measurement.date >= date_start).all()

    session.close()

    test = min_tobs[0][0]

    if test is None:
        return (jsonify({"error": "Please format the date as YYYY-MM-DD."}), 404)
    else:
        return (
            jsonify({
            "min_tobs": min_tobs,
            "avg_tobs": avg_tobs,
            "max_tobs": max_tobs})

            #f"The Minimum Tempurature between {date_start} and {date_end} was {min_tobs[0]}</br>"
            #f"The Average Tempurature between {date_start} and {date_end} was {avg_tobs[0]}</br>"
            #f"The Maximum Tempurature between {date_start} and {date_end} was {max_tobs[0]}</br>"
    )

if __name__ == '__main__':
    app.run(debug=True)