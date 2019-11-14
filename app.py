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

Base.classes.keys


app = Flask(__name__)


@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<stat>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    Measurement = Base.classes.measurement

    session = Session(engine)
    
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-22').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

    session.close()

    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    Measurement = Base.classes.measurement

    session = Session(engine)

    results = session.query(Measurement.station).\
    group_by(Measurement.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    Measurement = Base.classes.measurement

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-08-22').\
    group_by(Measurement.tobs).\
    order_by(Measurement.date.desc()).all()

    session.close()

    tobs = list(np.ravel(results))
    
    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def start_date(start):  
    Measurement = Base.classes.measurement

    session = Session(engine)

    results = session.query(Measurement.date, func.max(Measurement.tobs), 
    func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
    group_by(Measurement.date).\
    filter(Measurement.date >= start).all()

    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):  
    Measurement = Base.classes.measurement

    session = Session(engine)

    results = session.query(Measurement.date, func.max(Measurement.tobs), 
    func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
    group_by(Measurement.date).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    session.close()
    
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
