
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route('/')
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"'/api/v1.0/[start format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start format:yyyy-mm-dd]/[end format:yyyy-mm-dd]<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query to retrieve the last 12 months of precipitation data 
    prcp_data=session.query(Measurement.date,Measurement.prcp)\
           .filter(Measurement.date>='2016-08-24')\
           .filter(Measurement.date<='2017-08-23').all()

    session.close()

    # Create a dictionary from the  data
    all_prcp = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route('/api/v1.0/stations')
def Station():
    session = Session(engine)
     
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    all_station = list(np.ravel(results))
    return jsonify(all_station)

@app.route('/api/v1.0/tobs')
def Tobs():
    session = Session(engine)
    # Query the last year's temperature observationof the most active station
    temp_data = session.query(Measurement.date,Measurement.tobs)\
           .filter(Measurement.date>='2016-08-24')\
           .filter(Measurement.date<='2017-08-23')\
           .filter(Measurement.station == 'USC00519281').all()
    session.close()


    # Create a dictionary from the  data
    all_temp = []
    for date, tobs in temp_data:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs

        all_temp.append(temp_dict)

    return jsonify(all_temp)

@app.route('/api/v1.0/<start>')
def Start(start):
    session = Session(engine)
    start = session.query(Measurement.date).\
            group_by(Measurement.date).order_by(Measurement.date.asc()).first()
    start_temp= session.query(func.min(Measurement.tobs),\
                            func.max(Measurement.tobs),\
                            func.avg(Measurement.tobs))\
                            .filter(Measurement.date>= start).all()

    session.close()

    start_date_temp = []
    for min, avg, max in start_temp:
        starttemp_dict = {}
        starttemp_dict["max"] = max
        starttemp_dict["min"] = min
        starttemp_dict["avg"] = avg

        start_date_temp.append(starttemp_dict)

    return jsonify(start_date_temp)


if __name__ == "__main__":
    app.run(debug=True)